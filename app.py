from fastapi import FastAPI, Response
from fastapi.responses import StreamingResponse, HTMLResponse
import cv2, logging, threading, contextlib, io

from utils import Model, Detect
model_wrapper = Model('yolo26n.pt')
model_wrapper.validate()
model_wrapper.load_model()
model = model_wrapper.model
CONF_THRESHOLD = 0.3

# Detector and lock for thread-safe model inference
detector = Detect(model=model, conf_threshold=CONF_THRESHOLD)
model_lock = threading.Lock()

try:
    logging.getLogger('ultralytics').setLevel(logging.WARNING)
except Exception:
    pass

app = FastAPI()

cam = cv2.VideoCapture(0)

cam_lock = threading.Lock()

def gen_frames():
    while True:
        with cam_lock:
            success, frame = cam.read()
        if not success:
            break

        # Run detection on the frame (protected by model_lock)
        detected_frame = None
        try:
            with model.lock:
                detected_frame = detector.detect(frame)
        except Exception:
            detected_frame = None

        output_frame = detected_frame if detected_frame is not None else frame

        ret, buffer = cv2.imencode('.jpg', output_frame)
        if not ret:
            continue

        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.get('/', response_class=HTMLResponse)
async def index():
    return HTMLResponse(content=(
        "<html>"
        "<head><title>Video Streaming</title></head>"
        "<body>"
        "<h1>Streaming Kamera (FastAPI)</h1>"
        "<img src=\"/video_feed\" width=\"640\" height=\"480\"/>"
        "</body></html>"
    ))

@app.get('/video_feed')
def video_feed():
    return StreamingResponse(gen_frames(), media_type='multipart/x-mixed-replace; boundary=frame')

@app.on_event('shutdown')
def shutdown_event():
    with cam_lock:
        if cam.isOpened():
            cam.release()
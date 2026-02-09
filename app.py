from fastapi import FastAPI
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import cv2, logging, threading
from pathlib import Path

from utils import Model, Detect
model_wrapper = Model('yolo26n.pt')
model_wrapper.validate()
model_wrapper.load_model()
model = model_wrapper.model

CONF_THRESHOLD = 0.7

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

        detected_frame = None
        try:
            with model_lock:
                detected_frame = detector.Detect(frame)
        except Exception as e:
            logging.exception(f"Error during detection: {e}")
            detected_frame = None

        output_frame = detected_frame if detected_frame is not None else frame

        ret, buffer = cv2.imencode('.jpg', output_frame)
        if not ret:
            continue

        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"
INDEX_HTML_PATH = TEMPLATES_DIR / "index.html"

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get('/', response_class=HTMLResponse)
async def index():
    """
    Mengembalikan halaman HTML dari file templates/index.html.
    Placeholder __CONF_THRESHOLD__ di dalam HTML akan diganti dengan nilai
    CONF_THRESHOLD dari Python.
    """
    html = INDEX_HTML_PATH.read_text(encoding="utf-8")
    html = html.replace("__CONF_THRESHOLD__", str(CONF_THRESHOLD))
    return HTMLResponse(content=html)

@app.get('/video_feed')
def video_feed():
    return StreamingResponse(gen_frames(), media_type='multipart/x-mixed-replace; boundary=frame')

@app.on_event('shutdown')
def shutdown_event():
    with cam_lock:
        if cam.isOpened():
            cam.release()
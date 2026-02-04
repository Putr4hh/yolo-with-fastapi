from utils import Model
from utils import Camera
from utils import Detect
import cv2

VERBOSE = False


if __name__ == "__main__":
    m = Model()
    m.validate()
    m.load_model()

    cam = Camera()  # default 0
    try:
        cam.initialize_camera()
    except Exception as e:
        print('Gagal inisialisasi kamera:', e)
        exit(1)

    d = Detect(m.model)

    try:
        while True:
            ret, frame = cam.read_frame()
            if not ret:
                break

            results = d.detect(frame)
            
            cv2.imshow('BAIM WONG', results)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except Exception as e:
        print('Error menampilkan hasil:', e)
        exit(1)
    finally:
        cam.release()
        cv2.destroyAllWindows()

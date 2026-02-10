from utils import Model
from utils import Camera
from utils import Detect
import cv2


if __name__ == "__main__":

    # Running Model
    m = Model()
    m.validate()
    m.load_model()

    # Running Camera
    cam = Camera()
    try:
        cam.initialize()
    except Exception as e:
        print(f'gagal inisialisasi camera: ', e)

    d = Detect(m.model)

    try:
        while True:
            ret, frame = cam.read_frame()
            if not ret:
                break

            results = d.detect(frame)

            cv2.imshow('hola', results)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except Exception as e:
        print(f'error menampilkan hasil:', e)
        exit(1)

    finally:
        cam.release()
        cv2.destroyAllWindows()
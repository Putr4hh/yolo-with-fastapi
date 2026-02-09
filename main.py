from utils import Model
from utils import Camera
from utils import Detect
import cv2


if __name__ == "__main__":

    # Running Model
    m = Model()
    m.validate()
    m.load_model()

    # Running camera
    cam = Camera()
    try:
        cam.initialize()
    except Exception as e:
        print('Gagal initialize')
        exit(1)

    # Detect
    d = Detect(m.model)

    try:
        while True:
            ret, frame = cam.read_frame()
            if not ret:
                break

            results = d.Detect(frame)

            cv2.imshow('HEHE', results)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    except Exception as e:
        print('Error menampilan hasil:', e)
        exit(1)

    finally:
        cam.release()
        cv2.destroyAllWindows()
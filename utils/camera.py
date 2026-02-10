import cv2, logging

from sympy import false

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Camera Class
class Camera:

    # Variabel
    def __init__(self, camera_id=0):
        self.camera_id = camera_id
        self.camera = None

    # Initialize
    def initialize(self):
        try:
            logger.info(f'initialize camera (Camera ID: {self.camera_id})')
            self.camera = cv2.VideoCapture(self.camera_id)

            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
            self.camera.set(cv2.CAP_PROP_FPS, 30)

            if not self.camera.isOpened():
                logger.error('gagal tidak bisa dibuka')
                raise RuntimeError('gagal tidak bisa dibuka')

            logger.info('camera berhasil dibuka')

        except Exception as e:
            logger.error('gagal initialize camera')
            raise

    # Read frame
    def read_frame(self):
        try:
            if self.camera is None:
                logger.error('Camera belom dianiliasasi')
                return False, None

            ret, frame = self.camera.read()
            if not ret:
                logger.error('gagal membaca frame')
                return False, None
            return True, frame

        except Exception as e:
            logger.exception(f'gagal read_frame: {e}')
            return False, None

    # Release
    def release(self):
        try:
            if self.camera:
                self.camera.release()
                logger.info('camera dilepas')
        except Exception as e:
            logger.exception(f'gagal release camera: {e}')
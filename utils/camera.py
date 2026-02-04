import cv2, logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Camera:
    def __init__(self, camera_id=0):
        self.camera_id = camera_id
        self.camera = None

    def initialize_camera(self):
        try:
            logger.info(f'Membuka kamera (device ID: {self.camera_id})...')
            self.camera = cv2.VideoCapture(self.camera_id)

            if not self.camera.isOpened():
                logger.error('Tidak bisa buka kamera!')
                raise RuntimeError('Tidak bisa buka kamera!')

            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
            self.camera.set(cv2.CAP_PROP_FPS, 30)

            logger.info('Camera berhasil dibuka')
        except Exception as e:
            logger.exception(f'Error initialize kamera: {e}')
            raise

    def read_frame(self):
        try:
            if self.camera is None:
                logger.error('Kamera belum diinisialisasi')
                return False, None
            ret, frame = self.camera.read()
            if not ret:
                logger.error('Gagal membaca frame dari kamera')
                return False, None
            return True, frame
        except Exception as e:
            logger.exception(f'Error read_frame: {e}')
            return False, None

    def release(self):
        try:
            if self.camera:
                self.camera.release()
                logger.info('Kamera dilepas')
        except Exception as e:
            logger.exception(f'Error release kamera: {e}')
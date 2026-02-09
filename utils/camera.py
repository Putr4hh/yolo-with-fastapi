import cv2, logging

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
            logger.info(f'pengecekan camera (Device ID: {self.camera_id})')
            self.camera = cv2.VideoCapture(self.camera_id)

            # Setting camera
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
            self.camera.set(cv2.CAP_PROP_FPS, 60)

            # Semisal camera ga kebuka
            if not self.camera.isOpened():
                logger.error('Camera gagatidak bisal dibuka')
                raise RuntimeError('Camera tidak bisa dibuka')
            
            logger.info('Camera berhasil dibuka')
            
        except Exception as e:
            logger.error(f'Gagal inilize camera: {e}')
            raise

    # Read frame
    def read_frame(self):
        try:
            if self.camera is None:
                logger.error('Camera belum inisialisasi')
                return False, None
            
            ret, frame = self.camera.read()
            if not ret:
                logger.error('Gagal membaca frame')
                return False, None
            return True, frame
        
        except Exception as e:
            logger.exception(f'Erorr Read_frame: {e}')
            return False, None
        
    # Release
    def release(self):
        try:
            if self.camera:
                self.camera.release()
                logger.info('camera dilepas')
        except Exception as e:
            logger.exception('Gagal release camera: {e}')
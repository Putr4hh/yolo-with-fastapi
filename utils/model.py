import os, logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Model:
    def __init__(self, model_path='yolo26n.pt'):
        self.model_path = model_path
        self.model = None

    def validate(self):
        if not os.path.exists(self.model_path):
            logger.error(f'Model file tidak ditemukan {self.model_path}')
            exit(1)
        logger.info(f'Model file ditemukan {self.model_path}')

    def load_model(self):
        try:
            logger.info('Loading YOLO model')
            from ultralytics import YOLO
            self.model = YOLO(self.model_path)
            logger.info(f'Model loaded berhasil')
        except Exception as e:
            logger.error(f'Gagal memuat model: {e}')
            exit(1)

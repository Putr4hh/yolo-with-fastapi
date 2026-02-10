import os, logging
from sys import exception

from ultralytics.models import yolo

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Model Class
class Model:

    # Variabel
    def __init__(self, model_path='yolo26n.pt'):
        self.model_path = model_path
        self.model = None

    # Validate
    def validate(self):
        logger.info('mengecek model')
        if not os.path.exists(self.model_path):
            logger.error(f'Model gada {self.model_path}')
            exit(1)

    # Load model
    def load_model(self):
        try:
            logger.info('memuat model')
            from ultralytics import YOLO
            self.model = YOLO(self.model_path)
            logger.info(f'memuat berhasil {self.model_path}')
        except Exception as e:
            logger.error(f'gagal memuat {self.model_path}')
            exit(1)
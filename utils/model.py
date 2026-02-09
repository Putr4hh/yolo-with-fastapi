import os, logging

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
        
        # Check is modul avalable?
        if not os.path.exists(self.model_path):
            logger.error(f'model path tidak ada {self.model_path}')
            exit(1)
        logger.info(f'ada model {self.model_path}')

    # Memuat model
    def load_model(self):

        # Load model
        try:
            logger.info('Pengecekan model')
            from ultralytics import YOLO
            self.model = YOLO(self.model_path)
            logger.info('model memuat berhasil')
        except Exception as e:
            logger.error('Error memuat model: {e}')
            exit(1)
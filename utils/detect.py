import logging
import time
import cv2

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Detect:

    # Variabel
    def __init__(self, model=None, conf_threshold=0.1):
        self.model = model
        self.conf_threshold = conf_threshold

    # detect
    def detect(self, frame):
        try:
            if self.model is None:
                logger.error('Model belum dianalisis')
                return None

            results = self.model(frame, verbose=False, conf=self.conf_threshold)

            img = results[0].plot()

            return img
        
        except Exception as e:
            logger.error(f'Detect gagal: {e}')
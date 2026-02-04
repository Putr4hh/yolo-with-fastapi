import logging, cv2

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Detect:
    def __init__(self, model=None, conf_threshold=0.5):
        self.model = model
        self.conf_threshold = conf_threshold

    def detect(self, frame):
        try:
            if self.model is None:
                logger.error('Model belum diinisialisasi pada Detect')
                return None
            results = self.model(frame, verbose=False, conf=self.conf_threshold)
            # Plot hasil deteksi (kembali sebagai numpy array BGR)
            img = results[0].plot()
            # Tambahkan informasi (jumlah deteksi) pada gambar
            self.draw_info(img, results[0])
            return img
        except Exception as e:
            logger.exception(f"Error during detection: {e}")
            return None
        
    def draw_info(self, image, results):
        try:
            det_count = len(results.boxes) if results.boxes is not None else 0
            cv2.putText(image, f'Detections: {det_count}', (10, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        except Exception as e:
            logger.exception(f"Error drawing info: {e}")
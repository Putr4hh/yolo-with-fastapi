import logging
import time
import cv2

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Detect:

    # Variabel
    def __init__(self, model=None, conf_threshold=0.5):
        self.model = model
        self.conf_threshold = conf_threshold
        self.prev_time = None
        self.fps = 0.0

    # Detect
    def Detect(self, frame):
        try:
            if self.model is None:
                logger.error('Model Belum Diinisialisasi Pada Detect')
                return None

            # Update FPS setiap frame
            self.update_fps()

            results = self.model(frame, verbose=False, conf=self.conf_threshold)
            
            img = results[0].plot()
            num_detections = len(results[0].boxes)

            # Gambar jumlah deteksi
            img = self.draw_detection_count(img, num_detections)

            # Gambar FPS (fungsi terpisah)
            img = self.draw_fps(img)

            return img
        
        except Exception as e:
            logger.exception(f"Error during detection: {e}")
            return None


    def draw_detection_count(self, img, num_detections):

        # Text jumlah deteksi
        text_det = f'Detection: {num_detections}'

        # Setting font dll...
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.9
        thickness = 2

        # Posisi X,Y di frame
        x = 50
        y = 100          # baris untuk Detection

        # Gambar text Detection
        cv2.putText(img, text_det, (x, y), font, font_scale, (0, 255, 0), thickness)

        return img

    def update_fps(self):
        """
        Hitung dan update nilai FPS berdasarkan selisih waktu antar frame.
        Fungsi ini hanya mengurus logika FPS (dipisah dari gambar teks).
        """
        curr_time = time.time()
        if self.prev_time is None:
            self.fps = 0.0
        else:
            dt = curr_time - self.prev_time
            if dt > 0:
                self.fps = 1.0 / dt
        self.prev_time = curr_time


    def draw_fps(self, img):
        """
        Gambar teks FPS di bawah teks Detection.
        Fungsi ini terpisah dari draw_detection_count sesuai permintaan.
        """
        text_fps = f'FPS: {self.fps:.2f}'

        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.9
        thickness = 2

        x = 50
        y = 140  # di bawah Detection (100), selisih 40px

        cv2.putText(img, text_fps, (x, y), font, font_scale, (0, 255, 255), thickness)

        return img
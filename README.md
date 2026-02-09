## YOLO Object Detection dengan FastAPI & OpenCV

Proyek ini adalah contoh sederhana _real‑time object detection_ menggunakan:

- **YOLO (Ultralytics)** sebagai model deteksi objek.
- **OpenCV** untuk akses kamera dan manipulasi frame.
- **FastAPI** untuk menampilkan streaming video hasil deteksi di browser.

Terdapat **2 cara menjalankan deteksi**:

1. **Mode Web (FastAPI)** → akses via browser (`app.py`).
2. **Mode Desktop / OpenCV Window** → akses via jendela OpenCV (`main.py`).

---

### Struktur Proyek

- **`app.py`**: Aplikasi FastAPI untuk streaming video:
  - Endpoint `GET /` → halaman HTML sederhana dengan `<img>` yang menampilkan stream.
  - Endpoint `GET /video_feed` → stream MJPEG dari kamera dengan bounding box, jumlah deteksi, dan FPS.
- **`main.py`**: Script mandiri untuk membuka jendela OpenCV:
  - Membuka kamera.
  - Menjalankan YOLO pada setiap frame.
  - Menampilkan hasil di jendela dengan judul `"HEHE"` dan keluar ketika tombol `q` ditekan.
- **`utils/model.py`** (`Model`):
  - Mengecek keberadaan file model (`yolo26n.pt`).
  - Memuat model YOLO menggunakan `ultralytics.YOLO`.
- **`utils/camera.py`** (`Camera`):
  - Mengelola inisialisasi kamera (`cv2.VideoCapture`).
  - Mengatur resolusi (1920x1080) dan FPS target (60).
  - Menyediakan fungsi `read_frame()` dan `release()`.
- **`utils/detect.py`** (`Detect`):
  - Menjalankan inferensi YOLO pada satu frame.
  - Menggambar bounding box dari hasil `results[0].plot()`.
  - Menghitung dan menampilkan **jumlah deteksi**.
  - Menghitung dan menampilkan **FPS**.
- **`yolo26n.pt`**: File model YOLO yang digunakan (harus berada di direktori utama).
- **`pyproject.toml`**: Konfigurasi proyek Python (minimal dependency).

---

### Kebutuhan Sistem

- **Python**: `>= 3.12`
- **OS**: Windows (proyek ini dibuat dan diuji di Windows; OS lain mungkin perlu penyesuaian kecil).
- **Kamera**: Webcam internal/eksternal yang dikenali oleh sistem.

---

### Instalasi Dependency

Jika Anda ingin cara paling cepat (mengabaikan `pyproject.toml`), Anda bisa langsung:

```bash
pip install fastapi uvicorn ultralytics opencv-python
```

Jika menggunakan **uv / pyproject** (opsional, jika sudah menginstal `uv`):

```bash
uv sync
```

Pastikan file model `yolo26n.pt` sudah ada di direktori root proyek.

---

### Menjalankan Mode Web (FastAPI)

Mode ini menjalankan server FastAPI dan menampilkan hasil deteksi di browser.

1. **Aktifkan virtual environment** (opsional tapi direkomendasikan).
2. Jalankan perintah berikut di root folder proyek:

```bash
uvicorn app:app --reload
```

3. Buka browser dan akses:

```text
http://127.0.0.1:8000/
```

4. Di halaman tersebut akan tampil:
   - Judul: **"Streaming Kamera (FastAPI)"**.
   - Elemen `<img src="/video_feed">` yang menampilkan video streaming dari webcam, dengan:
     - Bounding box dari YOLO.
     - Teks `Detection: X`.
     - Teks `FPS: Y.YY`.

#### Penjelasan Singkat `app.py`

- **Inisialisasi model**:
  - `Model('yolo26n.pt')` memvalidasi dan memuat model YOLO.
  - `Detect` digunakan untuk menjalankan deteksi pada setiap frame.
- **Kamera**:
  - `cv2.VideoCapture(0)` membuka kamera dengan ID `0` (kamera default).
- **Keamanan thread**:
  - `model_lock` dan `cam_lock` digunakan agar akses model dan kamera aman di lingkungan async/web.
- **Fungsi `gen_frames()`**:
  - Membaca frame dari kamera.
  - Menjalankan deteksi.
  - Mengenkode frame ke JPEG.
  - Mengirimkan stream MJPEG ke client.
- **Endpoint**:
  - `GET /` → mengembalikan HTML.
  - `GET /video_feed` → mengembalikan `StreamingResponse` dengan tipe `multipart/x-mixed-replace`.
- **Shutdown event**:
  - `@app.on_event('shutdown')` akan me‑`release` kamera ketika server dimatikan.

---

### Menjalankan Mode Desktop (OpenCV Window)

Mode ini menjalankan script biasa yang membuka window OpenCV, tanpa FastAPI.

Jalankan:

```bash
python main.py
```

Perilaku:

- Script akan:
  - Memuat model YOLO dengan `Model`.
  - Menginisialisasi kamera dengan `Camera.initialize()`.
  - Membaca frame secara loop dan memprosesnya dengan `Detect`.
  - Menampilkan hasil di jendela OpenCV dengan judul `"HEHE"`.
- Tekan **`q`** di jendela video untuk keluar.

Jika kamera gagal di‑initialize, program akan menampilkan pesan **"Gagal initialize"** dan berhenti.

---

### Konfigurasi Penting

- **File model**:
  - Default: `yolo26n.pt` di direktori root.
  - Diatur di `utils/model.py` → `Model(model_path='yolo26n.pt')`.
- **Confidence threshold (kepercayaan deteksi)**:
  - Untuk mode web (`app.py`): `CONF_THRESHOLD = 0.3`.
  - Untuk kelas `Detect` di `utils/detect.py`: default `conf_threshold=0.5` (dapat diubah saat inisialisasi).
- **ID Kamera**:
  - Di `camera.py` → `Camera(camera_id=0)`.
  - Jika Anda memiliki beberapa kamera, ganti ke `1`, `2`, dst sesuai kebutuhan.
- **Resolusi & FPS**:
  - Di `camera.initialize()`:
    - `WIDTH = 1920`
    - `HEIGHT = 1080`
    - `FPS = 60`
  - Anda dapat menurunkan resolusi/FPS jika performa tidak cukup kuat.

---

### Troubleshooting

- **Kamera tidak bisa dibuka**:
  - Pastikan tidak ada aplikasi lain yang sedang menggunakan kamera.
  - Coba ganti `camera_id` (0 → 1, 2, dst).
  - Periksa pesan log di terminal.
- **Model tidak ditemukan**:
  - Pastikan file `yolo26n.pt` benar‑benar ada di root proyek.
  - Path dapat diubah di `Model(model_path=...)`.
- **FPS rendah / lag**:
  - Turunkan resolusi kamera.
  - Jalankan tanpa `--reload` jika sudah stabil.
- **Error saat import `cv2` / OpenCV**:
  - Pastikan `opencv-python` sudah terinstal:
    - `pip install opencv-python`

---

### Pengembangan Lanjutan

Beberapa ide pengembangan tambahan:

- **Menambahkan halaman HTML yang lebih interaktif**:
  - Tombol start/stop stream.
  - Pilih sumber kamera.
- **Endpoint tambahan**:
  - Upload gambar dan mengembalikan hasil deteksi.
  - Menyimpan log deteksi ke file atau database.
- **Konfigurasi via environment variable**:
  - Path model, kamera ID, dan threshold dapat diambil dari variabel lingkungan.

Proyek ini bisa menjadi dasar untuk sistem CCTV sederhana, sistem counting objek, atau demo computer vision berbasis web.


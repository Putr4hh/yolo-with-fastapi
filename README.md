# YOLO + FastAPI 🔧

**Deskripsi singkat:** Proyek ini melakukan deteksi objek realtime menggunakan model YOLO (`yolo26n.pt`) dan menyediakan dua cara menjalankan:
- FastAPI streaming (`app.py`) untuk melihat hasil lewat browser
- Demo lokal (`main.py`) menampilkan jendela OpenCV (tekan `q` untuk keluar)

**Cepat mulai**

- Pasang dependensi:

  ```bash
  pip install fastapi uvicorn ultralytics opencv-python
  ```

- Jalankan server FastAPI:

  ```bash
  uvicorn app:app --reload --host 0.0.0.0 --port 8000
  # buka http://localhost:8000
  ```

- Jalankan demo lokal:

  ```bash
  python main.py
  ```

**Catatan:** Gunakan Python >= 3.12 dan pastikan file `yolo26n.pt` ada di root proyek. Jika kamera tidak menggunakan index 0, ubah pengaturan kamera di `app.py` atau `main.py`. 👌

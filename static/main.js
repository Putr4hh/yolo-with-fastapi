(function () {
    const img = document.getElementById('stream-img');
    const btnPlay = document.getElementById('btn-play');
    const btnPause = document.getElementById('btn-pause');
    const btnFullscreen = document.getElementById('btn-fullscreen');
    const statusDot = document.getElementById('status-dot');
    const statusText = document.getElementById('status-text');
    const loadingOverlay = document.getElementById('loading-overlay');
    const videoWrapper = img ? img.parentElement : null;

    if (!img || !btnPlay || !btnPause || !btnFullscreen || !statusDot || !statusText || !loadingOverlay || !videoWrapper) {
        // Jika elemen belum tersedia, jangan jalankan script lebih jauh.
        return;
    }

    const STREAM_URL = '/video_feed';
    let isStreaming = true;

    function setStatus(state, message) {
        statusDot.classList.remove('online', 'offline');
        if (state === 'online') {
            statusDot.classList.add('online');
        } else if (state === 'offline') {
            statusDot.classList.add('offline');
        }
        statusText.textContent = message;
    }

    function startStream() {
        if (isStreaming) return;
        img.src = STREAM_URL + '?t=' + Date.now();
        isStreaming = true;
        loadingOverlay.style.display = 'flex';
        setStatus('online', 'Streaming berjalan');
    }

    function stopStream() {
        if (!isStreaming) return;
        img.src = '';
        isStreaming = false;
        loadingOverlay.style.display = 'none';
        setStatus('offline', 'Streaming dihentikan (klik Start lagi)');
    }

    btnPlay.addEventListener('click', startStream);
    btnPause.addEventListener('click', stopStream);

    btnFullscreen.addEventListener('click', () => {
        const target = videoWrapper;
        if (!document.fullscreenElement) {
            if (target.requestFullscreen) {
                target.requestFullscreen();
            }
        } else {
            if (document.exitFullscreen) {
                document.exitFullscreen();
            }
        }
    });

    img.addEventListener('load', () => {
        loadingOverlay.style.display = 'none';
        if (isStreaming) {
            setStatus('online', 'Streaming berjalan');
        }
    });

    img.addEventListener('error', () => {
        loadingOverlay.style.display = 'none';
        if (isStreaming) {
            setStatus('offline', 'Gagal memuat stream, cek server/kamera');
        }
    });

    window.addEventListener('DOMContentLoaded', () => {
        // status awal saat halaman dibuka
        setStatus('online', 'Menghubungkan ke kamera...');
    });
})();


# config.py
# File konfigurasi utama untuk path

import os

# --- PATH KONFIGURASI UTAMA ---

# ❗ UBAH PATH INI SESUAI LOKASI FOLDER DATASET DI PROYEK LARAVEL ANDA ❗
# Pastikan path ini benar dan folder 'Dataset' sudah ada di dalamnya.
# Gunakan Raw String (r"...") untuk menghindari masalah backslash di Windows.
LARAVEL_PROJECT_PATH = r"D:\laragon\www\test03"
DATASET_SUBDIR = "storage/Dataset" # Subdirektori di dalam proyek Laravel

# Path absolut ke folder Dataset
DATASET_PATH = os.path.join(LARAVEL_PROJECT_PATH, DATASET_SUBDIR)

# Path ke folder embeddings (bisa tetap di proyek Python atau dipindah juga)
# Untuk saat ini, kita biarkan di proyek Python
EMB_DIR = "embeddings"

# Path ke file absensi (CSV atau bisa dihapus jika logging via DB)
CSV_LOG_PATH = r"D:/Semester 8/Capstong/TA2/absensi.csv"

# --- Konfigurasi Geolokasi ---
# Ganti dengan koordinat target Anda
#TARGET_LATITUDE = -6.9926
#TARGET_LONGITUDE = 110.4208
#ACCEPTABLE_RADIUS_METERS = 50

# --- Konfigurasi Database (jika digunakan) ---
DB_NAME = "qash_demo"
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root', # Ganti 'insertuserhere'
    'password': '', # Ganti 'insertpasswordhere'
    'database': DB_NAME
}

# --- Konfigurasi Lainnya ---
# Mode Logger ('CSV' atau 'MYSQL')
LOGGING_MODE = 'MYSQL' # Ganti ke 'MYSQL' jika database siap

# Thresholds
RECOGNITION_THRESHOLD_ABSENSI = 0.40 # 60% kemiripan untuk Absensi 1:1
RECOGNITION_THRESHOLD_REGISTER = 0.30 # 70% kemiripan untuk Cek Duplikasi Wajah
DETECTION_QUALITY_THRESHOLD_REGISTER = 0.70 # Kualitas gambar min 70% saat daftar
VALIDATE_POSE_ENABLED = False # Aktifkan/nonaktifkan validasi pose
POSE_THRESHOLD_SIDE = 30
POSE_THRESHOLD_UP_DOWN = 30

# --- Jangan ubah di bawah ini ---
MODEL_PATH = os.path.join(EMB_DIR, "knn_model.pkl")
NAMES_PATH = os.path.join(EMB_DIR, "names.pkl")

# Pastikan folder embeddings ada di proyek Python
os.makedirs(EMB_DIR, exist_ok=True)
# Pastikan folder Dataset target ada
try:
    os.makedirs(DATASET_PATH, exist_ok=True)
    print(f"✅ Memastikan folder Dataset ada di: {DATASET_PATH}")
except OSError as e:
    print(f"❌ GAGAL membuat/mengakses folder Dataset di: {DATASET_PATH}. Error: {e}")
    # Anda mungkin ingin keluar jika path dataset krusial tidak bisa diakses
    # import sys
    # sys.exit(1)

print(f"💡 Konfigurasi dimuat: Dataset di '{DATASET_PATH}', Embeddings di '{EMB_DIR}'")

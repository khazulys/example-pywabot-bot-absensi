import json
import os
from datetime import datetime

DATA_DIR = "data"
ABSENSI_FILE = os.path.join(DATA_DIR, "absensi.json")

def ensure_data_dir_exists():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def save_absensi(nama, lokasi, jarak, status):
    ensure_data_dir_exists()
    
    waktu_absen = datetime.now().isoformat()
    
    new_entry = {
        "nama": nama,
        "lokasi": lokasi,
        "waktu_absen": waktu_absen,
        "jarak": f"{jarak:.2f} meter",
        "status": status
    }
    
    data = []
    if os.path.exists(ABSENSI_FILE):
        with open(ABSENSI_FILE, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                pass

    data.append(new_entry)
    
    with open(ABSENSI_FILE, "w") as f:
        json.dump(data, f, indent=4)

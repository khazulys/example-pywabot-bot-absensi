# Contoh Bot WhatsApp pake PyWaBot

Halo! Pernah kepikiran bikin bot WhatsApp sendiri? Nah, proyek ini adalah contoh sederhana gimana caranya bikin bot pakai library `pywabot` di Python.

Bot ini punya beberapa fitur dasar, termasuk sistem absensi simpel yang ngecek lokasi kamu.

## Bot-nya Bisa Apa Aja Sih?

*   **Nyapa Pengguna:** Otomatis ngirim pesan sapaan ke pengguna baru.
*   **Nampilin Menu:** Kalau ada yang ngetik `.list`, bot bakal ngasih tau perintah apa aja yang ada.
*   **Ngirim Lelucon:** Iseng-iseng, bisa minta lelucon garing pake perintah `.kata`.
*   **Sistem Absensi:**
    *   Ketik `.absen` buat mulai.
    *   Bot bakal minta kamu kirim lokasi buat ngecek jarak.
    *   Kalau jaraknya deket, bot bakal minta foto selfie buat bukti.
    *   Data absen (nama, lokasi, dll.) bakal disimpen.

## Isi Foldernya Apa Aja?

```
/
├── bot.py              # File utama buat jalanin bot-nya
├── handlers/
│   └── handlers.py     # Logika buat ngerespon semua perintah ada di sini
├── utils/
│   ├── data_manager.py # Ngurusin cara nyimpen data absen
│   └── utils.py        # Fungsi-fungsi bantuan (kayak ngitung jarak, dll)
├── config/
│   └── config.json     # Tempat nyimpen settingan radius & link Google Maps
├── .env                # Simpen API key rahasia di sini
├── .gitignore          # Biar file-file rahasia nggak ke-upload ke Git
├── requirements.txt    # Daftar library Python yang dipake
└── README.md           # Penjelasan proyek ini
```

## Gimana Cara Mulainya?

1.  **Clone Dulu Proyek Ini:**
    ```bash
    git clone <url-proyek-ini>
    cd mybot
    ```

2.  **Install Library yang Dibutuhin:**
    Biar rapi, enaknya sih pake *virtual environment*.
    ```bash
    # Bikin virtual environment
    python -m venv venv
    # Aktifin (di Windows beda dikit ya)
    source venv/bin/activate
    # Install semua library dari requirements.txt
    pip install -r requirements.txt
    ```

3.  **Atur Konfigurasi:**
    *   **API Key:** Bikin file baru namanya `.env`, terus isi API key kamu di dalemnya kayak gini:
        ```
        API_KEY="isi_api_key_kamu_di_sini"
        ```
    *   **Lokasi & Radius:** Buka file `config/config.json`, terus ganti URL Google Maps dan radiusnya sesuai kebutuhan.
        ```json
        {
          "gmaps_url": "https://maps.app.goo.gl/lokasi_target_kamu",
          "radius": "100"
        }
        ```

## Cara Jalanin Bot-nya

Kalau semua udah siap, tinggal jalanin aja file `bot.py` dari terminal:
```bash
python bot.py
```

Nanti, kamu bakal diminta masukin nomor HP buat dapet kode pairing. Kalau udah berhasil, bot-nya langsung aktif dan siap nerima pesan.

### Daftar Perintah Bot

*   `.list`: Buat liat daftar perintah.
*   `.kata`: Minta kata-kata mutiara (yang kadang lucu).
*   `.absen`: Mulai proses absen.
*   `.cancel`: Batalin proses yang lagi jalan.

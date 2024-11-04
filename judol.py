import requests
import datetime

# Konfigurasi API
GOOGLE_API_KEY = ''  # Ganti dengan API Key Google Anda
GOOGLE_CSE_ID = ''           # Ganti dengan Custom Search Engine ID
TELEGRAM_BOT_TOKEN = ''  # Ganti dengan token bot Telegram Anda
TELEGRAM_CHAT_ID = ''      # Ganti dengan chat ID Telegram Anda

# Fungsi untuk melakukan dorking
def google_dork():
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": GOOGLE_API_KEY,
        "cx": GOOGLE_CSE_ID,
        "q": "site:*.go.id slot",
        "sort": "date:r:now-24h"  # Filter untuk 24 jam terakhir
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        results = data.get("items", [])
        websites = [item["link"] for item in results]
        return websites
    else:
        print(f"Error: {response.status_code}")
        return []

# Fungsi untuk mengirim notifikasi Telegram
def send_telegram_notification(websites):
    if not websites:
        print("Tidak ada hasil baru untuk dilaporkan.")
        return

    date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"Web Defacement Judi Online Terbaru\nTanggal & Waktu: {date_time}\n\nDaftar Website:\n" + "\n".join(websites)

    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }

    response = requests.post(telegram_url, json=payload)
    if response.status_code == 200:
        print("Notifikasi berhasil dikirim ke Telegram.")
    else:
        print(f"Error mengirim notifikasi: {response.status_code}")

# Eksekusi Dorking dan Kirim Notifikasi
websites = google_dork()
send_telegram_notification(websites)

import requests

# Fungsi untuk mengirim file menggunakan bot Telegram
def send_file(chat_id, file_path):
    token = "6113573987:AAEBBITXWP8u4cK84qKTItkdfPJYbbxz1e4"
    url = f"https://api.telegram.org/bot{token}/sendDocument"
    files = {"document": open(file_path, "rb")}
    data = {"chat_id": chat_id}
    response = requests.post(url, data=data, files=files)
    return response.json()

# Chat ID penerima (recipient)
recipient_chat_id = "5626056399"  # Ganti dengan chat ID penerima

# Path ke file Attendance.csv
file_path = "C:/Users/ThinkPad/Documents/Smart-Absensi-main/Attendance.csv"


# Kirim file
response = send_file(recipient_chat_id, file_path)

# Cek apakah file terkirim dengan sukses
if response.get("ok"):
    print("File terkirim dengan sukses!")
else:
    print("File gagal terkirim.")
    print("Respon dari server:", response)

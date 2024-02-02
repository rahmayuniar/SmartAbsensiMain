from pymongo import MongoClient 
import requests
import cv2, os, numpy as np
import tkinter as tk
from PIL import ImageTk, Image
from datetime import datetime

# Buat koneksi ke server MongoDB (pastikan MongoDB sudah berjalan)
client = MongoClient("mongodb+srv://distraokta:hawkeye161@cluster0.cybfqid.mongodb.net/?retryWrites=true&w=majority")
db_siswa = client.datasiswa
collection_siswa = db_siswa.siswa


def send_file(chat_id, file_path):
    token = "6113573987:AAEBBITXWP8u4cK84qKTItkdfPJYbbxz1e4"  # Ganti dengan token bot Telegram Anda
    url = f"https://api.telegram.org/bot{token}/sendDocument"
    files = {"document": open(file_path, "rb")}
    data = {"chat_id": chat_id}
    response = requests.post(url, data=data, files=files)
    return response.json()

def selesai1():
    intructions.config(text="Rekam Data Telah Selesai!")
def selesai2():
    intructions.config(text="Training Wajah Telah Selesai!")
def selesai3():
    intructions.config(text="Absensi Telah Dilakukan")
def rekamDataWajah():
    wajahDir = 'datawajah'
    cam = cv2.VideoCapture(0)
    cam.set(3, 640)
    cam.set(4, 480)
    faceDetector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    eyeDetector = cv2.CascadeClassifier('haarcascade_eye.xml')
    faceID = entry2.get()
    nama = entry1.get()
    nis = entry2.get()
    kelas = entry3.get()
    ambilData = 1
    while True:
        retV, frame = cam.read()
        abuabu = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceDetector.detectMultiScale(abuabu, 1.3, 5)
        for (x, y, w, h) in faces:
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
            namaFile = str(nis) +''+str(nama) + '' + str(kelas) +'_'+ str(ambilData) +'.jpg'
            cv2.imwrite(wajahDir + '/' + namaFile, frame)
            ambilData += 1
            roiabuabu = abuabu[y:y + h, x:x + w]
            roiwarna = frame[y:y + h, x:x + w]
            eyes = eyeDetector.detectMultiScale(roiabuabu)
            for (xe, ye, we, he) in eyes:
                cv2.rectangle(roiwarna, (xe, ye), (xe + we, ye + he), (0, 255, 255), 1)
        cv2.imshow('webcamku', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):  # jika menekan tombol q akan berhenti
            break
        elif ambilData > 30:
            break
    selesai1()
    cam.release()
    cv2.destroyAllWindows()  # untuk menghapus data yang sudah dibaca

def trainingWajah():
    wajahDir = 'datawajah'
    latihDir = 'latihwajah'

    def getImageLabel(path):
        imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
        faceSamples = []
        faceIDs = []
        for imagePath in imagePaths:
            PILimg = Image.open(imagePath).convert('L')
            imgNum = np.array(PILimg, 'uint8')
            faceID = int(os.path.split(imagePath)[-1].split('_')[0])
            faces = faceDetector.detectMultiScale(imgNum)
            for (x, y, w, h) in faces:
                faceSamples.append(imgNum[y:y + h, x:x + w])
                faceIDs.append(faceID)
            return faceSamples, faceIDs

    faceRecognizer = cv2.face.LBPHFaceRecognizer_create()
    faceDetector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    faces, IDs = getImageLabel(wajahDir)
    faceRecognizer.train(faces, np.array(IDs))
    # simpan
    faceRecognizer.write(latihDir + '/training.xml')
    selesai2()

def markAttendance(name):
    with open("Attendance.csv", 'r+') as f:
        namesDatalist = f.readlines()
        namelist = []
        yournis = entry2.get()
        yourclass = entry3.get()
        for line in namesDatalist:
            entry = line.split(',')
            namelist.append(entry[0])
        if name not in namelist:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{yourclass},{yournis},{dtString}')
            # Simpan data kehadiran ke MongoDB
            attendance_data = {
                "name": name,
                "class": yourclass,
                "nis": yournis,
                "timestamp": dtString
            }
            collection_siswa.insert_one(attendance_data)  # Menyimpan data kehadiran ke MongoDB


def absensiWajah():
    wajahDir = 'datawajah'
    latihDir = 'latihwajah'
    cam = cv2.VideoCapture(0)
    faceDetector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    faceRecognizer = cv2.face.LBPHFaceRecognizer_create()
    faceRecognizer.read(latihDir + '/training.xml')
    font = cv2.FONT_HERSHEY_SIMPLEX

    #id = 0
    yourname = entry1.get()
    names = []
    names.append(yourname)
    minWidth = 0.1 * cam.get(3)
    minHeight = 0.1 * cam.get(4)

    while True:
        retV, frame = cam.read()
        frame = cv2.flip(frame, 1)
        abuabu = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceDetector.detectMultiScale(abuabu, 1.2, 5, minSize=(round(minWidth), round(minHeight)), )
        for (x, y, w, h) in faces:
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0),2)
            id, confidence = faceRecognizer.predict(abuabu[y:y+h,x:x+w])
            if (confidence < 100):
                id = names[0]
                confidence = "  {0}%".format(round(150 - confidence))
            elif confidence < 50:
                id = names[0]
                confidence = "  {0}%".format(round(170 - confidence))

            elif confidence > 70:
                id = "Tidak Diketahui"
                confidence = "  {0}%".format(round(150 - confidence))

            cv2.putText(frame, str(id), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
            cv2.putText(frame, str(confidence), (x + 5, y + h + 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

        cv2.imshow('ABSENSI WAJAH', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):  # jika menekan tombol q akan berhenti
            break
    markAttendance(id)
    selesai3()
    cam.release()


    # Fungsi untuk mengirim kehadiran ke Telegram

    # Fungsi untuk mengirim kehadiran ke Telegram
def kirim_kehadiran_ke_telegram():
    # Path ke file CSV kehadiran
    file_path = "C:/Users/ThinkPad/Documents/Smart-Absensi-main/Attendance.csv"
    # Ganti dengan chat ID penerima di Telegram
    recipient_chat_id = "5626056399"
    # Mengirim file kehadiran ke Telegram
    response = send_file(recipient_chat_id, file_path)

    if response.get("ok"):
        print("File terkirim dengan sukses!")
    else:
        print("File gagal terkirim.")
        print("Respon dari server:", response)


# GUI
root = tk.Tk()
# mengatur canvas (window tkinter)
canvas = tk.Canvas(root, width=582.15, height=324.07)
canvas.grid(columnspan=10, rowspan=2)
canvas.configure(bg="#87CEEB")
# judul
judul = tk.Label(root, text="Face Attendance - Smart Absensi", font=("Roboto",20),bg="#87CEEB", fg="white")
canvas.create_window(300, 80, window=judul)
#credit
made = tk.Label(root, text="SMART ABSENSI - SMART CLASSROOM", font=("Times New Roman",13), bg="#87CEEB",fg="white")
canvas.create_window(300, 20, window=made)
# for entry data nama
entry1 = tk.Entry (root, font="Roboto")
canvas.create_window(350, 170, height=25, width=300, window=entry1)
label1 = tk.Label(root, text="Nama", font="Roboto", fg="white", bg="#87CEEB")
canvas.create_window(115,170, window=label1)
# for entry data nis
entry2 = tk.Entry (root, font="Roboto")
canvas.create_window(350, 210, height=25, width=300, window=entry2)
label2 = tk.Label(root, text="NIS", font="Roboto", fg="white", bg="#87CEEB")
canvas.create_window(107, 210, window=label2)
# for entry data kelas
entry3 = tk.Entry (root, font="Roboto")
canvas.create_window(350, 250, height=25, width=300, window=entry3)
label3 = tk.Label(root, text="Kelas", font="Roboto", fg="white", bg="#87CEEB")
canvas.create_window(114, 250, window=label3)

global intructions

# tombol untuk rekam data wajah
intructions = tk.Label(root, text="Welcome Students!", font=("Roboto",15),fg="white",bg="#87CEEB")
canvas.create_window(300, 300, window=intructions)
Rekam_text = tk.StringVar()
Rekam_btn = tk.Button(root, textvariable=Rekam_text, font="Roboto", bg="#87CEEB", fg="white", height=1, width=15,command=rekamDataWajah)
Rekam_text.set("Take Images")
Rekam_btn.grid(column=0, row=2)

# tombol untuk training wajah
Rekam_text1 = tk.StringVar()
Rekam_btn1 = tk.Button(root, textvariable=Rekam_text1, font="Roboto", bg="#87CEEB", fg="white", height=1, width=15,command=trainingWajah)
Rekam_text1.set("Training")
Rekam_btn1.grid(column=1, row=2)

# tombol absensi dengan wajah
Rekam_text2 = tk.StringVar()
Rekam_btn2 = tk.Button(root, textvariable=Rekam_text2, font="Roboto", bg="#87CEEB", fg="white", height=1, width=20, command=absensiWajah)
Rekam_text2.set("Automatic Attendance")
Rekam_btn2.grid(column=2, row=2)

root.mainloop()

# Setelah GUI ditutup, panggil fungsi untuk mengirim kehadiran ke Telegram
kirim_kehadiran_ke_telegram()
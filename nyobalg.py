import tkinter as tk

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
import cv2
import cv2, os, numpy as np
from PIL import ImageTk, Image
from datetime import datetime
import tkinter as tk

# GUI
root = tk.Tk()
# mengatur canvas (window tkinter)
canvas = tk.Canvas(root, width=582.15, height=324.07)
canvas.grid(columnspan=10, rowspan=2)
canvas.configure(bg="#87CEEB")

            if (confidence > 70):
                id = names[0]
                confidence = "  {0}%".format(round(150 - confidence))
            elif (confidence < 30):
                id = names[0]
                confidence = "  {0}%".format(round(170 - confidence))

            elif confidence > 70:
                id = "Tidak Diketahui"
                confidence = "  {0}%".format(round(150 - confidence))


            if (confidence < 100):
                id = names[0]
                confidence = "  {0}%".format(round(150 - confidence))
            elif (confidence < 50):
                id = names[0]
                confidence = "  {0}%".format(round(170 - confidence))

            elif confidence > 70:
                id = "Tidak Diketahui"        
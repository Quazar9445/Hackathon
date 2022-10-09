# Import Tkinter All Items
from numbers import Number
from tkinter import Tk, Label, Menu, Toplevel, Button, Image

# Specifically for choosing color (Customization)
from tkinter import colorchooser

# Detects Current Time
import datetime

# OpenCV Detection
import cv2
import numpy as np

from _thread import *



# Setup Window
root = Tk()
root.title('SafetyFirst Camera Notification App')
root.geometry('1000x800')
root.iconbitmap('ico.ico')

# Customization
custo_menu = Menu(root)
root.config(menu=custo_menu)
bg = ""

def choose_wincolor(new_window):
    selected_color = colorchooser.askcolor(title="Choose BG Color")[1]
    root['bg'] = str(selected_color)
    new_window.destroy()
    

def make_window():
    new_window = Toplevel()
    new_window.title("Customize")
    new_window.geometry("400x300")
    ask_color = Button(new_window, text="Choose BG Color", command=lambda: choose_wincolor(new_window)).pack()
    


customize_sector = Menu(custo_menu, tearoff=False)
custo_menu.add_cascade(label="Options", menu=customize_sector)
customize_sector.add_command(label="Customize", command=make_window)
customize_sector.add_separator()
customize_sector.add_command(label="Exit", command=root.quit)

camera_num = 0

def set_camera(number):
    global camera_num
    camera_num = number
    print(camera_num)


# Configure Cameras
configure_camerazero = Button(root, text='Computer Camera', command=lambda: set_camera(0)).pack()
configure_cameraone = Button(root, text="Other Camera 1", command=lambda: set_camera(1)).pack()
configure_cameratwo = Button(root, text="Other Camera 2", command=lambda: set_camera(2)).pack()
configure_camerathree = Button(root, text="Other Camera 3", command=lambda: set_camera(3)).pack()
configure_camerafour = Button(root, text="Other Camera 4", command=lambda: set_camera(4)).pack()


# Keep Running Window
root.mainloop()

#Captures Video and stores in a variable. The Params in this function take in the external camera number
cap = cv2.VideoCapture(camera_num)



#Takes each indivdual frame 
ret, frame1 = cap.read()
ret, frame2 = cap.read()





# While Camera is recording
while cap.isOpened():
    # Finds the absolute difference between frame 1 and 2
    diff = cv2.absdiff(frame1, frame2)
    # Converts the image from cv2 Blue Green Red coloring scale to Grayscale
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _= cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        
        if cv2.contourArea(contour) < 5000:
            continue
        cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0) , 2)
        cv2.putText(frame1, "Status: {}".format("Currently Moving"), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

        
    
    cv2.imshow('feed', frame1)
    frame1 = frame2
    ret, frame2 = cap.read()
    
    if cv2.waitKey(1) & 0xFf == 27:
        break
        
cv2.destroyAllWindows()
cap.release()

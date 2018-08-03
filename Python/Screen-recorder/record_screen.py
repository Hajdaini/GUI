"""
@Author : AJDAINI Hatim
@GitHub : https://github.com/Hajdaini
"""

import numpy as np
import cv2
import time, datetime
from tkinter import *
from sys import platform
if platform == "linux2":
    import pyscreenshot as ImageGrab # pip3 install pyscreenshot
else:
    from PIL import ImageGrab

WIDTH = 300
HEIGHT = 300
start_record = False
close_all = False
count_start_time_once = True
fps = 25


def hide_widget():
    global label_fps
    global input_fps

    label_fps.place_forget()
    input_fps.place_forget()


def record_toggle():
    global start_record
    global close_all
    global button_record

    if start_record:
        window.destroy()
        close_all = True
    else:
        hide_widget()
        button_record['text'] = 'SAVE AND QUIT'
        start_record = True


def on_closing():
    global start_record
    global close_all
    close_all = True
    start_record = True


def window_position(window, width, height):
    screen_width = int(window.winfo_screenwidth())
    screen_height = int(window.winfo_screenheight())
    window_width = width
    window_height = height
    window_x = (screen_width // 2) - (window_width // 2)
    window_y = (screen_height // 2) - (window_height // 2)
    return '{}x{}+{}+{}'.format(window_width, window_height, window_x, window_y)


# Windows configuration
window = Tk()
window.title('AJDAINI Recorder')
window.geometry(window_position(window, WIDTH, HEIGHT))
window.configure(bg='#0B132B')
window.protocol("WM_DELETE_WINDOW", on_closing)
# Widgets configuration
button_record = Button(window, text='Record', font='Arial 12', bg='#1C2541', fg='white', highlightcolor='#3A506B', activebackground='#3A506B', command=record_toggle)
label_timer = Label(window, text='No Record', font='Arial 14 bold', bg='#0B132B', fg='#FF6958')
label_fps = Label(window, text='speed (fps) ', font='Arial 12', bg='#0B132B', fg='white')
input_fps = Entry(window, font='Arial 12 bold', width=8, fg='#007EA7', border=2, justify='center')
input_fps.insert(0, str(fps))
label_credit = Label(window, text='Created by AJDAINI Hatim', font='Arial 12 italic', bg='#0B132B', fg='#3A506B')

# Widgets position
label_fps.place(relx=0.5, rely=0.1, anchor=CENTER)
input_fps.place(relx=0.5, rely=0.2, anchor=CENTER)
button_record.place(relx=0.5, rely=0.4, anchor=CENTER)
label_timer.place(relx=0.5, rely=0.53, anchor=CENTER)
label_credit.place(relx=0.5, rely=0.63, anchor=CENTER)

# Video recording
screen_width = int(window.winfo_screenwidth())
screen_height = int(window.winfo_screenheight())
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('ouput.avi', fourcc, int(input_fps.get()), (screen_width,  screen_height))
while True:
    if close_all:
        break
    try:
        if start_record:
            if count_start_time_once:
                out = cv2.VideoWriter('ouput.avi', fourcc, int(input_fps.get()), (screen_width, screen_height))
                count_start_time_once = False
                start_time = time.time()
            label_timer['text'] = str(datetime.timedelta(seconds=int(time.time() -start_time)))
        window.update()
    except:
        pass
    if start_record:
        image = ImageGrab.grab()
        image_np = np.array(image)
        frame = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
        out.write(frame)

out.release()
cv2.destroyAllWindows()

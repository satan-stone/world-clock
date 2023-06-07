#!/usr/bin/env python3

from tkinter import *
from tkinter.ttk import *
import time
import requests
import shutil
from PIL import ImageTk, Image
import os
import json
import threading

#read config
cf = open('config.json', 'r')
config = json.load(cf)

# becomes index 'i' value for creating elements
items_in_config = len(config['places']) 

# we use this to create the Frame() objects along with create_frame_vars()
frame_vars = vars() 

# used to create a consistent variable name for Frame() based on country code
def create_frame_vars(country_code, type): 
    if type == 'flag':
        a = country_code + '_flag_lbl'
    elif type == 'clock':
        a = country_code + '_clock_lbl'
    return a

# fetches flag uses the 'cc' value from the config. Must be lowercase and valid country code
def fetch_flag(country_code): 
    if not country_code == 'utc':
        url = 'https://flagcdn.com/h120/' + country_code + '.png'
        flag_file = country_code + '.png'
        flag = requests.get(url, stream=True)
        with open(flag_file, 'wb') as out_file:
            shutil.copyfileobj(flag.raw, out_file)
        del flag
    else:
        pass

# lets load the flags into the UI
def load_flags(country_code, image_file, i): 
    load_image = Image.open(image_file)
    flag_image = ImageTk.PhotoImage(load_image)
    flag_frame = create_frame_vars(country_code, 'flag')
    frame_vars[flag_frame] = Label(frame, image=flag_image)
    frame_vars[flag_frame].grid(column=i, row=1)
    frame_vars[flag_frame].image = flag_image

# load clocks and keep them updating
def get_time(locale, country_code, i): 
    os.environ['TZ'] = locale
    time.tzset()
    cur_time = time.strftime('%H:%M:%S')
    clock_frame = create_frame_vars(country_code, 'clock')
    frame_vars[clock_frame] = Label(frame,font=('arial', 40, 'bold') )
    frame_vars[clock_frame].grid(column=i, row=2)
    frame_vars[clock_frame].config(text=cur_time, )
    root.update_idletasks()
    x = threading.Thread(target=get_time, args=(locale, country_code, i))
    x.start()
    #root.after(1000, get_time(locale, country_code, i))

# create the main window    
root = Tk()
root.title('World Clock')
frame = Frame(root, borderwidth=5)
frame.grid(column=0, row=0)

# read in config and create UI objects
for i in range(items_in_config):
    locale = config['places'][i]['olson_country']
    country_code = config['places'][i]['cc']
    fetch_flag(country_code)
    image_file = country_code + '.png'
    load_flags(country_code, image_file, i)
    get_time(locale, country_code, i)

root.mainloop()

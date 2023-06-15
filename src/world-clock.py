#!/usr/bin/env python3

from tkinter import *
from tkinter.ttk import *
import time
import requests
import shutil
from PIL import ImageTk, Image
import os
import json


# read config
cf = open('config.json', 'r')
config = json.load(cf)


# becomes index 'i' value for creating elements
items_in_config = len(config['places'])

# we use this to create the Frame() objects along with create_label_vars()
frame_vars = vars()


# used to create a consistent variable name for Frame() based on country code
def create_label_vars(country_code, type):
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
def load_flags(country_code, i):
    image_file = country_code + '.png'
    load_image = Image.open(image_file)
    flag_image = ImageTk.PhotoImage(load_image)
    flag_label = create_label_vars(country_code, 'flag')
    frame_vars[flag_label] = Label(frame, borderwidth=5, image=flag_image)
    frame_vars[flag_label].grid(column=i, row=1)
    frame_vars[flag_label].image = flag_image


# load clocks and keep them updating
def get_time(locale, country_code, i):
    os.environ['TZ'] = locale
    time.tzset()
    cur_time = time.strftime('%a %H:%M')
    clock_label = create_label_vars(country_code, 'clock')
    frame_vars[clock_label] = Label(frame, borderwidth=5, font=('arial', 36, 'bold'))
    frame_vars[clock_label].grid(column=i, row=2)
    frame_vars[clock_label].config(text=cur_time)
    frame_vars[clock_label].update_idletasks()
    frame_vars[clock_label].update()


# attempt to update clocks
def update_time():
    while True:
        time.sleep(.6)
        for i in range(items_in_config):
            locale = config['places'][i]['time_zone']
            country_code = config['places'][i]['cc']
            os.environ['TZ'] = locale
            time.tzset()
            cur_time = time.strftime('%a %H:%M')
            clock_label = create_label_vars(country_code, 'clock')
            frame_vars[clock_label].config(text=cur_time)
            frame_vars[clock_label].update_idletasks()
            frame_vars[clock_label].update()
            

# create the main window    
root = Tk()
root.title('World Clock')
frame = Frame(root, borderwidth=5)
frame.grid(column=0, row=0)


# read in config and create UI objects
for i in range(items_in_config):
    print(config['places'][i])
    locale = config['places'][i]['time_zone']
    country_code = config['places'][i]['cc']
    fetch_flag(country_code)
    load_flags(country_code, i)
    get_time(locale, country_code, i)


update_time()

import numpy as np
import cv2
import sys
from tkinter import filedialog
from tkinter import *
import os
import json

root = Tk()
root.withdraw()
folder_selected = filedialog.askdirectory()
dictColors = dict()
    
for file in os.listdir(folder_selected):
    filename = os.fsdecode(file)
    if filename.endswith(".png"): 
        path = os.path.join(folder_selected, filename)
        img = cv2.imread(path)
        # calculate the average color of each row of our image
        avg_color_per_row = np.average(img, axis=0)
        # calculate the averages of our rows
        avg_colors = np.average(avg_color_per_row, axis=0)
        # so, convert that array to integers
        int_averages = np.array(avg_colors, dtype=np.uint8)
        dictColors[path] = int_averages.tolist()
        continue
    else:
        continue

json_object = json.dumps(dictColors, indent = 4) 

with open('clrs.json', 'w', encoding='utf-8') as f:
    json.dump(json_object, f, ensure_ascii=False, indent=4)

print('Done!')

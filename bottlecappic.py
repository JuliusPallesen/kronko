import enum
import numpy as np
import cv2
import sys
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import json
import addImg
import test

SIZE = 26

height = 0
width = 0
heightmm = 0
widthmm = 0
heightkk = 0
widthkk = 0
circlesizepx = 0.0
ratio = 0.0

def make_slid(a_min:int, a_max:int, curr:int, slider_id:str, root_win_name:str, on_change_callback=lambda x: x):
	cv2.createTrackbar(slider_id, root_win_name, a_min, a_max, on_change_callback)
	cv2.setTrackbarPos(slider_id, root_win_name, curr)
	return slider_id

def getslid(id, root_wind:str):
	try:
		result = cv2.getTrackbarPos(id, root_wind)
		return result
	except Exception as e:
		print(f'Error in getting slider value - {str(e)}')
		return None

def initSizes(inpt):
    global ratio
    global widthmm
    global widthkk
    global heightmm
    global heightkk
    global circlesizepx

    widthkk = inpt // SIZE
    widthmm = widthkk * SIZE

    heightmm = int(widthmm * ratio)
    heightkk = heightmm // SIZE
    heightmm = heightkk * SIZE

    circlesizepx = int(width / (inpt / SIZE))

    widthkk = max(widthkk,width // circlesizepx)
    heightkk = max(heightkk,height // circlesizepx)

    print(str(heightmm) + 'mm x ' + str(widthmm)+ 'mm')
    print(str(heightkk) + ' kronkorken x ' + str(widthkk)+ ' kronkorken')
    print('circlesize in px: ' + str(circlesizepx))

def genCircles(img):
    #generate circles where the bottlecaps will be placed
    with open('./clrs.json') as json_file:
        clrs = json.load(json_file)

    h, w, _ = img.shape
    new = np.zeros((h,w,3), np.uint8)

    

    for y in range(heightkk):
        for x in range(widthkk) :
            mask = np.zeros((height,width), np.uint8)
            xpos = (x * circlesizepx) + circlesizepx // 2
            ypos = (y * circlesizepx) + circlesizepx // 2

            cv2.circle(mask,
                        (xpos,ypos),
                        circlesizepx // 2,
                        (255,255,255),
                        thickness=-1)

            m_val = np.array(cv2.mean(img,mask)[::1])

            nearest = ''
            min = 99999

            for bottleCap in clrs:
                #bc reads key 3 row array from json converts it to float array and  appends a 0
                bc = np.append(np.asarray(clrs[bottleCap], dtype = np.float64),255)
                #find the minimal color vector distance
                dist = np.linalg.norm(m_val-bc)
                if min > dist:
                    min = dist
                    nearest = bottleCap

            new = addImg.performAdd(new, nearest, xpos, ypos, mask, circlesizepx)
    return new

def setslid(id_:str, value:int, root_wind:str):
	cv2.setTrackbarPos(id_, root_wind, value)

def openImg():
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
    img = cv2.imread(filename)

    return img

def main():
    global ratio
    global width
    global height

    root_name = 'BottleCapPics'
    cv2.namedWindow(root_name)

    img = openImg()

    img2 = img.copy()
    
    height, width = img.shape[:2]
    ratio = height / width
    
    sliders = [
        make_slid(0,2000,1000, 'width', root_name)
    ]
    
    while True:
        cv2.imshow(root_name, img2)

        code = cv2.waitKey(1)
        
        #quit
        if code == ord('q') or code == 27:
            break
        
        #original
        if code == ord('o'):
            img2 = img.copy()

        #read
        if code == ord('r'):
            img = openImg()
            img2 = img.copy()

        #make
        if code == 32 or code == ord('w'):
            img2 = img.copy()
            w = int(getslid('width',root_wind=root_name))
            initSizes(w)
            img2 = genCircles(img2)

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
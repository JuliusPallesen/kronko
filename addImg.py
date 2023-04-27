from cv2 import imshow
import numpy as np
import cv2 as cv
import sys
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import json
from PIL import Image
from bottlecappic import circlesizepx 

def openImg():
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
    img = cv.imread(filename)
    return img

def overlay_image_alpha(img, img_overlay, x, y, alpha_mask):
    """Overlay `img_overlay` onto `img` at (x, y) and blend using `alpha_mask`.

    `alpha_mask` must have same HxW as `img_overlay` and values in range [0, 1].
    """
    # Image ranges
    y1, y2 = max(0, y), min(img.shape[0], y + img_overlay.shape[0])
    x1, x2 = max(0, x), min(img.shape[1], x + img_overlay.shape[1])

    # Overlay ranges
    y1o, y2o = max(0, -y), min(img_overlay.shape[0], img.shape[0] - y)
    x1o, x2o = max(0, -x), min(img_overlay.shape[1], img.shape[1] - x)

    # Exit if nothing to do
    if y1 >= y2 or x1 >= x2 or y1o >= y2o or x1o >= x2o:
        return

    # Blend overlay within the determined ranges
    img_crop = img[y1:y2, x1:x2]
    img_overlay_crop = img_overlay[y1o:y2o, x1o:x2o]
    alpha = alpha_mask[y1o:y2o, x1o:x2o, np.newaxis]
    alpha_inv = 1.0 - alpha

    img_crop[:] = alpha * img_overlay_crop + alpha_inv * img_crop

    return img_crop

def combine ():
    # Load two images
    img1 = openImg()
    img2 = openImg()

    # I want to put logo on top-left corner, So I create a ROI
    rows,cols,channels = img2.shape
    roi = img1[0:rows, 0:cols]

    # Now create a mask of logo and create its inverse mask also
    img2gray = cv.cvtColor(img2,cv.COLOR_BGR2GRAY)
    ret, mask = cv.threshold(img2gray, 10, 255, cv.THRESH_BINARY)
    mask_inv = cv.bitwise_not(mask)

    # Now black-out the area of logo in ROI
    img1_bg = cv.bitwise_and(roi,roi,mask = mask_inv)

    # Take only region of logo from logo image.
    img2_fg = cv.bitwise_and(img2,img2,mask = mask)

    # Put logo in ROI and modify the main image
    dst = cv.add(img1_bg,img2_fg)
    img1[0:rows, 0:cols ] = dst
    cv.imshow('res',img1)
    cv.waitKey(0)

def performAdd(img, overlay, x, y, alpha_mask, size):
    # Prepare inputs
    img_overlay_rgba = np.array(Image.open(overlay))
    img_overlay_rgba = cv.resize(img_overlay_rgba, dsize=(size,size))
    # Perform blending
    alpha_mask = img_overlay_rgba[:, :, 3] / 255.0
    img_result = img[:, :, :3].copy()
    img_overlay = img_overlay_rgba[:, :, :3]

    overlay_image_alpha(img_result, img_overlay, x, y, alpha_mask)

    return img_result
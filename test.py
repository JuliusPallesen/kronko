import cv2
def testAddImg(imgL, imgS, x_offset, y_offset):
    s_img = imgS

    y1, y2 = y_offset, y_offset + s_img.shape[0]
    x1, x2 = x_offset, x_offset + s_img.shape[1]

    alpha_s = s_img[:, :, 3] / 255.0
    alpha_l = 1.0 - alpha_s

    for c in range(0, 3):
        imgL[y1:y2, x1:x2, c] = (alpha_s * s_img[:, :, c] +
                                alpha_l * imgL[y1:y2, x1:x2, c])
    
    return imgL
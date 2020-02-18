import cv2
import numpy as np
import os
from os.path import isdir, exists, join


# file path
rootDir = os.getcwd()
imgDir = join(rootDir, "img")
if exists(imgDir):
    print("Dir exists")
else:
    os.mkdir(imgDir)

# masked instance
imgMaskInstanceSrc = join(imgDir, "fixed_mask_4.png")
print(imgMaskInstanceSrc)

if exists(imgMaskInstanceSrc):
    print("imgMaskInstanceSrc exists")
    imgMaskInstance = cv2.imread(imgMaskInstanceSrc)
else:
    print("No such imgMaskInstanceSrc")
# 이미지 읽어서 그레이스케일 변환, 바이너리 스케일 변환
imgMaskInstanceGray = cv2.cvtColor(imgMaskInstance, cv2.COLOR_BGR2GRAY)
# binary threshold
ret, th = cv2.threshold(imgMaskInstanceGray, 200, 255, cv2.THRESH_BINARY)


contours, hierarchy = cv2.findContours(th, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
print("num of contours: {}".format(len(contours)))

cal_ = 1.2   # I wanted to show an area slightly larger than my min rectangle set this to one if you don't
img_box = cv2.cvtColor(imgMaskInstanceGray.copy(), cv2.COLOR_GRAY2BGR)
for cnt in contours:
    rect = cv2.minAreaRect(cnt)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    cv2.drawContours(img_box, [box], 0, (0, 255, 0), 2) # this was mostly for debugging you may omit

    W = rect[1][0]
    H = rect[1][1]

    Xs = [i[0] for i in box]
    Ys = [i[1] for i in box]
    x1 = min(Xs)
    x2 = max(Xs)
    y1 = min(Ys)
    y2 = max(Ys)

    rotated = False
    angle = rect[2]

    if angle < -45:
        angle += 90
        rotated = True

    center = (int((x1+x2)/2), int((y1+y2)/2))
    size = (int(cal_ * (x2 - x1)), int(cal_ * (y2 - y1)))
    cv2.circle(img_box, center, 10, (255, 0, 0), -1) #again this was mostly for debugging purposes

    M = cv2.getRotationMatrix2D((size[0]/2, size[1]/2), angle, 1.0)

    cropped = cv2.getRectSubPix(img_box, size, center)
    cropped = cv2.warpAffine(cropped, M, size)

    croppedW = W if not rotated else H
    croppedH = H if not rotated else W

    croppedRotated = cv2.getRectSubPix(cropped, (int(croppedW * cal_), int(croppedH * cal_)), (size[0] / 2, size[1] / 2))
    cv2.imshow('cropped rotated', croppedRotated)
    cv2.waitKey(0)
    cv2.destroyWindow('cropped rotated')

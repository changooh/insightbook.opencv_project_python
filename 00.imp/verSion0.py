import cv2
import numpy as np
import os
from os.path import isdir,exists,join


rootDir = os.getcwd()

imgDir = join(rootDir,"img")

if exists(imgDir):
    os.mkdir(imgDir)

# fixed rbg
img_fix = "../img/imp_image/data/crop_image_0.png"
# img_fix = "../img/imp_image/sample01/fixed_raw.jpg"
img0 = cv2.imread(img_fix)

# fixed depth map
img9 = cv2.imread('../img/imp_image/data/crop_depth_0.png', -1)
# img9 = cv2.imread('../img/imp_image/sample01/depth_fixed_raw.png', -1)

# masked instance
# img_src03 = '../img/imp_image/sample01/fixed_mask_1.png'
# img_src03 = '../img/imp_image/01_17_16_29_34_fixed_mask_0.png'
img_src03 = '../img/imp_image/data/crop_image_1_2.png'

# 이미지 읽어서 그레이스케일 변환, 바이너리 스케일 변환
img = cv2.imread(img_src03)
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# binary threshold
ret, th = cv2.threshold(img_gray, 200, 255, cv2.THRESH_BINARY)
im, contours, hr = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contr = contours[0]
# inner coordinate
x, y, w, h = cv2.boundingRect(contr)

# # rotate rectangle - center (x,y), (width, height), angle of rotation
# rect = cv2.minAreaRect(contr)
# box = cv2.boxPoints(rect)
# box = np.int0(box)
# cv2.drawContours(img, [box], 0, (0, 255, 0), 1)

# draw outer bounding box (blue)
# px 확대
px = 5
x_outer01 = x - px
x_outer02 = x + w + px
y_outer01 = y - px
y_outer02 = y + h + px
# print outer coordinates 1270 523 1369 626
print("outer coordinates: ", x_outer01, y_outer01, x_outer02, y_outer02)
# draw rectangle
# cv2.rectangle(img, (x_outer01, y_outer01), (x_outer02, y_outer02), (255, 0, 0), 1)

# instance mask roi 지정
roi = img[y_outer01:y_outer02, x_outer01:x_outer02]
imgMaskGray = roi.copy()  # roi array 복제 ---①
# cv2.imwrite('../img/imp_image/sample01/result_mask_1.png', imgMaskGray)
cv2.imwrite('../img/imp_image/data/result_mask_2.png', imgMaskGray)

# raw image roi 지정 # print(roi0.shape)
roi0 = img0[y_outer01:y_outer02, x_outer01:x_outer02]
# roi array copy
imgRgb = roi0.copy()
cv2.imwrite('../img/imp_image/data/result_rbg_2.png', imgRgb)

# instance depth roi
roi = img9[y_outer01:y_outer02, x_outer01:x_outer02]  # depth roi 지정
img3 = roi.copy()  # roi array 복제
# cv2.imwrite('../img/imp_image/sample01/result_depth_60.png', img*60)

#  정규화
img_norm1 = cv2.normalize(img3, None, 255, 255 * 255, cv2.NORM_MINMAX)
# img_norm1 = cv2.normalize(img3, None, 1, 50, cv2.NORM_MINMAX)
# img_norm1= cv2.normalize(img3, None, 1, 255, cv2.NORM_MINMAX)

# median 블러 API
imgDepth = cv2.medianBlur(img_norm1, 5)

# 결과 image save
# merged = np.hstack((img_norm2, blur, blur2))
cv2.imwrite('../img/imp_image/data/result_norm_2.png', imgDepth)
# cv2.imwrite('../img/imp_image/img_norm2_3.png', img_norm2)
# cv2.imwrite('../img/imp_image/img_media_2.png', blur)

# Mask area coordinates
maskIndices = np.where(imgMaskGray == [255])
# coordinates list [0] - x axis - height, [1] -y axis - width
maskCoordinates = np.array(list(zip(maskIndices[0], maskIndices[1])))

# unMask area coordinates
unMaskIndices = np.where(imgMaskGray != [255])
# coordinates list [0] - x axis - height, [1] -y axis - width
unMaskCoordinates = np.array(list(zip(unMaskIndices[0], unMaskIndices[1])))

# Get each depth value from maskCoordinates
maskColList = []
newMaskArray = np.zeros((maskCoordinates.shape[0], maskCoordinates.shape[1] + 1), dtype=int)
# newMaskArray = np.zeros((5, 3))
# newMaskArray[:, : -1] = maskCoordinates[5, :]
newMaskArray[:, : -1] = maskCoordinates
# print(newMaskArray)
breakPoint = 100000
for i, xy in enumerate(maskCoordinates):
    if i == breakPoint:
        break
    else:
        depthValue = imgDepth[xy[0], xy[1]]
        maskColList.append(depthValue)

# print(newColList)
newMaskArray[:, -1] = maskColList
# print(newMaskArray)

# # Get max, min, median values
print('---Masked---')
print("mean: %d" % np.mean(maskColList))
print("std: %d" % np.std(maskColList))
print("median: %d" % np.median(maskColList))
print("min: %d" % np.min(maskColList))
print("max: %d" % np.max(maskColList))

# Get each depth value from unMaskCoordinates
unMaskColList = []
newUnMaskArray = np.zeros((unMaskCoordinates.shape[0], unMaskCoordinates.shape[1] + 1), dtype=int)
# newMaskArray = np.zeros((5, 3))
# newMaskArray[:, : -1] = maskCoordinates[5, :]
newUnMaskArray[:, : -1] = unMaskCoordinates
# print(newMaskArray)
breakPoint = 100000
for i, xy in enumerate(unMaskCoordinates):
    if i == breakPoint:
        break
    else:
        depthValue = imgDepth[xy[0], xy[1]]
        unMaskColList.append(depthValue)

# print(newColList)
newUnMaskArray[:, -1] = unMaskColList
# print(newMaskArray)
# # Get max, min, median values
print('---unMasked---')
print("mean: %d" % np.mean(unMaskColList))
print("std: %d" % np.std(unMaskColList))
print("median: %d" % np.median(unMaskColList))
print("min: %d" % np.min(unMaskColList))
print("max: %d" % np.max(unMaskColList))

# instance 중앙값보다 같거나 높은 위치의 fix rate
medianValue = np.median(maskColList)
# medianValue = medianValue + 10.0
# boolMedian = np.array(unMaskColList) <= medianValue
boolMedian = np.array(unMaskColList) > medianValue
# boolMedian = unMaskColList <= np.std(unMaskColList)
# print(boolMedian)
cntTrue = np.sum(boolMedian)
rateMedian = cntTrue / len(unMaskColList)
print('median, cntTrue, rateMedian: ', np.median(maskColList), cntTrue, rateMedian)

#  visualization start
viewDepth = cv2.cvtColor(imgDepth, cv2.COLOR_GRAY2BGR)
for i, t in enumerate(boolMedian):
    if t:
        x, y = unMaskCoordinates[i, :]
        viewDepth[x, y] = [0, 255, 0]
        imgRgb[x, y] = [0, 255, 0]

        # break
    else:
        x, y = unMaskCoordinates[i, :]
        viewDepth[x, y] = [0, 0, 255]
        imgRgb[x, y] = [0, 0, 255]

# cv2.imwrite('../img/imp_image/sample01/result_detect_1.png', imgDepth)
# cv2.imwrite('../img/imp_image/sample01/result_rgb_detect_1.png', imgRgb)
cv2.imwrite('../img/imp_image/data/result_detect_2.png', viewDepth)
cv2.imwrite('../img/imp_image/data/result_rgb_detect_2.png', imgRgb)
# visualization end

print('end')

import cv2
import numpy as np
import os
from os.path import isdir, exists, join

# saved file names
saveVisualRgbPng = "result_rbg_3.png"
saveVisualDepthPng = "result_detect_3.png"
saveInstanceNormPng = "result_norm_3.png"
saveRgbPng = "result_rbg_3.png"
saveMaskedInstancePng = "result_mask_3.png"

# file path
rootDir = os.getcwd()
imgDir = join(rootDir, "img")
if exists(imgDir):
    print("Dir exists")
else:
    os.mkdir(imgDir)

# fixed rbg
imgFixRbgSrc = join(imgDir, "fixed_raw.jpg")
if exists(imgFixRbgSrc):
    print("imgFix exists")
    imgRgbFixed = cv2.imread(imgFixRbgSrc)
    # img_fix = "../img/imp_image/sample01/fixed_raw.jpg"
else:
    print("No such imgFix")

# fixed depth map
imgFixDepthSrc = join(imgDir, "depth_fixed_raw.png")
if exists(imgFixDepthSrc):
    print("imgFixDepthSrc exists")
    imgDepthFixed = cv2.imread(imgFixDepthSrc, -1)
else:
    print("No such imgFixDepthSrc")

# masked instance
imgMaskInstanceSrc = join(imgDir, "fixed_mask_3.png")
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

# get contours
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
imgMaskInstanceRoi = th[y_outer01:y_outer02, x_outer01:x_outer02]
imgMaskInstanceRet = imgMaskInstanceRoi.copy()  # roi array 복제 ---①
saveMaskedInstancePath = join(imgDir, saveMaskedInstancePng)
# cv2.imwrite('../img/imp_image/sample01/result_mask_1.png', imgMaskGray)
cv2.imwrite(saveMaskedInstancePath, imgMaskInstanceRet)

# raw image roi 지정
# print(roi0.shape)
imgRgbFixedRoi = imgRgbFixed[y_outer01:y_outer02, x_outer01:x_outer02]
# roi array copy
imgRgbFixedRet = imgRgbFixedRoi.copy()

saveRgbFixedRetPath = join(imgDir, saveRgbPng)
cv2.imwrite(saveRgbFixedRetPath, imgRgbFixedRet)

# instance depth roi
imgDepthInstanceRoi = imgDepthFixed[y_outer01:y_outer02, x_outer01:x_outer02]  # depth roi 지정
imgInstanceNormalSrc = imgDepthInstanceRoi.copy()  # roi array 복제
# cv2.imwrite('../img/imp_image/sample01/result_depth_60.png', img*60)

#  정규화
imgInstanceBlurSrc = cv2.normalize(imgInstanceNormalSrc, None, 255, 255 * 255, cv2.NORM_MINMAX)
# img_norm1 = cv2.normalize(imimgInstanceNormalSrcg3, None, 1, 50, cv2.NORM_MINMAX)
# img_norm1= cv2.normalize(imgimgInstanceNormalSrc3, None, 1, 255, cv2.NORM_MINMAX)

# median 블러 API
imgInstanceNormalRet = cv2.medianBlur(imgInstanceBlurSrc, 5)
# imgInstanceNormalRet = imgInstanceBlurSrc

# 결과 image save
# merged = np.hstack((img_norm2, blur, blur2))
saveInstanceNormPath = join(imgDir, saveInstanceNormPng)
cv2.imwrite(saveInstanceNormPath, imgInstanceNormalRet)

# Mask area coordinates
maskIndices = np.where(imgMaskInstanceRet == [255])
# coordinates list [0] - x axis - height, [1] -y axis - width
maskCoordinates = np.array(list(zip(maskIndices[0], maskIndices[1])))

# unMask area coordinates
unMaskIndices = np.where(imgMaskInstanceRet != [255])
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
        depthValue = imgInstanceNormalRet[xy[0], xy[1]]
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
        depthValue = imgInstanceNormalRet[xy[0], xy[1]]
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
viewDepth = cv2.cvtColor(imgInstanceNormalRet, cv2.COLOR_GRAY2BGR)
for i, t in enumerate(boolMedian):
    if t:
        x, y = unMaskCoordinates[i, :]
        viewDepth[x, y] = [0, 255, 0]
        imgRgbFixedRet[x, y] = [0, 255, 0]

        # break
    else:
        x, y = unMaskCoordinates[i, :]
        viewDepth[x, y] = [0, 0, 255]
        imgRgbFixedRet[x, y] = [0, 0, 255]

saveVisualDepthPath = join(imgDir, saveVisualDepthPng)
cv2.imwrite(saveVisualDepthPath, viewDepth)

saveVisualRgbPngPath = join(imgDir, saveVisualRgbPng)
cv2.imwrite(saveVisualRgbPngPath, imgRgbFixedRet)
# visualization end

print('end')

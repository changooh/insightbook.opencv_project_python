import cv2
import numpy as np

# load masking image
# imgMaskSrc = '../img/imp_image/sample01/result_mask_1.png'
imgMaskSrc = '../img/imp_image/data/result_mask_2.png'

imgMask = cv2.imread(imgMaskSrc)
imgMaskGray = cv2.cvtColor(imgMask, cv2.COLOR_BGR2GRAY)

# load depth image
# imgDepthSrc = '../img/imp_image/sample01/result_norm_1.png'
imgDepthSrc = '../img/imp_image/data/result_norm_2.png'
imgDepth = cv2.imread(imgDepthSrc)
imgDepthGray = cv2.cvtColor(imgDepth, cv2.COLOR_BGR2GRAY)

# load object image
# imgRgbSrc = '../img/imp_image/sample01/result_rbg_1.png'
imgRgbSrc = '../img/imp_image/data/result_rbg_2.png'

imgRgb = cv2.imread(imgRgbSrc)

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
        depthValue = imgDepthGray[xy[0], xy[1]]
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
        depthValue = imgDepthGray[xy[0], xy[1]]
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

# visualization

for i, t in enumerate(boolMedian):
    if t:
        x, y = unMaskCoordinates[i, :]
        imgDepth[x, y] = [0, 255, 0]
        imgRgb[x, y] = [0, 255, 0]

        # break
    else:
        x, y = unMaskCoordinates[i, :]
        imgDepth[x, y] = [0, 0, 255]
        imgRgb[x, y] = [0, 0, 255]

cv2.imwrite('../img/imp_image/data/result_detect_2.png', imgDepth)
cv2.imwrite('../img/imp_image/data/result_rgb_detect_2.png', imgRgb)

# cv2.imwrite('../img/imp_image/sample01/result_detect_1.png', imgDepth)
# cv2.imwrite('../img/imp_image/sample01/result_rgb_detect_1.png', imgRgb)


print('end')

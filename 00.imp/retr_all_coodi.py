import cv2
import numpy as np

# load masking image
imgMaskSrc = '../img/imp_image/mask_2_2.png'
imgMask = cv2.imread(imgMaskSrc)
imgMaskGray = cv2.cvtColor(imgMask, cv2.COLOR_BGR2GRAY)

# load depth image
imgDepthSrc = '../img/imp_image/img_norm2.png'
imgDepth = cv2.imread(imgDepthSrc)
imgDepthGray = cv2.cvtColor(imgDepth, cv2.COLOR_BGR2GRAY)

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
newMaskArray = np.zeros((maskCoordinates.shape[0], maskCoordinates.shape[1] + 1))
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

# Get max, min, median values
print('---Masked---')
print("mean: %d" % np.mean(maskColList))
print("std: %d" % np.std(maskColList))
print("median: %d" % np.median(maskColList))
print("min: %d" % np.min(maskColList))
print("max: %d" % np.max(maskColList))

# Get each depth value from unMaskCoordinates
unMaskColList = []
newUnMaskArray = np.zeros((unMaskCoordinates.shape[0], unMaskCoordinates.shape[1] + 1))
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

# Get max, min, median values
print('---unMasked---')
print("mean: %d" % np.mean(unMaskColList))
print("std: %d" % np.std(unMaskColList))
print("median: %d" % np.median(unMaskColList))
print("min: %d" % np.min(unMaskColList))
print("max: %d" % np.max(unMaskColList))





# import cv2
# import numpy as np
#
# cap = cv2.imread('/home/PATH/TO/IMAGE/IMG_0835.jpg')
# #You're free to do a resize or not, just for the example
# cap = cv2.resize(cap, (340,480))
# for x in range (0,340,1):
#     for y in range(0,480,1):
#         color = cap[y,x]
#         print color

print('end')

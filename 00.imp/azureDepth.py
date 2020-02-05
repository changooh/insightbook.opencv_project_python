import cv2
import numpy as np

# load depth image
imgDepthSrc = '../img/imp_image/data/crop_depth_0.png'
imgDepth = cv2.imread(imgDepthSrc, -1)
# imgDepthGray = cv2.cvtColor(imgDepth, cv2.COLOR_BGR2GRAY)
#  정규화
img_norm1 = cv2.normalize(imgDepth, None, 255, 255 * 255, cv2.NORM_MINMAX)


# cv2.imshow('img1', img_norm1)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

cv2.imwrite('../img/imp_image/data/azure_norm1.png', img_norm1)


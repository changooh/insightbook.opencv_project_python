import cv2
import numpy as np

# img = cv2.imread('../img/imp_image/01_17_16_29_34_fix.png', cv2.IMREAD_GRAYSCALE)
# print(img.shape)
# print(img.size)
# y = 674
# x = 1071
# roi = img[y+5:y+20, x+50:x+90]
# print(roi)

img = cv2.imread('../img/imp_image/01_17_16_29_34_fix.png', cv2.IMREAD_COLOR)

# y = 674
# x = 1071
# roi = img[y:y+50, x:x+50]
# print(roi)

hist, bins = np.histogram(img.flatten(), 256, [0, 256])

cdf = hist.cumsum()

# cdf의 값이 0인 경우는 mask처리를 하여 계산에서 제외
# mask처리가 되면 Numpy 계산에서 제외가 됨
# 아래는 cdf array에서 값이 0인 부분을 mask처리함
cdf_m = np.ma.masked_equal(cdf, 0)

#History Equalization 공식
cdf_m = (cdf_m - cdf_m.min())*255/(cdf_m.max()-cdf_m.min())

# Mask처리를 했던 부분을 다시 0으로 변환
cdf = np.ma.filled(cdf_m, 0).astype('uint8')

img2 = cdf[img]

# cv2.imshow('cropped', roi)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# inner coordinates:  1071 674 1163 748
# outer coordinates:  1061 664 1173 758

# x,y,w,h	=	cv2.selectROI('img', img, False)
# if w and h:
#     roi = img[y:y+h, x:x+w]
#     cv2.imshow('cropped', roi)  # ROI 지정 영역을 새창으로 표시
#     # cv2.moveWindow('cropped', 0, 0) # 새창을 화면 좌측 상단에 이동
#     cv2.imwrite('../cropped2.jpg', roi)   # ROI 영역만 파일로 저장
#
cv2.imshow('img', img2)
cv2.waitKey(0)
cv2.destroyAllWindows()


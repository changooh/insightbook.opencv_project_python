import cv2
import numpy as np

# 이미지 읽어서 그레이스케일 변환, 바이너리 스케일 변환
img = cv2.imread('../img/imp_image/01_17_16_29_34_fixed_mask_3.png')
# 이미지 읽어서 그레이스케일 변환, 바이너리 스케일 변환
img0 = cv2.imread('../img/imp_image/01_17_16_29_34_fixed_raw.jpg')

imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# ret, th = cv2.threshold(imgray, 200,255,cv2.THRESH_BINARY_INV)
ret, th = cv2.threshold(imgray, 200,255,cv2.THRESH_BINARY)

# find contours
im, contours, hr = cv2.findContours(th, cv2.RETR_EXTERNAL, \
                                        cv2.CHAIN_APPROX_SIMPLE)
contr = contours[0]

# draw inner bounding box (pink)
x, y, w, h = cv2.boundingRect(contr)
# print coordinates 1280 533 1359 616
print(w, h)
print("inner coordinates: ", x, y, x+w, y+h)
# draw rectangle
cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 255), 1)

# draw outer bounding box (blue)
# px 확대
px = 10
x_outer01 = x - px
x_outer02 = x + w + px
y_outer01 = y - px
y_outer02 = y + h + px
# print outer coordinates 1270 523 1369 626
print("outer coordinates: ", x_outer01, y_outer01, x_outer02, y_outer02)
# draw rectangle
cv2.rectangle(img, (x_outer01, y_outer01), (x_outer02, y_outer02), (255, 0, 0), 1)

roi = img[y_outer01:y_outer02, x_outer01:x_outer02]     # roi 지정
img2 = roi.copy()  # roi 배열 복제 ---①
cv2.imwrite('../img/imp_image/mask_3.png', img2)

roi0 = img0[y_outer01:y_outer02, x_outer01:x_outer02]     # roi 지정
# print(roi0.shape)

img00 = roi0.copy()  # roi 배열 복제 ---①
cv2.imwrite('../img/imp_image/mask_org_3.png', img00)
#
# # show image
# cv2.imshow('Bound Fit shapes', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
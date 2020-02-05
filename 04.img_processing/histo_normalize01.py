import cv2
import numpy as np
# import matplotlib.pylab as plt

#--① 그레이 스케일로 영상 읽기
# img = cv2.imread('../img/abnormal.jpg', cv2.IMREAD_GRAYSCALE)
# img2 = cv2.imread('../img/imp_image/01_17_16_29_34_fix.png', cv2.IMREAD_GRAYSCALE)
img = cv2.imread('../img/imp_image/01_17_16_29_34_fix.png', -1)
print(img.dtype)
# 1280 533 1359 616 00
#1385 563 1485 662 02
# 1331 625 1428 715 03
# x=320; y=150; w=50; h=50
roi = img[625:715, 1331:1428]     # roi 지정
img2 = roi.copy()           # roi 배열 복제 ---①
# print(img2)

# cv2.imwrite('../img/imp_image/fix60.png', img*60)
#--② 직접 연산한 정규화
# img_f = img2.astype(np.float32)
# print(img_f.max(), img_f.min())
# img_norm = ((img_f - img_f.min()) * (255*255) / (img_f.max() - img_f.min()))
# img_norm = img_norm.astype(np.uint16)

#  정규화
img_norm2 = cv2.normalize(img2, None, 0, 255*255, cv2.NORM_MINMAX)

# median 블러 API
blur = cv2.medianBlur(img_norm2, 5)

# 가우시안 블러 API로 블러링 ---③
# blur2 = cv2.GaussianBlur(img_norm2, (3, 3), 0)

#1341 635 1418 705
px = 10
w = 77
h = 70
# draw rectangle on blur
cv2.rectangle(blur, (px, px), (px+w, px+h), (0, 0, 0), 1)
# 결과 출력
# merged = np.hstack((img_norm2, blur, blur2))

cv2.imwrite('../img/imp_image/img_norm3.png', img_norm2)
cv2.imwrite('../img/imp_image/img_media3.png', blur)
# cv2.imwrite('../img/imp_image/img_gauss3.png', blur2)
# cv2.imwrite('../img/imp_image/img_media3_1.png', blur3)

# cv2.imshow('filtering', merged)
#
# cv2.waitKey(0)
# cv2.destroyAllWindows()







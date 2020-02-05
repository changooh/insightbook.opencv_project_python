import cv2
import numpy as np
# import matplotlib.pylab as plt

#--① 이미지 그레이 스케일로 읽기 및 출력
# img = cv2.imread('../img/mountain.jpg', cv2.IMREAD_GRAYSCALE)
img = cv2.imread('../img/imp_image/01_17_16_29_34_fix.png', cv2.IMREAD_GRAYSCALE)

# cv2.imshow('img', img)

# 1280 533 1359 616
# x=320; y=150; w=50; h=50
roi = img[533:616, 1280:1359]     # roi 지정
img2 = roi.copy()           # roi 배열 복제 ---①

#--② 히스토그램 계산 및 그리기
hist = cv2.calcHist([img2], [0], None, [256], [0,255])
# plt.plot(hist)
cv2.imshow('histogram', hist)

print("hist.shape:", hist.shape)  #--③ 히스토그램의 shape (256,1)
print("hist.sum():", hist.sum(), "img.shape:", img.shape) #--④ 히스토그램 총 합계와 이미지의 크기
# plt.show()
cv2.waitKey(0)
cv2.destroyAllWindows()

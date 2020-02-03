import cv2
import numpy as np

img_fix = '../img/imp_image/01_17_16_29_34_fixed_raw.jpg'
img_src03 = '../img/imp_image/01_17_16_29_34_fixed_mask_2.png'
# 이미지 읽어서 그레이스케일 변환, 바이너리 스케일 변환
img = cv2.imread(img_src03)
img0 = cv2.imread(img_fix)
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# binary threshold
ret, th = cv2.threshold(img_gray, 200, 255, cv2.THRESH_BINARY)
# cv2.imshow("threshold", th)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# find contours
im, contours, hr = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contr = contours[0]

# cv2.drawContours(img, contours, -1, (0, 255, 0), 3)
# cv2.imshow("RETR_EXTERNAL", img)
# cv2.waitKey(0)
# im, contours2, hr = cv2.findContours(th, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# cv2.drawContours(img, contours2, -1, (255, 0, 0), 3)
# cv2.imshow("RETR_TREE", img)
# cv2.waitKey(0)

# for cnt in contours:
#     rect = cv2.minAreaRect(cnt)
#     box = cv2.boxPoints(rect)
#     box = np.int0(box)
#     cv2.drawContours(img, [box], 0, (0, 0, 255), 3)

# cv2.imshow("RETR_TREE", img)
# cv2.waitKey(0)

# draw inner bounding box (pink)
x, y, w, h = cv2.boundingRect(contr)

# print coordinates 1280 533 1359 616
print(w, h)
print("inner coordinates: ", x, y, x + w, y + h)
# draw rectangle
cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 1)

# rotate rectangle
rect = cv2.minAreaRect(contr)
box = cv2.boxPoints(rect)
box = np.int0(box)
cv2.drawContours(img, [box], 0, (0, 255, 0), 1)

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

roi = img[y_outer01:y_outer02, x_outer01:x_outer02]  # instance mask roi 지정
img2 = roi.copy()  # roi array 복제 ---①
cv2.imwrite('../img/imp_image/mask_2_2.png', img2)

roi0 = img0[y_outer01:y_outer02, x_outer01:x_outer02]  # raw image roi 지정
# print(roi0.shape)

img00 = roi0.copy()  # roi array copy ---①
cv2.imwrite('../img/imp_image/mask_org_2.png', img00)

# instance depth roi
img9 = cv2.imread('../img/imp_image/01_17_16_29_34_fix.png', -1)
roi = img9[y_outer01:y_outer02, x_outer01:x_outer02]  # depth roi 지정
img2 = roi.copy()  # roi array 복제 ---①
# print(img2)
# cv2.imwrite('../img/imp_image/fix60.png', img*60)

#--② 직접 연산한 정규화
# img_f = img2.astype(np.float32)
# print(img_f.max(), img_f.min())
# img_norm = ((img_f - img_f.min()) * 255 / (img_f.max() - img_f.min()))
# img_norm = img_norm.astype(np.uint16)

#  정규화
img_norm1 = cv2.normalize(img2, None, 255, 255 * 255, cv2.NORM_MINMAX)
# img_norm1 = cv2.normalize(img2, None, 1, 50, cv2.NORM_MINMAX)
# img_norm1 = cv2.normalize(img2, None, 1, 255, cv2.NORM_MINMAX)

#
# max2nd1 = np.unique(img_norm1)[2]
# max2nd2 = np.unique(img_norm1)[1]

# median 블러 API
blur = cv2.medianBlur(img_norm1, 5)
# xMin = np.array(img_norm1)
v_median = np.median(blur)
# xMin = np.array(blur[px+1:px + h, px+1:px + w])
# xMin = np.array(blur[px:px + h, px:px + w])
# print(xMin.shape)
# print(xMin[10:30, 50:60])
# print(xMin.max())
# print(xMin.min())
# print(xMin.mean())
# print(xMin.var())
# print(xMin.std())


# draw rectangle on blur
cv2.rectangle(blur, (px, px), (px + w, px + h), (0, 0, 0), 1)
# 결과 출력
# merged = np.hstack((img_norm2, blur, blur2))
cv2.imwrite('../img/imp_image/img_norm1_2.png', img_norm1)
# cv2.imwrite('../img/imp_image/img_norm2_3.png', img_norm2)
cv2.imwrite('../img/imp_image/img_media2.png', blur)

# show image
# cv2.imshow('Bound Fit shapes', blur)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


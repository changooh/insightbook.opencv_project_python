import cv2

# 0
img_src03 = '../img/imp_image/01_17_16_29_34_fixed_mask_3.png'
image = cv2.imread(img_src03)

im_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# binary threshold
ret, th = cv2.threshold(im_gray, 200, 255, cv2.THRESH_BINARY_INV)

im2, contour, hierarchy = cv2.findContours(th, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
# 모든 좌표를 갖는 컨투어 그리기, 초록색  ---⑥
cv2.drawContours(image, contour, -1, (0, 255, 0), 4)

# for cnt in contours:
#     cv2.drawContours(th, cnt, -1, (0, 255, 0), 5)

# cv2.imshow("contour result", image)
# cv2.imshow("bitwise", bitwise)
cv2.imshow("result", image)
# cv2.imshow("result", gray)
# cv2.imshow("edge result", edge)
# cv2.imshow("th", th)
cv2.waitKey(0)
cv2.destroyAllWindows()

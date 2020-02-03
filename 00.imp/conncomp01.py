# https://mellowlee.tistory.com/entry/Opencv-connectedComponents-connectedComponentsWithStats

import cv2
import numpy as np
img_src = 'imagePath'
img = cv2.imread(img_src)
# color image load
gray = cv2.cvtColor(img, cv2.Color_bgr2gray)
# gray 변환
ret, labels, stats, centriods = cv2.connectedComponentsWithStats(gray)
img1 = np.zeros(img.shape, dtype=img.dtype)
for i in range(1, ret):
    r = np.random.randint(256)
    g = np.random.randint(256)
    b = np.random.randint(256)

    img1[labels==i] = [b, g, r]

    x, y, width, height = stats[i]
    cv2.rectangle(img1, (x, y), (x+width, y+height), (0,0,255), 2)
    cx, cy = centriods[i]
    cv2.circle(img1, (int(cx), int(cy)), 5, (255,0,0), -1)

cv2.imshow('components', img1)
cv2.waitkey()
cv2.destroyAllwindows()

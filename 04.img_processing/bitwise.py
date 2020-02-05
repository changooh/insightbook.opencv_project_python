import numpy as np, cv2
# import matplotlib.pylab as plt

#--① 연산에 사용할 이미지 생성
img1 = np.zeros( ( 200,400), dtype=np.uint8)
img2 = np.zeros( ( 200,400), dtype=np.uint8)


#
img1[:, :200] = 255         # 오른쪽은 검정색(0), 왼쪽은 흰색(255)
img2[100:200, :] = 255      # 위는 검정색(0), 아래는 흰색(255)

print(img1)
print(img2)
cv2.imshow('img1', img1)
cv2.imshow('img2', img2)


# -- ② 비트와이즈 연산
# 두 이미지의 255 영역이 만나는 부분
bitAnd = cv2.bitwise_and(img1, img2)
# 255 영역은 모두
bitOr = cv2.bitwise_or(img1, img2)
# 겹치는 영역은 0 안겹치는 영역은 255
bitXor = cv2.bitwise_xor(img1, img2)
# image1의 반대결과
bitNot = cv2.bitwise_not(img1)

cv2.imshow('bitand', bitAnd)
cv2.imshow('bitOr', bitOr)
cv2.imshow('bitXor', bitXor)
cv2.imshow('bitNot', bitNot)

cv2.waitKey(0)
cv2.destroyAllWindows()
# #--③ Plot으로 결과 출력
# imgs = {'img1':img1, 'img2':img2, 'and':bitAnd,
#           'or':bitOr, 'xor':bitXor, 'not(img1)':bitNot}
# for i, (title, img) in enumerate(imgs.items()):
#     plt.subplot(3,2,i+1)
#     plt.title(title)
#     plt.imshow(img, 'gray')
#     plt.xticks([]); plt.yticks([])
#
# plt.show()
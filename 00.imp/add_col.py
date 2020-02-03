import numpy as np

oData = np.array([[1, 2, 3], [4, 5, 6]])

# newCol = [7, 8]

newColList = []
a = 1
b = 2
newColList.append(a)
newColList.append(b)

newData = np.zeros((oData.shape[0], oData.shape[1] + 1))
print(newData)
newData[:, : -1] = oData
print(newData)
newData[:, -1] = newColList
print(newData)
#
# newColList = []
# a = 1
# b = 2
# c = 3
# newColList.append(a)
# newColList.append(b)
# newColList.append(c)
#
# print(newColList)





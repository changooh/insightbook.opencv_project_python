# def rankInstancePriority(depthMap, maskList, roi)
# Input Parameter1 - Depth Map(depth_map_array)
#
# Input Parameter2 - Cropped Mask image
# list(((mask_image_array), (xy_tuple)), (index 1),,, (index n))
#
# Input Parameter3 – ROI coordinates ((x, y), (x, y))  # 추후 확정
#
# Return Parameter rankList(3, 2,,, n)  # 우선순위 1위부터 instance index number return 함

import cv2
import numpy as np
import os
from os.path import isdir, exists, join


# def file path
def conFilePath():
    rootDir = os.getcwd()
    imgDir = join(rootDir, "img")
    if exists(imgDir):
        print("imgDir exists")
        retPass = True
    else:
        os.mkdir(imgDir)
        print("Try next time, conFilePath")
        retPass = False

    return retPass, imgDir


# def load fixed depth map
def loadFixedDepth(paraPass, imgDir):
    imgFixedRaw = "depth_fixed_raw.png"
    if paraPass:
        imgFixDepthSrc = join(imgDir, imgFixedRaw)
        if exists(imgFixDepthSrc):
            depthFixed = cv2.imread(imgFixDepthSrc, -1)
            print("fixed depth map loaded")
            paraPass = True
            retPass = paraPass
    else:
        print("Try next time, loadFixedDepth")
        paraPass = False
        retPass = paraPass

    return retPass, depthFixed


# def load masked instances
def loadMaskedInstance(paraPass, imgDir, paraPx=0):
    dataList = []
    if paraPass:
        imgMaskDir = join(imgDir, "src")
        if exists(imgMaskDir):
            print("imgMaskDir exists")
            imgMaskFileList = os.listdir(imgMaskDir)
            if len(imgMaskFileList) > 0:
                print("no of files: ", len(imgMaskFileList))
                for i, f in enumerate(imgMaskFileList):
                    imgMaskInstanceSrc = join(imgDir, f)
                    print(imgMaskInstanceSrc)
                    imgMaskInstance = cv2.imread(imgMaskInstanceSrc)
                    # 이미지 읽어서 그레이스케일 변환, 바이너리 스케일 변환
                    imgMaskInstanceGray = cv2.cvtColor(imgMaskInstance, cv2.COLOR_BGR2GRAY)
                    # binary threshold
                    ret, th = cv2.threshold(imgMaskInstanceGray, 200, 255, cv2.THRESH_BINARY)
                    # get contours
                    im, contours, hr = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    contr = contours[0]
                    # inner coordinate
                    x, y, w, h = cv2.boundingRect(contr)
                    # draw outer bounding box (blue)
                    # bounding box px 확대
                    x_outer01 = x - paraPx
                    x_outer02 = x + w + paraPx
                    y_outer01 = y - paraPx
                    y_outer02 = y + h + paraPx
                    # instance mask roi 지정
                    imgMaskInstanceRoi = th[y_outer01:y_outer02, x_outer01:x_outer02]
                    imgMaskInstanceRet = imgMaskInstanceRoi.copy()  # roi array 복제 ---①
                    maskData = (imgMaskInstanceRet, (y_outer01, y_outer02, x_outer01, x_outer02))
                    dataList.append(maskData)
                    print("end")

            else:
                print("None of masked instance files")
        else:
            os.mkdir(imgMaskDir)
            paraPass = False
            print("imgMaskDir just created")
    else:
        print("Try next time, loadMaskedInstance")

    return paraPass, dataList


def rankFreeInstance(imgDepth, maskDataList):
    rankInstList = []
    for i, objData in enumerate(maskDataList):
        print("start instance normalization")
        # instance depth roi
        imgDepthInstanceRoi = imgDepth[objData[1][0]:objData[1][1], objData[1][2]:objData[1][3]]  # depth roi 지정
        imgInstanceNormalSrc = imgDepthInstanceRoi.copy()
        # normalization
        imgInstanceBlurSrc = cv2.normalize(imgInstanceNormalSrc, None, 255, 255 * 255, cv2.NORM_MINMAX)
        # median 블러 API
        imgInstanceNormalRet = cv2.medianBlur(imgInstanceBlurSrc, 5)
        # unMask area coordinates
        unMaskIndices = np.where(objData[0] != [255])
        # coordinates list [0] - x axis - height, [1] -y axis - width
        unMaskCoordinates = np.array(list(zip(unMaskIndices[0], unMaskIndices[1])))
        print("rankFreeInstance end")
        # Mask area coordinates
        maskIndices = np.where(objData[0] == [255])
        # coordinates list [0] - x axis - height, [1] -y axis - width
        maskCoordinates = np.array(list(zip(maskIndices[0], maskIndices[1])))
        # Get each depth value from maskCoordinates
        maskColList = []
        newMaskArray = np.zeros((maskCoordinates.shape[0], maskCoordinates.shape[1] + 1), dtype=int)
        # newMaskArray = np.zeros((5, 3))
        # newMaskArray[:, : -1] = maskCoordinates[5, :]
        newMaskArray[:, : -1] = maskCoordinates
        # print(newMaskArray)
        breakPoint = 100000
        for e, xy in enumerate(maskCoordinates):
            if e == breakPoint:
                break
            else:
                depthValue = imgInstanceNormalRet[xy[0], xy[1]]
                maskColList.append(depthValue)
        # print(newColList)
        newMaskArray[:, -1] = maskColList
        # print(newMaskArray)

        # # Get max, min, median values
        # print('---Masked---')
        # print("mean: %d" % np.mean(maskColList))
        # print("std: %d" % np.std(maskColList))
        # print("median: %d" % np.median(maskColList))
        # print("min: %d" % np.min(maskColList))
        # print("max: %d" % np.max(maskColList))

        # Get each depth value from unMaskCoordinates
        unMaskColList = []
        newUnMaskArray = np.zeros((unMaskCoordinates.shape[0], unMaskCoordinates.shape[1] + 1), dtype=int)
        # newMaskArray = np.zeros((5, 3))
        # newMaskArray[:, : -1] = maskCoordinates[5, :]
        newUnMaskArray[:, : -1] = unMaskCoordinates
        # print(newMaskArray)
        breakPoint = 100000
        for e, xy in enumerate(unMaskCoordinates):
            if e == breakPoint:
                break
            else:
                depthValue = imgInstanceNormalRet[xy[0], xy[1]]
                unMaskColList.append(depthValue)

        # print(newColList)
        newUnMaskArray[:, -1] = unMaskColList
        # print(newMaskArray)
        # # Get max, min, median values
        # print('---unMasked---')
        # print("mean: %d" % np.mean(unMaskColList))
        # print("std: %d" % np.std(unMaskColList))
        # print("median: %d" % np.median(unMaskColList))
        # print("min: %d" % np.min(unMaskColList))
        # print("max: %d" % np.max(unMaskColList))

        # instance 중앙값보다 같거나 높은 위치의 fix rate
        medianValue = np.median(maskColList)
        # medianValue = medianValue + 10.0
        # boolMedian = np.array(unMaskColList) <= medianValue
        boolMedian = np.array(unMaskColList) > medianValue
        # boolMedian = unMaskColList <= np.std(unMaskColList)
        # print(boolMedian)
        cntTrue = np.sum(boolMedian)
        rateFree = cntTrue / len(unMaskColList)
        # print('median, cntTrue, rateMedian: ', np.median(maskColList), cntTrue, rateFree)
        rankData = (i, rateFree)
        rankInstList.append(rankData)
        rankInstList.sort(key=lambda x: x[1], reverse=True)

    return rankInstList

if __name__ == '__main__':
    # RUN FUNCTIONS
    isPass, srcFilePath = conFilePath()
    isPass, imgDepthFixed = loadFixedDepth(isPass, srcFilePath)
    isPass, maskInstanceList = loadMaskedInstance(isPass, srcFilePath, paraPx=10)
    rankInstanceList = rankFreeInstance(imgDepthFixed, maskInstanceList)
    print(rankInstanceList)

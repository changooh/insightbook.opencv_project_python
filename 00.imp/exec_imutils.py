import cv2
import imutils
import os
from os.path import join
from imutils import paths
import matplotlib as plt

# https://github.com/jrosebr1/imutils
# pip install imutils

# Finding function OpenCV functions by name
imutils.find_function("contour")
# console print
# 1. CONTOURS_MATCH_I1
# 2. CONTOURS_MATCH_I2
# 3. CONTOURS_MATCH_I3
# 4. contourArea
# 5. drawContours
# 6. findContours
# 7. isContourConvex

# internet image read
url = "https://trello-attachments.s3.amazonaws.com/5e4cd8cac105a4738cd6eb14/346x464/921fbf30eb86f02014af149b9f2750de/2020-02-19_15_44_11.png"
logo = imutils.url_to_image(url)
cv2.imshow("URL to Image", logo)
cv2.waitKey(1000)
cv2.destroyWindow("URL to Image")

# # Translation
# # translate the image x=25 pixels to the right and y=75 pixels up
# translated = imutils.translate(logo, 25, -75)
# # cv2.imshow("translated", translated)

# # Rotation
# # loop over the angles to rotate the image
# for angle in (45, 200, 90):
#     # rotate the image and display it
#     rotated = imutils.rotate(logo, angle=angle)
#     # cv2.imshow("Rotation Angle=%d" % angle, rotated)

# # Resizing
# # loop over varying widths to resize the image to
# for width in (400, 300, 200, 100):
#     # resize the image and display it
#     resized = imutils.resize(logo, width=width)
#     # cv2.imshow("Resizing Width=%dpx" % width, resized)

# # Skeletonization
# # skeletonize the image
# size is the size of the structuring element kernel
# gray = cv2.cvtColor(logo, cv2.COLOR_BGR2GRAY)
# cv2.imshow("gray", gray)
# skeleton = imutils.skeletonize(gray, size=(3, 3))
# cv2.imshow("Skeleton", skeleton)

# Displaying with Matplotlib
# # INCORRECT: show the image without converting color spaces
# plt.figure("Incorrect")
# plt.imshow(logo)
# # CORRECT: convert color spaces before using plt.imshow
# plt.figure("Correct")
# plt.imshow(imutils.opencv2matplotlib(logo))
# plt.show()

# # Checking OpenCV Versions
# print("Your OpenCV version: {}".format(cv2.__version__))
# print("Are you using OpenCV 2.X? {}".format(imutils.is_cv2()))
# print("Are you using OpenCV 3.X? {}".format(imutils.is_cv3()))
# print("Are you using OpenCV 4.X? {}".format(imutils.is_cv4()))

# # Automatic Canny Edge Detection
# gray = cv2.cvtColor(logo, cv2.COLOR_BGR2GRAY)
# edgeMap = imutils.auto_canny(gray)
# cv2.imshow("Original", logo)
# cv2.imshow("Automatic Edge Map", edgeMap)


# 4-point Perspective Transform
# http://www.pyimagesearch.com/2014/09/01/build-kick-ass-mobile-document-scanner-just-5-minutes/

# Sorting Contours
# Example:
# See the contents of demos/sorting_contours.py

# (Recursively) Listing Paths to Images
rootDir = os.getcwd()
srcDir = join(rootDir, "img")
for imagePath in paths.list_images(srcDir):

    print(imagePath)




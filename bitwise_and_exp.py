import numpy as np
import cv2
from matplotlib import pyplot as plt

img1 = cv2.imread('bitwise_1.png')
img2 = cv2.imread('bitwise_2.png')
img3 = cv2.imread('bitwise_3.png')
img4 = cv2.imread('bitwise_4.png')
img5 = cv2.imread('bitwise_5.png')

bitwiseAnd = cv2.bitwise_and(img1, img2)
bitwiseAnd = cv2.bitwise_and(bitwiseAnd, img3)
bitwiseAnd = cv2.bitwise_and(bitwiseAnd, img4)
image = cv2.bitwise_and(bitwiseAnd, img5)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# corners = cv2.goodFeaturesToTrack(gray,25,0.01,10)
# corners = np.int0(corners)
 
# for i in corners:
#     x,y = i.ravel()
#     cv2.circle(image,(x,y),3,255,-1)
 
# plt.imshow(image),plt.show()

edges = cv2.Canny(gray, 100, 200)
plt.imshow(edges, cmap='gray')
plt.title('Edge Image')
plt.show()


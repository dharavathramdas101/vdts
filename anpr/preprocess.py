import cv2

img = r"C:\Users\DHARAVATH RAMDAS\vdts\ts_numberplate_img.jpg"
img = cv2.imread(img)

# gray scale conversion 
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#cv2.imshow("gray_image",gray_img)
#cv2.waitKey(0)

# remove noise from image using median filtering
"""try:
    filter_img = cv2.bilateralFilter(gray_img, 11, 17, 17)
    cv2.imshow("filtered img", filter_img)
    cv2.waitKey(0)
except Exception as e:
    print("Error " + str(e))"""

try:
    edge = cv2.Canny(gray_img, 30, 200)
    cv2.imshow("edge_img", edge)
    cv2.waitKey(0)
except Exception as e:
    print("Error" + str(e))

    
import cv2

pic = cv2.imread('picture0.jpg')

while True:
    cv2.imshow('img',pic)
    if cv2.waitKey(1) == ord('q'):
            break
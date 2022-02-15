import cv2 
import depthai as dai

#create a pipeline
pipeline = dai.Pipeline()

#define the source and output
camRgb = pipeline.create(dai.node.ColorCamera)
xoutVideo = pipeline.create(dai.node.XLinkOut)

xoutVideo.setStreamName("video")

#properties

camRgb.setBoardSocket(dai.CameraBoardSocket.RGB)
camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
camRgb.setVideoSize(960, 540)

xoutVideo.input.setBlocking(False)
xoutVideo.input.setQueueSize(1)

#Linking
camRgb.video.link(xoutVideo.input)

with dai.Device(pipeline) as device:

    video = device.getOutputQueue(name="video", maxSize=1, blocking=False)

    while True:
        videoIn = video.get()
        img_gray = cv2.cvtColor(videoIn.getCvFrame(), cv2.COLOR_BGR2GRAY)
        img_blur = cv2.GaussianBlur(img_gray, (3,3), cv2.BORDER_DEFAULT)
        sobelx = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=0, ksize=5)
        sobely = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=0, dy=1, ksize=5)
        sobelxy = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=5)
        cv2.imshow('Sobel X', sobelx)
        cv2.imshow('Sobel Y', sobely)
        cv2.imshow('Sobel X Y using Sobel() function', sobelxy)
        edges = cv2.Canny(image=img_blur, threshold1=150, threshold2=190)
        cv2.imshow('Canny Edge Detection', edges)
        if cv2.waitKey(1) == ord('q'):
            break
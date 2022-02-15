import cv2 
import depthai as dai
import numpy as np
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
        gray_image = cv2.cvtColor(videoIn.getCvFrame(), cv2.COLOR_BGR2GRAY)
        laplace = cv2.Laplacian(gray_image, cv2.CV_64F)
        laplace = np.uint8(np.absolute(laplace))
        cv2.imshow('Laplacian Image', laplace)
        if cv2.waitKey(1) == ord('q'):
            break
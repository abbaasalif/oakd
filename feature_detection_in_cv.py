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
        #Get BGR from NV12 encoded video frame to show with opencv
        # cv2.imshow("video", videoIn.getCvFrame())
        orb = cv2.ORB_create()
        # cv2.resize(videoIn.getCvFrame(),(960,540)
        kp = orb.detect(videoIn.getCvFrame(),None)
        kp, des = orb.compute(videoIn.getCvFrame(), kp)
        img2 = cv2.drawKeypoints(videoIn.getCvFrame(), kp, None, color = (0,255,0), flags=0)
        cv2.imshow("output", img2)


        if cv2.waitKey(1) == ord('q'):
            break
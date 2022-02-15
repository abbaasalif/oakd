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
camRgb.setVideoSize(1920, 1080)

xoutVideo.input.setBlocking(False)
xoutVideo.input.setQueueSize(1)

#Linking
camRgb.video.link(xoutVideo.input)

with dai.Device(pipeline) as device:

    video = device.getOutputQueue(name="video", maxSize=1, blocking=False)

    while True:
        videoIn = video.get()
        
        #Get BGR from NV12 encoded video frame to show with opencv
        cv2.imshow("video", videoIn.getCvFrame())

        if cv2.waitKey(1) == ord('q'):
            break
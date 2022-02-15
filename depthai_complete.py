import cv2
import depthai as dai
import numpy as np

def getFrame(queue):
    #Get frame from the queue
    frame = queue.get()
    #convert the frmae to OpenCV format and return
    return frame.getCvFrame()

def getMonoCamera(pipeline, isLeft):
    #configure mono camera
    mono = pipeline.createMonoCamera()

    #set the Camera Resolution
    mono.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
    if isLeft:
        mono.setBoardSocket(dai.CameraBoardSocket.LEFT)
    else:
        mono.setBoardSocket(dai.CameraBoardSocket.RIGHT)
    return mono
def getcolorcam(pipeline):
    camRgb = pipeline.create(dai.node.ColorCamera)

    #set the camera resolution
    camRgb.setBoardSocket(dai.CameraBoardSocket.RGB)
    camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
    camRgb.setVideoSize(1920, 1080)

if __name__ == '__main__':

    #define a pipeline
    pipeline = dai.Pipeline()

    #set up left and right cameras
    monoLeft = getMonoCamera(pipeline, isLeft = True)
    monoRight = getMonoCamera(pipeline, isLeft = False)
    rgb = getcolorcam(pipeline)

    #set output Xlink for left camera
    xoutLeft = pipeline.createXLinkOut()
    xoutLeft.setStreamName("left")

    #set output XLink for color camera
    xoutRgb = pipeline.create(dai.node.XLinkOut)
    xoutRgb.setStreamName("color")

    #set output Xlink for right camera
    xoutRight = pipeline.createXLinkOut()
    xoutRight.setStreamName("right")

    #Attach cameras to output XLink 
    monoLeft.out.link(xoutLeft.input)
    monoRight.out.link(xoutRight.input)
    camRgb.video.link(xoutRgb.input)
    xoutRgb.input.setBlocking(False)
    xoutRgb.input.setQueueSize(1)
    #pipeline is defined, now we can connect to the device
    with dai.Device(pipeline) as device:

        #get the output queues.
        leftQueue = device.getOutputQueue(name = 'left', maxSize=1)
        rightQueue = device.getOutputQueue(name = 'right', maxSize = 1)
        rgb = device.getOutputQueue(name="color", maxSize=1)
        
        #Set the display window name
        cv2.namedWindow("Stereo Pair")
        #Variable used to toggle between side by side view and one frame view
        sidebySide = True

        while True:
            #get left Frame
            leftFrame = getFrame(leftQueue)
            #get right frame
            rightFrame = getFrame(rightQueue)

            if sidebySide:
                #show side by side view
                imOut = np.hstack((leftFrame, rightFrame))

            else:
                imOut = np.uint8(leftFrame/2 + rightFrame/2)
            #Display the output image
            cv2.imshow("Stereo Pair", imOut)

            #check for keyboard input
            key = cv2.waitKey(1)
            if key == ord('q'):
                break # quit when q is pressed
            elif key == ord('t'):
                sidebySide = not sidebySide
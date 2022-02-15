import depthai as dai
import cv2
#everthing processed in opencv ai kit is donr through a pipeline object below
pipeline = dai.Pipeline()
#we are creating a pipline to get the feed from left monocamera and create a xlink input 
mono = pipeline.createMonoCamera()
mono.setBoardSocket(dai.CameraBoardSocket.LEFT) # xlink node created it is a mechanism using which you device (OAK D) connects to your host. You can have either xlinkIN or xlinkOUT

#now we are going to create the XlinkOut for the output of frmaes
xout = pipeline.createXLinkOut()
xout.setStreamName("left")
mono.out.link(xout.input)

with dai.Device(pipeline) as device:
    queue = device.getOutputQueue(name='left')
    frame = queue.get()
    imOut = frame.getCvFrame()
    cv2.imshow("Image", imOut)
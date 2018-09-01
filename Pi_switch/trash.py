import cv2
import numpy as np
import socket
import ctypes
import struct

cap = []
cap.append(cv2.VideoCapture(0))
#cap.append(cv2.VideoCapture(1))

cap[0].set(cv2.CAP_PROP_FPS, 15)
#cap[1].set(cv2.CAP_PROP_FPS, 15)

#grab a single frame from one camera
def grab(num):
    res, im = cap[num].read()
    return (res,im)

#grab a frame from each camera and stitch them
#side by side
def grabSBS():
    res, imLeft  = grab(1)
    #next line is for pretending I have 2 cameras
    #imRight = imLeft.copy()
    res, imRight = grab(0)
    imSBS = np.concatenate((imLeft, imRight), axis=1)
    return res,imSBS

###For displaying locally instead of streaming
#while(False):
#    res, imLeft = grab(0)
#    imRight = imLeft.copy()
#    imSBS = np.concatenate((imLeft, imRight), axis=1)
#    cv2.imshow("win", imSBS)
#    cv2.waitKey(20)

header_data = ctypes.create_string_buffer(12)

while(True):
    sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sck.bind(("10.0.0.XXX", 12321))

    sck.listen(1)

    while(True):
        (client, address) = sck.accept()
        print ("Client connected:", address)
        try:
            while (True):
                res, im = grabSBS()
                if (res):
                    success, coded = cv2.imencode('.jpg', im)
                    if (success):
                        height, width, channels = im.shape
                        size = len(coded)
                        struct.pack_into(">i", header_data , 0, width)
                        struct.pack_into(">i", header_data , 4, height)
                        struct.pack_into(">i", header_data , 8, size)
                        client.sendall(header_data .raw)
                        client.sendall(coded.tobytes())
        except Exception as ex:
            print ("ERROR:", ex)
            client.close()
            sck.close()
            exit()
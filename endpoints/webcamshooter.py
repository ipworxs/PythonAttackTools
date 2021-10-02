#!/usr/bin/env python

__description__ = 'Webcamshooter - Takes Picture from Main Webcam and Save it to disk'
__author__ = 'Oliver G.'
__version__ = '0.0.1'
__date__ = '2021/10/2021'

"""
Source code put in public domain, no Copyright
Use this tool at your own risk


History:
  2021/10/2021: start
 
Todo:
"""

import cv2 
import socket
import time
import os

cam = cv2.VideoCapture(0 + cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
cam.set(cv2.CAP_PROP_FPS, 30)
cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

timestr = time.strftime("%Y%m%d-%H%M%S")

ret, frame = cam.read()

# generate filename
img_name = "c:\\Temp\\"+str(socket.gethostname())+"-"+str(timestr)+".png"

# Create Folder if not exist
os.makedirs(os.path.dirname(img_name), exist_ok=True)

# save to disk
cv2.imwrite(img_name, frame)

cam.release()
cv2.destroyAllWindows()
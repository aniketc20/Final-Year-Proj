from email import message
from http import server
from math import fabs
from turtle import width
import cv2, imutils, socket
import numpy as np
import time
import base64

BUFF_SIZE = 65536
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
host_name = socket.gethostname()
host_ip = "192.168.0.103"
print(host_ip)
port = 9999
socket_address = (host_ip, port)
server_socket.bind(socket_address)
print(socket_address)

vid = cv2.VideoCapture('https://advertisementfyp.blob.core.windows.net/videos/Dog - 15305.mp4')

while True:
    msg, client_addr = server_socket.recvfrom(BUFF_SIZE)
    WIDTH = 400
    while(vid.isOpened()):
        _,frame = vid.read()
        frame = imutils.resize(frame, width = WIDTH)
        encoded, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80 ])
        message = base64.b64encode(buffer)
        server_socket.sendto(message, client_addr)
        cv2.imshow('TRANSMITTING VIDEO', frame)
        key = cv2.waitKey(1)&0xFF
        if key == ord('q'):
            server_socket.close()
            break

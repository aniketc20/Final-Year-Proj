
# This is server code to send video frames over UDP
import cv2, imutils, socket
import numpy as np
import time
import base64
from _thread import *
import os
import sys
import mysql.connector

connection = mysql.connector.connect(
  host="localhost",
  user="root",
  password="pampadeepak",
  database="advertisement"
)

sys.path.insert(1, os.getcwd())
print(os.getcwd())

BUFF_SIZE = 65536
server_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
host_name = socket.gethostname()
host_ip = '192.168.68.174'#  socket.gethostbyname(host_name)
print(host_ip)
port = 9999
ThreadCount = 0
socket_address = (host_ip,port)
server_socket.bind(socket_address)
print('Listening at:',socket_address)

#print(Slot.objects.all())
sql_select_Query = "SELECT * FROM advertisement.slot;"
cursor = connection.cursor()
cursor.execute(sql_select_Query)
# get all records
records = cursor.fetchall()
print("Total number of rows in table: ", cursor.rowcount)

print("\nPrinting each row")
videos = []
for row in records:
        print("Id = ", row[0], )
        print("Slot Date = ", row[1])
        print("Slot Timing  = ", row[2])
        print("Billboard ID  = ", row[3], "\n")
        print("Company ID  = ", row[4], "\n")
        print("Video url  = ", row[5], "\n")
        videos.append(row[5])
        # 'http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4',
        # 'http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4']
videos = [0,'/Users/aniketchoudhary/Desktop/10secs/pexels-koolshooters-8533480 (1).mp4', '/Users/aniketchoudhary/Desktop/15secs/vid2.mp4', '/Users/aniketchoudhary/Desktop/10secs/pexels-koolshooters-8533480 (1).mp4']
vid = cv2.VideoCapture(videos[0]) #  replace 'rocket.mp4' with 0 for webcam
fps,st,frames_to_count,cnt = (0,0,20,0)


while True:
    msg,client_addr = server_socket.recvfrom(BUFF_SIZE)
    print('GOT connection from ',client_addr)
    WIDTH=400
    count = 0
    while(vid.isOpened()):
        ret,frame = vid.read()
        if not ret:
            count = count + 1
            if(count<len(videos)):
                vid = cv2.VideoCapture(videos[count]) #  replace 'rocket.mp4' with 0 for webcam
            else:
                count = 0
                vid = cv2.VideoCapture(videos[count])
            ret,frame = vid.read()
        frame = imutils.resize(frame,width=WIDTH)
        encoded,buffer = cv2.imencode('.jpg',frame,[cv2.IMWRITE_JPEG_QUALITY,80])
        message = base64.b64encode(buffer)
        server_socket.sendto(message,client_addr)
        frame = cv2.putText(frame,'FPS: '+str(fps),(10,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
        cv2.imshow('TRANSMITTING VIDEO',frame)
        key = cv2.waitKey(1) & 0xFF

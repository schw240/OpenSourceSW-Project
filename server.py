import socketserver
import datetime
import base64
import numpy as np
import cv2
import os
import socket
import os
import sys

while True:

    host = "192.168.0.13"
    port = 9955
    server_sock = socket.socket(socket.AF_INET)
    server_sock.bind((host, port))
    server_sock.listen(5)
    print("get....")
    client_sock, addr = server_sock.accept()
    print("connected : ", addr)
    now = datetime.datetime.now().strftime("%H-%M")

    image1 = []

    try:
    
        while True:
            data1=client_sock.recv(1024)
            print("data1 = ")
            print(data1)
            print("length = ")
            print(len(data1))
            image1.extend(data1)
            if len(data1) < 1024:
                break
        print("get over")
        image = np.asarray(bytearray(image1), dtype="uint8")
        print("point1")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        print("point2")
        #cv2.imwrite("./" + str(now) + ".jpg", image)
        cv2.imwrite("./" + str(now) + ".jpg", image)
        print("point3")
    except Exception:
        print(addr,"exception")
        shutdown(client_sock, SHUT_RD)
    filename = str(now) + ".jpg"
    print("1point")
    f=open(filename,'rb')
    data2=f.read()
    exx=client_sock.sendall(data2)
    print("send????")
    f.flush()
    f.close()
import socketserver
import datetime
import base64
import numpy as np
import cv2
import os
import socket

host = ""
port = 9955
server_sock = socket.socket(socket.AF_INET)
server_sock.bind((host, port))
server_sock.listen(5)
print("get....")
client_sock, addr = server_sock.accept()
print("connected : ", addr)

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
    cv2.imwrite("./fromclient2.jpg", image)
    print("point3")
except Exception:
    print(addr,"exception")
    shutdown(client_sock, SHUT_RD)

filename = "toclient.jpg"
print("1point")
f=open(filename,'rb')
data2=f.read()
exx=client_sock.sendall(data2)
f.flush()
f.close()
client_sock.close()
server_sock.close()


#f = open(filename,'rb')
#print("2point")
#data2 = f.read()
#print("3point")
#exx=client_sock.sendall(data2)
#print ("4point")
#f.flush()
#print ("5point")
#f.close()
#print ("6point")



#data2 = f.read(1024)
#print("3point")
#while (data2):
#    print("4point")
#    print("data1 = ")
#    print(data2)
#    client_sock.send(data2)
#    print("5point")
#    data2 = f.read(1024)
#    print("6point")
#    if len(data2) < 1024:
#        break
#f.close()
#print("8point")
#server_sock.close()
#print("9point")

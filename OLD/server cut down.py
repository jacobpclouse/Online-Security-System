import socket
import cv2
import pickle
import struct
import imutils
# Server Socket
# create an INET, STREAMing socket
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print("HOST IP: ", host_ip)
port = 10050
socket_address = (host_ip,port)
print(f"Socket Created: {socket_address}")
# Bind socket to the host,
# the values passed to bind() depend on the address family of the socket
server_socket.bind(socket_address)
print("Socket bind complete")
# listen() enables a server to accept() connections
# listen() has a backlog parameter,
# It specifies the number of unaccepted connections that the system will allow before refusing new connection
server_socket.listen(5)
print("Socket now listening")
while True:
    client_socket,addr = server_socket.accept()
    print('Connection from: ',addr)
    if client_socket:
        vid = cv2.VideoCapture(0)
        while(vid.isOpened()):
            img,frame = vid.read()
            a = pickle.dumps(frame)
            message = struct.pack("Q",len(a))+a
            client_socket.sendall(message)
            cv2.imshow('Sending...',frame)
            key = cv2.waitKey(10)
            if key ==13:
                client_socket.close()
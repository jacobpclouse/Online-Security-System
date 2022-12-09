import socket
import cv2
import pickle
import struct
import imutils
# CLIENT SOCKET
# create an INET, STREAMING SOCKET: 
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_ip = '127.0.1.1' # use command line args to pass this in
port = 10050 # Port to listen on (non privilaged ports are > 1023)
# now connect to the web server on the specified port
client_socket.connect((host_ip,port))
# 'b' or 'B' produces an instance of bytes (instead of a string) 
data = b''
# Q: unsigned long integer
payload_size = struct.calcsize("Q")
while True:
    while len(data) < payload_size:
        packet = client_socket.recv(4*1024)
        if not packet: break
        data+=packet
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("Q",packed_msg_size)[0]
    while len(data) < msg_size:
        data += client_socket.recv(4*1024)
    frame_data = data[:msg_size]
    data = data[msg_size:]
    frame = pickle.loads(frame_data)
    cv2.imshow("Recieving...",frame)
    key = cv2.waitKey(10)
    if key == 13:
        break
client_socket.close()
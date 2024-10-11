# from: https://pyshine.com/Socket-Programming-with-multiple-clients/
# video: Socket programming with multiple clients and OpenCV in Python - https://youtu.be/1skHb3IjOr4

# Welcome to PyShine
# lets make the client code
# In this code client is sending video to server
import socket, pickle, struct
import pyshine as ps  # pip install pyshine
import imutils  # pip install imutils
import cv2

camera = True
if camera == True:
    vid = cv2.VideoCapture(0)
else:
    vid = cv2.VideoCapture("1.mp4")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = "127.0.0.1"  # Here according to your server ip write the address

port = 9999
client_socket.connect((host_ip, port))

if client_socket:
    while vid.isOpened():
        try:
            img, frame = vid.read()
            frame = imutils.resize(frame, width=380)
            a = pickle.dumps(frame)
            message = struct.pack("Q", len(a)) + a
            client_socket.sendall(message)
            cv2.imshow(f"TO: {host_ip}", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                client_socket.close()
        except:
            print("VIDEO FINISHED!")
            break

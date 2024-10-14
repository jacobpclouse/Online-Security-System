# from: https://pyshine.com/Socket-Programming-with-multiple-clients/
# video: Socket programming with multiple clients and OpenCV in Python - https://youtu.be/1skHb3IjOr4

# run video mode: python 1_client.py 127.0.0.1 9999 2.mp4 
# run webcam mode: python 1_client.py 127.0.0.1 9999 

# Welcome to PyShine
# lets make the client code
# In this code client is sending video to server
import socket, pickle, struct
import pyshine as ps  # pip install pyshine
import imutils  # pip install imutils
import cv2
import sys



# importing Command line arguments - for IP and port numbers
# https://cs.stanford.edu/people/nick/py/python-main.html

def returnIPandPort():
    incomingIP = sys.argv[1]
    incomingPort = int(sys.argv[2])
    incomingTestVideo = sys.argv[3] if len(sys.argv) > 3 else None # return test video location, if nothing listed make it null
    return incomingIP,incomingPort,incomingTestVideo

incomingIP,incomingPort,incomingTestVideo = returnIPandPort()

# camera = True

# can we integrate below into lower if statement? we would just need to check if there is a webcam and exit if not
# if there isn't a sample video stream listed, then use the web camera
if incomingTestVideo == None:
    camera = True
else:
    camera = False


if camera == True:
    vid = cv2.VideoCapture(0)
else:
    vid = cv2.VideoCapture(incomingTestVideo)
    # vid = cv2.VideoCapture("20200918_180906000_iOS.mp4")



client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = incomingIP  # Here according to your server ip write the address
port = incomingPort
# host_ip = "127.0.0.1"  # Here according to your server ip write the address
# port = 9999


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
                print("Closing Socket...")
                client_socket.close()
        except:
            print("VIDEO FINISHED!")
            break

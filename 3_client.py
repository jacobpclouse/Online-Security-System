# Client Code: 3_client.py
import socket, pickle, struct
import cv2
import imutils
import sys
from datetime import datetime

# Function to retrieve IP, Port, and optional video source from command line arguments
def returnIPandPort():
    incomingIP = sys.argv[1]
    incomingPort = int(sys.argv[2])
    incomingTestVideo = sys.argv[3] if len(sys.argv) > 3 else None  # return test video location, if none listed, make it None
    return incomingIP, incomingPort, incomingTestVideo

incomingIP, incomingPort, incomingTestVideo = returnIPandPort()

# Check if using camera or a video file
camera = incomingTestVideo is None

# Initialize camera or video file for capture
if camera:
    # Try using DirectShow backend for camera (works better on Windows)
    vid = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    camera_name = "Camera_01"
    location = "Office"
else:
    vid = cv2.VideoCapture(incomingTestVideo)
    camera_name = "Camera_02"
    location = "Lunchroom"

# Check if video source is opened successfully
if not vid.isOpened():
    print("Error: Could not open video source.")
    sys.exit()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = incomingIP
port = incomingPort

client_socket.connect((host_ip, port))

# Send metadata to the server (camera name, location, start time)
metadata = {
    'camera_name': camera_name,
    'location': location,
    'start_time': str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
}
client_socket.sendall(pickle.dumps(metadata))

if client_socket:
    while vid.isOpened():
        try:
            img, frame = vid.read()
            if not img:
                print("Error: Failed to grab frame. Ending video stream.")
                break

            frame = imutils.resize(frame, width=380)
            a = pickle.dumps(frame)
            message = struct.pack("Q", len(a)) + a
            client_socket.sendall(message)

            cv2.imshow(f"TO: {host_ip}", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
        except Exception as e:
            print(f"Error: {e}")
            break

vid.release()
client_socket.close()
cv2.destroyAllWindows()

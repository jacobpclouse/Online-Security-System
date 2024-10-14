import socket, pickle, struct
import pyshine as ps  # pip install pyshine
import imutils  # pip install imutils
import cv2
import sys

from Utility_Functions.generalFunctions import myLogo, defang_datetime, createFolderIfNotExists, sanitize_filename, emptyFolder, clear_screen, eye_animation, get_private_ip


# Function to send metadata (camera name, IP, location) to server
def send_metadata(client_socket, camera_name, camera_ip, location):
    metadata = {
        "camera_name": camera_name,
        "camera_ip": camera_ip,
        "location": location
    }
    metadata_bytes = pickle.dumps(metadata)
    client_socket.sendall(struct.pack("Q", len(metadata_bytes)) + metadata_bytes)

# Function to retrieve command line arguments for IP, port, and test video
def returnIPandPort():
    incomingIP = sys.argv[1]
    incomingPort = int(sys.argv[2])
    incomingTestVideo = sys.argv[3] if len(sys.argv) > 3 else None  # return test video location, if nothing listed make it null
    return incomingIP, incomingPort, incomingTestVideo


incomingIP, incomingPort, incomingTestVideo = returnIPandPort()

# If no test video provided, use the webcam
if incomingTestVideo is None:
    camera = True
    vid = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Use DirectShow backend -- may be more reliable
    # vid = cv2.VideoCapture(0)
    # Metadata for the client -- with Camera
    camera_name = "ClientCamera1"  # Example camera name
    camera_ip = get_private_ip() 
    location = "Office_1"  # Example location
else:
    camera = False
    vid = cv2.VideoCapture(incomingTestVideo)
    # Metadata for the client -- WITHOUT Camera
    camera_name = socket.gethostname()  # Example camera name
    camera_ip = get_private_ip()  # Example camera IP (could be dynamic)
    location = "VIDEO-STREAM"  # Example location

# # Open camera or video file
# if camera:
#     vid = cv2.VideoCapture(0)
# else:
#     vid = cv2.VideoCapture(incomingTestVideo)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = incomingIP  # Server IP address
port = incomingPort

client_socket.connect((host_ip, port))

# Send metadata to server
send_metadata(client_socket, camera_name, camera_ip, location)

if client_socket:
    while vid.isOpened():
        try:
            img, frame = vid.read()
            frame = imutils.resize(frame, width=380)
            a = pickle.dumps(frame)
            message = struct.pack("Q", len(a)) + a
            client_socket.sendall(message)
            cv2.imshow(f"Camera Feed: {camera_name} -> TO: {host_ip}", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                print("Closing Socket...")
                client_socket.close()
        except:
            print("VIDEO FINISHED!")
            break

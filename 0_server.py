# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Importing Libraries / Modules
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
import socket, pickle, struct
#import imutils
import threading
import pyshine as ps  # pip install pyshine
import cv2 # pip install opencv-python
import os

from Utility_Functions.generalFunctions import myLogo, defang_datetime, createFolderIfNotExists, sanitize_filename, emptyFolder

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Functions
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
#get private ip inside network of the server computer
def get_private_ip():
    try:
        host_name = socket.gethostname()
        print(f"Computer Hostname: {host_name}")

        # Connect to an external server (Google's DNS server in this case)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        private_ip = s.getsockname()[0]
        s.close()
        return private_ip
    except Exception as e:
        return f"Unable to get IP: {e}"

# Function to handle client connection
def show_client(addr, client_socket):
    try:
        print("CLIENT {} CONNECTED!".format(addr))
        if client_socket:  # if a client socket exists
            data = b""
            payload_size = struct.calcsize("Q")
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for MP4
            out = None  # Initialize VideoWriter
            
            while True:
                while len(data) < payload_size:
                    packet = client_socket.recv(4 * 1024)  # 4K
                    if not packet:
                        break
                    data += packet
                if not data:
                    break
                packed_msg_size = data[:payload_size]
                data = data[payload_size:]
                msg_size = struct.unpack("Q", packed_msg_size)[0]

                while len(data) < msg_size:
                    data += client_socket.recv(4 * 1024)
                frame_data = data[:msg_size]
                data = data[msg_size:]
                frame = pickle.loads(frame_data)
                
                # Write text on frame for display
                text = f"CLIENT: {addr}"
                frame = ps.putBText(
                    frame,
                    text,
                    10,
                    10,
                    vspace=10,
                    hspace=1,
                    font_scale=0.7,
                    background_RGB=(255, 0, 0),
                    text_RGB=(255, 250, 250),
                )
                
                # If VideoWriter is not initialized, initialize it
                if out is None:
                    height, width, _ = frame.shape
                    # out = cv2.VideoWriter(f'client_{addr[1]}.mp4', fourcc, 20.0, (width, height))# write videoes to storage - orig
                    createFolderIfNotExists(OUTPUT_FOLDER_NAME)
                    out = cv2.VideoWriter(os.path.join(OUTPUT_FOLDER_NAME,f'client_{addr[1]}{defang_datetime()}.mp4'), fourcc, 20.0, (width, height))# write videoes to storage

                # Write frame to video file
                out.write(frame)
                
                # Display the frame
                cv2.imshow(f"FROM {addr}", frame)
                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                    break

            # Release video file after client disconnects
            if out is not None:
                out.release()
                
            client_socket.close()
    except Exception as e:
        print(f"CLIENT {addr} DISCONNECTED: {e}")
        pass


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# GLOBAL Variables
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
OUTPUT_FOLDER_NAME = 'CLIENT_VIDEO_STORAGE'  # folder where all the output files should be stored


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# MAIN
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
myLogo() 
createFolderIfNotExists(OUTPUT_FOLDER_NAME) # create a folder to store outputs in if one doesn't exist already

# for now, we use localhost or 127.0.0.1
host_ip = '127.0.0.1'
port = 9999
#host_ip = get_private_ip() # this hostname will be used later to get the host of the current computer and then use that as the host ip
print(f"HOST IP:{host_ip}, PORT: {port}")

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_address = (host_ip,port)
server_socket.bind(socket_address)
server_socket.listen()
print(f"Listening at: {socket_address}")

# Main loop to accept clients
while True:
    client_socket, addr = server_socket.accept()
    thread = threading.Thread(target=show_client, args=(addr, client_socket))
    thread.start()
    print("TOTAL CLIENTS ", threading.activeCount() - 1)

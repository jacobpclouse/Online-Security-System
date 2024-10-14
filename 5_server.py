import socket, pickle, struct
import threading
import pyshine as ps  # pip install pyshine
import cv2
import os
import json
from datetime import datetime

from Utility_Functions.generalFunctions import myLogo, defang_datetime, createFolderIfNotExists, sanitize_filename, emptyFolder, clear_screen, eye_animation

def get_metadata(camera_name, camera_ip, location, start_time, stop_time):
    """Creates a metadata dictionary"""
    metadata = {
        "camera_name": camera_name,
        "camera_ip": camera_ip,
        "location": location,
        "start_time": start_time.strftime("%Y-%m-%d %H:%M:%S"),
        "stop_time": stop_time.strftime("%Y-%m-%d %H:%M:%S")
    }
    return metadata

def save_metadata(metadata, filename):
    """Saves metadata to a JSON file"""
    with open(filename, 'w') as f:
        json.dump(metadata, f, indent=4)

def show_client(addr, client_socket):
    try:
        print(f"CLIENT {addr} CONNECTED!")
        if client_socket:
            # Receive metadata first
            metadata_size = struct.unpack("Q", client_socket.recv(struct.calcsize("Q")))[0]
            metadata_bytes = client_socket.recv(metadata_size)
            client_metadata = pickle.loads(metadata_bytes)

            print(f"Received metadata from client {addr}: {client_metadata}")
            
            camera_name = client_metadata["camera_name"]
            camera_ip = client_metadata["camera_ip"]
            location = client_metadata["location"]
            start_time = datetime.now()  # Start time
            
            data = b""
            payload_size = struct.calcsize("Q")
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for MP4
            out = None  # Initialize VideoWriter
            
            while True:
                while len(data) < payload_size:
                    packet = client_socket.recv(4 * 1024)
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
                
                # Initialize VideoWriter if not already done
                if out is None:
                    height, width, _ = frame.shape
                    createFolderIfNotExists(OUTPUT_FOLDER_NAME)
                    video_filename = os.path.join(OUTPUT_FOLDER_NAME, f'client_{addr[1]}_{defang_datetime()}.mp4')
                    out = cv2.VideoWriter(video_filename, fourcc, 20.0, (width, height))
                
                # Write frame to video file
                out.write(frame)

                # Display the frame
                cv2.imshow(f"FROM {addr}", frame)
                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                    break

            stop_time = datetime.now()  # Stop time

            # Release video file after client disconnects
            if out is not None:
                out.release()

            # Save metadata
            metadata = get_metadata(camera_name, camera_ip, location, start_time, stop_time)
            metadata_filename = video_filename.replace('.mp4', '.json')  # Save metadata with same name as video
            save_metadata(metadata, metadata_filename)

            client_socket.close()

    except Exception as e:
        print(f"CLIENT {addr} DISCONNECTED: {e}")
        pass

# Global variables and main loop remain the same
OUTPUT_FOLDER_NAME = 'CLIENT_VIDEO_STORAGE'

# Main loop
myLogo() 
createFolderIfNotExists(OUTPUT_FOLDER_NAME)
host_ip = '127.0.0.1'
port = 9999
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_address = (host_ip, port)
server_socket.bind(socket_address)
server_socket.listen()

while True:
    client_socket, addr = server_socket.accept()
    thread = threading.Thread(target=show_client, args=(addr, client_socket))
    thread.start()

import socket
import pickle
import struct
import threading
import cv2
import os
import json
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # For displaying images in Tkinter
import pyshine as ps  # pip install pyshine

# Include your existing Utility Functions
from Utility_Functions.generalFunctions import (myLogo, defang_datetime,
                                                createFolderIfNotExists, sanitize_filename,
                                                emptyFolder, clear_screen, eye_animation, get_private_ip)

OUTPUT_FOLDER_NAME = 'CLIENT_VIDEO_STORAGE'
clients = []  # Store client threads and related data
frames = {}   # Store frames for each client

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
    global frames  # Access global frames variable
    try:
        print(f"CLIENT {addr} CONNECTED!")
        if client_socket:
            # Receive metadata first
            metadata_size = struct.unpack("Q", client_socket.recv(struct.calcsize("Q")))[0]
            metadata_bytes = client_socket.recv(metadata_size)
            client_metadata = pickle.loads(metadata_bytes)

            camera_name = client_metadata["camera_name"]
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

                # Save frame for Tkinter display
                frames[addr] = frame

                # Initialize VideoWriter if not already done
                if out is None:
                    createFolderIfNotExists(OUTPUT_FOLDER_NAME)
                    filename = f'{camera_name}_loc_{location}_time_{defang_datetime()}'
                    video_filename = os.path.join(OUTPUT_FOLDER_NAME, f'{filename}.mp4')
                    out = cv2.VideoWriter(video_filename, fourcc, 20.0, (frame.shape[1], frame.shape[0]))
                
                # Write frame to video file
                out.write(frame)

            stop_time = datetime.now()  # Stop time

            # Release video file after client disconnects
            if out is not None:
                out.release()

            # Save metadata
            metadata = get_metadata(camera_name, '', location, start_time, stop_time)
            metadata_filename = video_filename.replace('.mp4', '.json')  # Save metadata with same name as video
            save_metadata(metadata, metadata_filename)

            client_socket.close()
            del frames[addr]  # Remove frame when client disconnects

    except Exception as e:
        print(f"CLIENT {addr} DISCONNECTED: {e}")
        pass

def update_display():
    """Update the displayed frames in the Tkinter window."""
    for addr, frame in frames.items():
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
        image = Image.fromarray(frame)
        photo = ImageTk.PhotoImage(image)

        # Display the frame in the Tkinter window
        label = tk.Label(video_frame, image=photo)
        label.image = photo  # Keep a reference to avoid garbage collection
        label.pack(side=tk.LEFT)  # Arrange labels side by side

    video_frame.after(33, update_display)  # Update at ~30 FPS

def start_server():
    """Start the server to accept incoming client connections."""
    host_ip = '127.0.0.1'
    port = 9999
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host_ip, port))
    server_socket.listen()

    while True:
        client_socket, addr = server_socket.accept()
        clients.append(threading.Thread(target=show_client, args=(addr, client_socket)))
        clients[-1].start()

def on_start():
    """Start the server on a separate thread."""
    threading.Thread(target=start_server, daemon=True).start()
    start_button.config(state=tk.DISABLED)  # Disable start button
    stop_button.config(state=tk.NORMAL)      # Enable stop button

def on_stop():
    """Stop the server."""
    for client in clients:
        client.join()  # Wait for all threads to finish
    messagebox.showinfo("Server Status", "Server has been stopped.")
    start_button.config(state=tk.NORMAL)  # Enable start button
    stop_button.config(state=tk.DISABLED)  # Disable stop button

# Setup Tkinter window
root = tk.Tk()
root.title("Video Stream Server")
video_frame = tk.Frame(root)
video_frame.pack()

start_button = tk.Button(root, text="Start Server", command=on_start)
start_button.pack(side=tk.LEFT)

stop_button = tk.Button(root, text="Stop Server", command=on_stop, state=tk.DISABLED)
stop_button.pack(side=tk.LEFT)

# Start the update display loop
update_display()

# Start the Tkinter event loop
root.mainloop()

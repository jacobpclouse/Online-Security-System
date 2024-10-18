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
from PIL import Image, ImageTk
import pyshine as ps  # pip install pyshine
import sqlite3  # Import SQLite library

from Utility_Functions.generalFunctions import (myLogo, defang_datetime,
                                                createFolderIfNotExists, sanitize_filename,
                                                emptyFolder, clear_screen, eye_animation, get_private_ip)

OUTPUT_FOLDER_NAME = 'CLIENT_VIDEO_STORAGE'
clients = []
frames = {}
frame_count = {}
start_time_dict = {}
createFolderIfNotExists(OUTPUT_FOLDER_NAME)

# Initialize SQLite database and create table if it doesn't exist
def init_db():
    conn = sqlite3.connect('Camera_Data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS CameraMetadata (
                    id INTEGER PRIMARY KEY,
                    camera_name TEXT,
                    camera_ip TEXT,
                    location TEXT,
                    start_time TEXT,
                    stop_time TEXT,
                    video_filename TEXT)''')
    conn.commit()
    conn.close()

def get_metadata(camera_name, camera_ip, location, start_time, stop_time, video_filename):
    """Creates a metadata dictionary"""
    metadata = {
        "camera_name": camera_name,
        "camera_ip": camera_ip,
        "location": location,
        "start_time": start_time.strftime("%Y-%m-%d %H:%M:%S"),
        "stop_time": stop_time.strftime("%Y-%m-%d %H:%M:%S"),
        "video_filename": video_filename
    }
    return metadata

def save_metadata(metadata, filename):
    """Saves metadata to a JSON file"""
    with open(filename, 'w') as f:
        json.dump(metadata, f, indent=4)

def insert_metadata_to_db(metadata):
    """Inserts metadata into the SQLite database"""
    conn = sqlite3.connect('Camera_Data.db')
    c = conn.cursor()
    c.execute('''INSERT INTO CameraMetadata (camera_name, camera_ip, location, start_time, stop_time, video_filename)
                 VALUES (?, ?, ?, ?, ?, ?)''', 
              (metadata["camera_name"], 
               metadata["camera_ip"], 
               metadata["location"], 
               metadata["start_time"], 
               metadata["stop_time"], 
               metadata["video_filename"]))
    conn.commit()
    conn.close()

def show_client(addr, client_socket):
    global frames, frame_count, start_time_dict
    try:
        print(f"CLIENT {addr} CONNECTED!")
        if client_socket:
            metadata_size = struct.unpack("Q", client_socket.recv(struct.calcsize("Q")))[0]
            metadata_bytes = client_socket.recv(metadata_size)
            client_metadata = pickle.loads(metadata_bytes)

            print(f"Received metadata from client {addr}: {client_metadata}")

            camera_name = client_metadata["camera_name"]
            location = client_metadata["location"]
            camera_ip = client_metadata["camera_ip"]
            start_time = datetime.now()
            start_time_dict[addr] = start_time  # Track start time for FPS calculation
            frame_count[addr] = 0  # Initialize frame count
            
            data = b""
            payload_size = struct.calcsize("Q")
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = None
            filename = f'{camera_name}_loc_{location}_time_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.mp4'
            video_filename = os.path.join(OUTPUT_FOLDER_NAME, filename)

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

                # Update frame count for FPS calculation
                frame_count[addr] += 1
                current_time = datetime.now()
                elapsed_time = (current_time - start_time_dict[addr]).total_seconds()
                fps = frame_count[addr] / elapsed_time if elapsed_time > 0 else 0

                # Write text on frame for display -- top text
                text = f"{camera_ip} | {current_time.strftime('%Y-%m-%d %H:%M:%S')}"
                frame = ps.putBText(
                    frame,
                    text,
                    10,
                    10,
                    vspace=10,
                    hspace=1,
                    font_scale=0.7,
                    background_RGB=(0, 0, 0),
                    text_RGB=(255, 250, 250),
                    alpha=0.5
                )

                # Metadata to display on the frame -- bottom text
                text2 = f"FPS: {fps:.2f} | CAM: {camera_name} | BLDG: {location}"
                height, width, _ = frame.shape
                text_y_position = height - 50
                frame = ps.putBText(
                    frame,
                    text2,
                    10, text_y_position,
                    vspace=5,
                    hspace=2,
                    font_scale=0.7,
                    background_RGB=(0, 0, 0),
                    text_RGB=(255, 255, 255),
                    alpha=0.5
                )

                frames[addr] = frame

                if out is None:
                    out = cv2.VideoWriter(video_filename, fourcc, 20.0, (frame.shape[1], frame.shape[0]))
                out.write(frame)

            stop_time = datetime.now()
            if out is not None:
                out.release()

            metadata = get_metadata(camera_name, camera_ip, location, start_time, stop_time, filename)
            metadata_filename = video_filename.replace('.mp4', '.json')
            save_metadata(metadata, metadata_filename)

            # Insert metadata into the database
            insert_metadata_to_db(metadata)

        del frames[addr]
        client_socket.close()

    except Exception as e:
        print(f"CLIENT {addr} DISCONNECTED: {e}")
        if addr in frames:
            del frames[addr]

def update_display():
    for addr in list(frames.keys()):
        frame = frames[addr]
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(frame_rgb)
        photo = ImageTk.PhotoImage(image)

        if addr in client_labels:
            label = client_labels[addr]
            label.config(image=photo)
            label.image = photo
        else:
            label = tk.Label(video_frame, image=photo)
            label.image = photo
            label.grid(row=len(client_labels) // 3, column=len(client_labels) % 3, padx=5, pady=5)
            client_labels[addr] = label

    for addr in list(client_labels.keys()):
        if addr not in frames:
            client_labels[addr].destroy()
            del client_labels[addr]

    video_frame.after(33, update_display)

def validate_ip_port():
    """Validates IP and port input."""
    ip = ip_entry.get()
    port = port_entry.get()
    
    try:
        socket.inet_aton(ip)  # Check if IP is valid
        if not (1024 <= int(port) <= 65535):  # Check port range
            raise ValueError
    except Exception:
        start_button.config(state=tk.DISABLED)
        return
    start_button.config(state=tk.NORMAL)

def start_server():
    """Start the server with the user-defined IP and port."""
    init_db()  # Initialize database when server starts
    eye_animation("--- === --- START SERVER LOG --- === ---")
    myLogo() 
    ip = ip_entry.get()
    port = int(port_entry.get())

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, port))
    server_socket.listen()

    ip_entry.config(state=tk.DISABLED)
    port_entry.config(state=tk.DISABLED)

    while True:
        client_socket, addr = server_socket.accept()
        client_thread = threading.Thread(target=show_client, args=(addr, client_socket))
        client_thread.daemon = True
        clients.append(client_thread)
        client_thread.start()

def on_start():
    threading.Thread(target=start_server, daemon=True).start()
    start_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)

def on_stop():
    for client in clients:
        client.join()
    messagebox.showinfo("Server Status", "Server has been stopped.")
    print("SERVER HAS BEEN STOPPED. Close out of the Tkinter window to exit!")
    start_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)

# Setup Tkinter window
root = tk.Tk()
root.title("Online Security System")

# Display private IP
private_ip_label = tk.Label(root, text=f"Private IP: {get_private_ip()}")
private_ip_label.pack()

# Start and Stop buttons at the top
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

start_button = tk.Button(button_frame, text="START SERVER", command=on_start, state=tk.DISABLED)
start_button.pack(side=tk.LEFT, padx=5)

stop_button = tk.Button(button_frame, text="STOP SERVER", command=on_stop, state=tk.DISABLED)
stop_button.pack(side=tk.LEFT, padx=5)

# Input for IP and Port
ip_port_frame = tk.Frame(root)
ip_port_frame.pack(pady=5)

ip_label = tk.Label(ip_port_frame, text="Server IP:")
ip_label.grid(row=0, column=0, padx=5, pady=5)
ip_entry = tk.Entry(ip_port_frame)
ip_entry.insert(0, "127.0.0.1")
ip_entry.grid(row=0, column=1, padx=5, pady=5)

port_label = tk.Label(ip_port_frame, text="Server Port:")
port_label.grid(row=1, column=0, padx=5, pady=5)
port_entry = tk.Entry(ip_port_frame)
port_entry.insert(0, "9999")
port_entry.grid(row=1, column=1, padx=5, pady=5)

# Validate IP and Port on change
ip_entry.bind("<KeyRelease>", lambda _: validate_ip_port())
port_entry.bind("<KeyRelease>", lambda _: validate_ip_port())

# Video frame to display video feeds
video_frame = tk.Frame(root)
video_frame.pack(pady=10)

client_labels = {}

# Start updating display
update_display()

# Run the Tkinter event loop
root.mainloop()

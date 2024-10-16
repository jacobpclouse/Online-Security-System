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

OUTPUT_FOLDER_NAME = 'CLIENT_VIDEO_STORAGE'
clients = []
frames = {}

# add back in animations, add back in overlay
# put buttons on top with the ip entries
# localhost doesn't work initially until you add a character and remove a char
# add framerate to the display

def get_private_ip():
    """Gets the private IP of the server computer"""
    try:
        host_name = socket.gethostname()
        print(f"Computer Hostname: {host_name}")
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        private_ip = s.getsockname()[0]
        s.close()
        return private_ip
    except Exception as e:
        return f"Unable to get IP: {e}"

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
    global frames
    try:
        print(f"CLIENT {addr} CONNECTED!")
        if client_socket:
            metadata_size = struct.unpack("Q", client_socket.recv(struct.calcsize("Q")))[0]
            metadata_bytes = client_socket.recv(metadata_size)
            client_metadata = pickle.loads(metadata_bytes)

            camera_name = client_metadata["camera_name"]
            location = client_metadata["location"]
            start_time = datetime.now()
            
            data = b""
            payload_size = struct.calcsize("Q")
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = None
            
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

                frames[addr] = frame

                if out is None:
                    filename = f'{camera_name}_loc_{location}_time_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.mp4'
                    video_filename = os.path.join(OUTPUT_FOLDER_NAME, filename)
                    out = cv2.VideoWriter(video_filename, fourcc, 20.0, (frame.shape[1], frame.shape[0]))
                
                out.write(frame)

            stop_time = datetime.now()
            if out is not None:
                out.release()

            metadata = get_metadata(camera_name, '', location, start_time, stop_time)
            metadata_filename = video_filename.replace('.mp4', '.json')
            save_metadata(metadata, metadata_filename)

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
            label.pack(side=tk.LEFT)
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
    start_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)

# Setup Tkinter window
root = tk.Tk()
root.title("Video Stream Server")

# Display private IP
private_ip_label = tk.Label(root, text=f"Private IP: {get_private_ip()}")
private_ip_label.pack()

# Input for IP
ip_label = tk.Label(root, text="Server IP:")
ip_label.pack()
ip_entry = tk.Entry(root)
ip_entry.insert(0, "127.0.0.1")
ip_entry.pack()

# Input for Port
port_label = tk.Label(root, text="Server Port:")
port_label.pack()
port_entry = tk.Entry(root)
port_entry.insert(0, "9999")
port_entry.pack()

# Validate IP and port input as user types
ip_entry.bind("<KeyRelease>", lambda event: validate_ip_port())
port_entry.bind("<KeyRelease>", lambda event: validate_ip_port())

# Video display frame
video_frame = tk.Frame(root)
video_frame.pack()

client_labels = {}

# Start and Stop buttons
start_button = tk.Button(root, text="Start Server", command=on_start, state=tk.DISABLED)
start_button.pack(side=tk.LEFT)

stop_button = tk.Button(root, text="Stop Server", command=on_stop, state=tk.DISABLED)
stop_button.pack(side=tk.LEFT)

# Update the display loop
update_display()

# Start the Tkinter event loop
root.mainloop()

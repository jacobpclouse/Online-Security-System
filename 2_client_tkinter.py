import socket
import pickle
import struct
import threading
import cv2
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import imutils  # pip install imutils

def get_private_ip():
    """Gets the private IP of the client computer"""
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

def returnIPandPort():
    ip = ip_entry.get()
    port = int(port_entry.get())
    return ip, port

def send_metadata(client_socket, camera_name, camera_ip, location):
    metadata = {
        "camera_name": camera_name,
        "camera_ip": camera_ip,
        "location": location
    }
    metadata_bytes = pickle.dumps(metadata)
    client_socket.sendall(struct.pack("Q", len(metadata_bytes)) + metadata_bytes)

def start_client():
    ip, port = returnIPandPort()
    incomingTestVideo = video_path if video_var.get() == 'Video' else None
    vid = None
    camera = False

    # If webcam is selected
    if incomingTestVideo is None:
        camera = True
        selected_webcam_index = webcam_dropdown.current()  # Selected webcam index
        vid = cv2.VideoCapture(selected_webcam_index)
    else:
        vid = cv2.VideoCapture(incomingTestVideo)

    # Set up client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip, port))

    # Send metadata to server
    send_metadata(client_socket, "ClientCamera", get_private_ip(), "Office_1")

    def stream_video():
        while vid.isOpened():
            try:
                img, frame = vid.read()
                if frame is None:
                    break
                frame = imutils.resize(frame, width=720)
                a = pickle.dumps(frame)
                message = struct.pack("Q", len(a)) + a
                client_socket.sendall(message)

                # Display the frame in the Tkinter window
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img_tk = ImageTk.PhotoImage(Image.fromarray(frame_rgb))
                video_label.config(image=img_tk)
                video_label.image = img_tk  # Keep a reference to avoid garbage collection

                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                    break
            except:
                break
        client_socket.close()

    # Disable IP, port, and video/webcam choice after starting
    ip_entry.config(state=tk.DISABLED)
    port_entry.config(state=tk.DISABLED)
    webcam_dropdown.config(state=tk.DISABLED)
    video_button.config(state=tk.DISABLED)
    video_option_menu.config(state=tk.DISABLED)

    # Start video streaming in a separate thread
    threading.Thread(target=stream_video, daemon=True).start()

def stop_client():
    messagebox.showinfo("Client Status", "Client has stopped streaming.")
    root.quit()

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

def choose_video():
    global video_path
    video_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4")])
    if video_path:
        video_button.config(text="Video selected")

def toggle_webcam_video_options(*args):
    if video_var.get() == "Webcam":
        webcam_dropdown.config(state=tk.NORMAL)
        video_button.config(state=tk.DISABLED)
    else:
        webcam_dropdown.config(state=tk.DISABLED)
        video_button.config(state=tk.NORMAL)

# Initialize Tkinter window
root = tk.Tk()
root.title("Client Video Stream")

# Display client's private IP
private_ip_label = tk.Label(root, text=f"Private IP: {get_private_ip()}")
private_ip_label.pack()

# Start and Stop buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

start_button = tk.Button(button_frame, text="START CLIENT", command=start_client, state=tk.DISABLED)
start_button.pack(side=tk.LEFT, padx=5)

stop_button = tk.Button(button_frame, text="STOP CLIENT", command=stop_client)
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

# Validate IP and port input as user types
ip_entry.bind("<KeyRelease>", lambda event: validate_ip_port())
port_entry.bind("<KeyRelease>", lambda event: validate_ip_port())

# Webcam or Video Selection
video_var = tk.StringVar(value="Webcam")
video_option_menu = tk.OptionMenu(root, video_var, "Webcam", "Video", command=toggle_webcam_video_options)
video_option_menu.pack(pady=5)

# Webcam Selection Dropdown
webcam_frame = tk.Frame(root)
webcam_frame.pack(pady=5)
webcam_label = tk.Label(webcam_frame, text="Select Webcam:") # NEED TO GET LOGIC to search for webcams and only display the ones we find, otherwise (if just one) default to that one
webcam_label.grid(row=0, column=0, padx=5, pady=5)

webcam_list = [f"Webcam {i}" for i in range(0, 3)]  # Dummy webcam list, replace with actual
webcam_dropdown = ttk.Combobox(webcam_frame, values=webcam_list, state="readonly")
webcam_dropdown.grid(row=0, column=1, padx=5, pady=5)
webcam_dropdown.current(0)

# Video File Selection Button
video_button = tk.Button(root, text="Choose Video", command=choose_video, state=tk.DISABLED)
video_button.pack(pady=5)

# Video display frame
video_frame = tk.Frame(root)
video_frame.pack()

video_label = tk.Label(video_frame)
video_label.pack()

# Start the Tkinter event loop
root.mainloop()

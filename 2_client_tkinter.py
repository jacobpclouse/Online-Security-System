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
import pyshine as ps

# Get available webcams
def get_available_webcams():
    print('--- === --- === ------ === --- === ------ === --- === ---')
    print('> HEY! You may see some error messages, this because open cv is looking to see what cameras are available')
    print('--- === --- === ------ === --- === ------ === --- === ---')
    
    webcams = []
    for i in range(10):  # Check the first 10 indices
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            webcams.append(i)
            cap.release()  # Release the camera
    print('--- === --- === ------ === --- === ------ === --- === ---')
    print('> OK! Should be done with the error messages!')
    print('--- === --- === ------ === --- === ------ === --- === ---')

    return webcams

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
    location = location_entry.get()  # Get the location from the new entry
    return ip, port, location  # Return location as well

def send_metadata(client_socket, camera_name, camera_ip, location):
    metadata = {
        "camera_name": camera_name,
        "camera_ip": camera_ip,
        "location": location
    }
    metadata_bytes = pickle.dumps(metadata)
    client_socket.sendall(struct.pack("Q", len(metadata_bytes)) + metadata_bytes)

def start_client():
    ip, port, location = returnIPandPort()  # Get location here
    if not location:  # Check if location is provided
        messagebox.showerror("Input Error", "Building location is mandatory.")
        return
    
    incomingTestVideo = video_path if video_var.get() == 'Video' else None
    vid = None
    camera = False

    # If webcam is selected
    if incomingTestVideo is None:
        camera = True
        selected_webcam_value = webcam_dropdown.get()  # Get the selected webcam value
        selected_webcam_split = int(selected_webcam_value.split(' ')[-1])  # Extract the index from the value
        vid = cv2.VideoCapture(selected_webcam_split)
    else:
        vid = cv2.VideoCapture(incomingTestVideo)

    # Set up client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Attempt to connect to the server with reconnection logic
    for attempt in range(5):
        try:
            client_socket.connect((ip, port))
            break  # Exit loop if connection is successful
        except Exception:
            reconnect_label.config(text=f"RECONNECTING, attempt number {attempt + 1}")
            root.update()  # Update the Tkinter window
            threading.Event().wait(1)  # Wait for 1 second before retrying
    else:
        messagebox.showerror("Connection Error", "Failed to connect to the server after 5 attempts.")
        return

    # Send metadata to server
    if incomingTestVideo is None:
        send_metadata(client_socket, selected_webcam_value, get_private_ip(), location)  # Use the location from user input
    else:
        send_metadata(client_socket, socket.gethostname(), get_private_ip(), "VIDEO-STREAM")

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

                # Draw a red outline around the frame -- TO SHOW WHEN RECORDING!
                cv2.rectangle(frame, (5, 5), (715, 515), (0, 0, 250), 4)

                # Display the frame in the Tkinter window
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img_tk = ImageTk.PhotoImage(Image.fromarray(frame_rgb))
                video_label.config(image=img_tk)
                video_label.image = img_tk  # Keep a reference to avoid garbage collection

                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                    break
            except Exception as e:
                print(f"Error while streaming: {e}")
                break
        client_socket.close()

    # Disable IP, port, and video/webcam choice after starting
    ip_entry.config(state=tk.DISABLED)
    port_entry.config(state=tk.DISABLED)
    webcam_dropdown.config(state=tk.DISABLED)
    video_button.config(state=tk.DISABLED)
    video_option_menu.config(state=tk.DISABLED)
    location_entry.config(state=tk.DISABLED)  # Disable location entry as well

    # Start video streaming in a separate thread
    threading.Thread(target=stream_video, daemon=True).start()

def preview_video(selected_webcam_index):
    """Function to display a preview of the selected webcam for 20 seconds."""
    preview_vid = cv2.VideoCapture(selected_webcam_index)

    def show_preview():
        for _ in range(20):  # Show preview for 20 seconds
            ret, frame = preview_vid.read()
            if not ret:
                break

            # Overlay the "PREVIEW" text on the frame
            text = f"PREVIEW"
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

            # Display the frame in the Tkinter window
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img_tk = ImageTk.PhotoImage(Image.fromarray(frame_rgb))
            video_label.config(image=img_tk)
            video_label.image = img_tk  # Keep a reference to avoid garbage collection

            cv2.waitKey(50)  # Display each frame for a short time

        preview_vid.release()

    # Start the preview in a separate thread
    threading.Thread(target=show_preview, daemon=True).start()

def start_preview():
    selected_webcam_value = webcam_dropdown.get()  # Get the selected webcam value
    selected_webcam_split = int(selected_webcam_value.split(' ')[-1])  # Extract the index from the value
    preview_video(selected_webcam_split)

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
        preview_button.config(state=tk.NORMAL)  # Enable preview button
    else:
        webcam_dropdown.config(state=tk.DISABLED)
        video_button.config(state=tk.NORMAL)
        preview_button.config(state=tk.DISABLED)  # Disable preview button

# Initialize Tkinter window
root = tk.Tk()
root.title("Client Video Stream")

# Display client's private IP
private_ip_label = tk.Label(root, text=f"Private IP: {get_private_ip()}")
private_ip_label.pack()

# Reconnection label
reconnect_label = tk.Label(root, text="")
reconnect_label.pack()

# Start and Stop buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

start_button = tk.Button(button_frame, text="START CLIENT", command=start_client, state=tk.DISABLED)
start_button.pack(side=tk.LEFT, padx=5)

stop_button = tk.Button(button_frame, text="STOP CLIENT", command=stop_client)
stop_button.pack(side=tk.LEFT, padx=5)

# Input for IP, Port, and Location
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

# New Location Entry
location_label = tk.Label(ip_port_frame, text="Building Location:")
location_label.grid(row=2, column=0, padx=5, pady=5)
location_entry = tk.Entry(ip_port_frame)
location_entry.grid(row=2, column=1, padx=5, pady=5)

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
webcam_label = tk.Label(webcam_frame, text="Select Webcam:")
webcam_label.grid(row=0, column=0, padx=5, pady=5)

save_these = get_available_webcams()
webcam_list = [f"Webcam {i}" for i in save_these]  # Dummy webcam list, replace with actual
webcam_dropdown = ttk.Combobox(webcam_frame, values=webcam_list, state="readonly")
webcam_dropdown.grid(row=0, column=1, padx=5, pady=5)
webcam_dropdown.current(0)

# Preview Button
preview_button = tk.Button(webcam_frame, text="Preview", command=start_preview, state=tk.NORMAL)
preview_button.grid(row=0, column=2, padx=5, pady=5)

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

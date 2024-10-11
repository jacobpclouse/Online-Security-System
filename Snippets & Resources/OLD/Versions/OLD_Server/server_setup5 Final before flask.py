# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Importing Libraries / Modules
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
import cv2
import socket
import pickle
import struct
import datetime

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Functions
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# --- Function to print out my Logo ---
def myLogo():
    print("Created and Tested by: ")
    print("   __                  _         ___ _                       ")
    print("   \ \  __ _  ___ ___ | |__     / __\ | ___  _   _ ___  ___  ")
    print("    \ \/ _` |/ __/ _ \| '_ \   / /  | |/ _ \| | | / __|/ _ \ ")
    print(" /\_/ / (_| | (_| (_) | |_) | / /___| | (_) | |_| \__ \  __/ ")
    print(" \___/ \__,_|\___\___/|_.__/  \____/|_|\___/ \__,_|___/\___| ")
    print("Dedicated to Peter Zlomek & Harely Alderson III")
    print("\n")


# --- Function to Defang date time ---
def defang_datetime():
    current_datetime = f"_{datetime.datetime.now()}"

    current_datetime = current_datetime.replace(":", "_")
    current_datetime = current_datetime.replace(".", "-")
    current_datetime = current_datetime.replace(" ", "_")

    return current_datetime


# --- Function to organize frames and handle disconnection ---
def send_frame(conn, frame):
    # Serialize the frame
    data = pickle.dumps(frame)
    # Pack the serialized frame and send its size
    message = struct.pack("Q", len(data)) + data
    try:
        # Send the frame to the client
        conn.sendall(message)
    except (ConnectionAbortedError, ConnectionResetError, OSError):
        # Close the connection if an error occurs
        print("Client disconnected")
        conn.close()


# --- MAIN function ---
def main():
    # Initialize the server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 8000))
    server_socket.listen(5)
    print("Server started, waiting for client connection...")

    # Accept a client connection
    conn, addr = server_socket.accept()
    print("Client connected:", addr)

    # Open the camera
    camera = cv2.VideoCapture(0)

    # Get the video dimensions and initialize the video writer
    width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = 30
    video_writer = cv2.VideoWriter('streamed_video.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    while True:
        # Read a frame from the camera
        _, frame = camera.read()

        # Write the frame to the video file
        video_writer.write(frame)

        # Send the frame to the client
        send_frame(conn, frame)

        # Break the loop if 'q' is pressed or client disconnects
        if cv2.waitKey(1) == ord('q') or conn.fileno() == -1:
            break

    # Release the camera, close the connection, and release the video writer
    camera.release()
    conn.close()
    video_writer.release()


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# MAIN
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
if __name__ == '__main__':
    main()

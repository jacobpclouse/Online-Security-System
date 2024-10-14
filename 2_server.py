# Server Code: 2_server.py
import socket, pickle, struct
import threading
import cv2
import os
from datetime import datetime
import pyshine as ps  # pip install pyshine

from Utility_Functions.generalFunctions import myLogo, defang_datetime, createFolderIfNotExists, sanitize_filename, emptyFolder, clear_screen, eye_animation

# need to adjust -
# put back the text on screen with the location and ip
# redo it so it stores the video clips in the client video storage
# make sure you can programatically access the data for the client data with python (if you can't directly access it from the videos, store it with a db and link it using filename)

# Function to handle client connection and stream video
def show_client(addr, client_socket):
    try:
        print(f"CLIENT {addr} CONNECTED!")
        if client_socket:
            data = b""
            payload_size = struct.calcsize("Q")
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = None

            # Receive metadata from the client
            metadata_pickle = client_socket.recv(4 * 1024)
            metadata = pickle.loads(metadata_pickle)
            print(f"Received Metadata: {metadata}")

            while True:
                try:
                    while len(data) < payload_size:
                        packet = client_socket.recv(4 * 1024)
                        if not packet:
                            print(f"CLIENT {addr} DISCONNECTED: No more data.")
                            return  # Gracefully handle disconnection
                        data += packet

                    packed_msg_size = data[:payload_size]
                    data = data[payload_size:]
                    msg_size = struct.unpack("Q", packed_msg_size)[0]

                    while len(data) < msg_size:
                        data += client_socket.recv(4 * 1024)
                    frame_data = data[:msg_size]
                    data = data[msg_size:]
                    frame = pickle.loads(frame_data)


                    # Write text on frame for display --
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
                    ) # ---


                    # Initialize VideoWriter only once, with the metadata information in the filename
                    if out is None:
                        height, width, _ = frame.shape
                        output_filename = f"{metadata['camera_name']}_{metadata['location']}_{metadata['start_time'].replace(':', '-')}.mp4"
                        out = cv2.VideoWriter(os.path.join(OUTPUT_FOLDER_NAME,output_filename), fourcc, 20.0, (width, height))
                        # out = cv2.VideoWriter(output_filename, fourcc, 20.0, (width, height))

                    # Write frame to video file
                    out.write(frame)

                    # Display the frame
                    cv2.imshow(f"FROM {addr}", frame)

                    key = cv2.waitKey(1) & 0xFF
                    if key == ord('q'):
                        print("Stopping Server...")
                        break

                except socket.error as e:
                    print(f"Socket error: {e}")
                    break

        print(f"CLIENT {addr} DISCONNECTED: Closing connection.")
        if client_socket:
            client_socket.close()
        if out:
            out.release()
        cv2.destroyAllWindows()

    except Exception as e:
        print(f"CLIENT {addr} ERROR: {e}")
        pass

# Main server code to accept clients
def start_server(host_ip='127.0.0.1', port=9999):
    createFolderIfNotExists(OUTPUT_FOLDER_NAME)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_address = (host_ip, port)
    server_socket.bind(socket_address)
    server_socket.listen()

    print(f"HOST IP: {host_ip}, PORT: {port}")
    print(f"Listening at: {socket_address}")

    while True:
        client_socket, addr = server_socket.accept()
        thread = threading.Thread(target=show_client, args=(addr, client_socket))
        thread.start()
        print("TOTAL CLIENTS ", threading.active_count() - 1)


OUTPUT_FOLDER_NAME = 'CLIENT_VIDEO_STORAGE'  # folder where all the output files should be stored

if __name__ == "__main__":
    eye_animation()
    myLogo() 
    createFolderIfNotExists(OUTPUT_FOLDER_NAME) # create a folder to store outputs in if one doesn't exist already
    start_server()

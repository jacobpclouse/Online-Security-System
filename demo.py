# Written by Jacob Clouse 
# Edited on Windows 10 - may need to be edited if you want to use on Linux/MacOS

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Importing Libraries / Modules
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
import datetime
import glob
import io
import os
# moving files and folders
import shutil  # used to move files around and clean folders
import zipfile  # used in zipping images
import numpy as np  # used to store actual encrypted data in a file and retrieve it
from PIL import Image

# video imports
import cv2
import socket
import pickle
import struct
from multiprocessing import Process

# Backend imports
from flask import Flask, request, send_file, \
    jsonify  # for web back end
from flask_cors import CORS



# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Variables
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

demo = Flask(__name__)
# without cors, app will refuse the requests from the frontend
Cors = CORS(demo)
CORS(demo, resources={r'/*': {'origins': '*'}})
demo.config['CORS_HEADERS'] = 'Content-Type'






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


# --- *** Function to organize video frames (VIDEO) *** ---
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


# --- *** Function to setup video stream (VIDEO) *** ---
def video_stream():
    # Initialize the server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 8000))
    server_socket.listen(5)
    print("Server started, waiting for client connection...")

    # Accept a client connection
    conn, addr = server_socket.accept()
    print("Client connected:", addr)
    current_datetime = defang_datetime()

    # Open the camera
    camera = cv2.VideoCapture(0)

    # Get the video dimensions and initialize the video writer
    width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = 30
    video_writer = cv2.VideoWriter(f'streamed_video_{current_datetime}.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    while True:
        # Read a frame from the camera
        _, frame = camera.read()

        # Write the frame to the video file
        video_writer.write(frame)

        # Send the frame to the client
        send_frame(conn, frame)

        # Break the loop if client disconnects
        if conn.fileno() == -1:
            break

    # Release the camera, close the connection, and release the video writer
    camera.release()
    conn.close()
    video_writer.release()


# # --- Function to read data into variable from bin ---
# def read_enck_to_variable(textName):
#     with open(textName, 'rb') as f:
#         my_bytes_object = f.read()
#     return my_bytes_object


# --- Function to empty out a directory ---
def clean_out_directory(folderPath):
    for filename in os.listdir(folderPath):
        filePath = os.path.join(folderPath, filename)
        try:
            if os.path.isfile(filePath):
                os.unlink(filePath)
        except Exception as e:
            print(f"Failed to delete {filePath} due to {e}")


# --- Function to check and see if a directory exists and, if not, create that directory ---
def create_folder(folderPath):
    if not os.path.exists(folderPath):
        os.makedirs(folderPath)


# -- Function that takes zip name and then an array of files to zip
def zip_files(zip_name, files_to_zip):
    with zipfile.ZipFile(zip_name, 'w') as zip_file:
        # Add each file to the zip file
        for file_path in files_to_zip:
            # Add the file to the zip file with its original name
            zip_file.write(file_path, arcname=file_path.split('/')[-1])


# --- Function that unzips files from zip file ---
def unzip_files(zip_name):
    # Create a ZipFile object with the name of the zip file and mode 'r' for read
    with zipfile.ZipFile(zip_name, mode='r') as zip_obj:
        # Print a list of all files in the zip file
        print("Files in zip file:")
        for file_name in zip_obj.namelist():
            print(f"- {file_name}")
        # Extract all files to the current working directory
        zip_obj.extractall()



# --- Function to remove unneeded zip files ---
def delete_zip_file(extraZip):
    if os.path.exists(extraZip) and extraZip.endswith('.zip'):
        os.remove(extraZip)
        print(f"{extraZip} has been deleted.")


# --- Function to get extension for retrieval --
def need_extension(filename):
    name, extension = filename.split(".")
    upperCaseExt = extension.upper()  
    print(upperCaseExt)
    return upperCaseExt


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Routes
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
@demo.route('/')
def start_video_stream():
    myLogo()
    # Start the video streaming process
    p = Process(target=video_stream)
    p.start()
    return "Video streaming started."



# -------------------------------------
# main statement - used to set dev mode and do auto reloading - remove this before going to production
# -------------------------------------
if __name__ == '__main__':
    demo.run(debug=True)


'''
created a flask server to handle the video streams, just need to adjust this so that we dont need a webpage open to allow the streams, allow multiple streams, name cameras, save videos to specific file locations, associate specific cameras with specific streams, etc

## IDEA: add numbers in routes, so we can associate specific routes with specific cameras
spawn subprocesses so that we can have multiple threads that are not tied to one another
'''
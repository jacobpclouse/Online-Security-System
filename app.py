import cv2
import socket
import pickle
import struct
from multiprocessing import Process
from flask import Flask

app = Flask(__name__)

class CameraStream:
    def __init__(self, camera_id):
        self.camera_id = camera_id
        self.process = None

    def start(self):
        if self.process is None or not self.process.is_alive():
            self.process = Process(target=self.video_stream)
            self.process.start()

    def video_stream(self):
        # Initialize the server socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('0.0.0.0', 8000))
        server_socket.listen(5)
        print(f"Camera {self.camera_id}: Server started, waiting for client connection...")

        # Accept a client connection
        conn, addr = server_socket.accept()
        print(f"Camera {self.camera_id}: Client connected:", addr)

        # Open the camera
        camera = cv2.VideoCapture(self.camera_id)

        # Get the video dimensions and initialize the video writer
        width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = 30
        video_writer = cv2.VideoWriter(f'streamed_video_{self.camera_id}.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

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

@app.route('/')
def start_video_streams():
    # Start the camera streams
    for camera_id in range(2):
        camera_stream = CameraStream(camera_id)
        camera_stream.start()

    return "Video streaming started for multiple cameras."

if __name__ == '__main__':
    app.run()

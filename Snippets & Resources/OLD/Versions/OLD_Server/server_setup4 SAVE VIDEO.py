import cv2
import socket
import pickle
import struct

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

if __name__ == '__main__':
    main()

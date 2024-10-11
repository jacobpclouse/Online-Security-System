import cv2
import socket
import pickle
import struct

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

    while True:
        # Read a frame from the camera
        _, frame = camera.read()

        # Check if the client is still connected
        if conn.fileno() == -1:
            print("Client disconnected")
            break

        try:
            # Serialize the frame
            data = pickle.dumps(frame)
            # Pack the serialized frame and send its size
            message = struct.pack("Q", len(data)) + data
            # Send the frame to the client
            conn.sendall(message)
        except (ConnectionAbortedError, ConnectionResetError, OSError):
            # Close the connection if an error occurs
            print("Client disconnected")
            break

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) == ord('q'):
            break

    # Release the camera and close the server socket
    camera.release()
    server_socket.close()

if __name__ == '__main__':
    main()

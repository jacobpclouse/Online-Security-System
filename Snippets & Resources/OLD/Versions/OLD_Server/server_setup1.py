import cv2
import socket
import pickle

def save_camera_feed():
    # Open camera
    cap = cv2.VideoCapture(0)

    # Define the codec and create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('camera_feed.avi', fourcc, 20.0, (640, 480))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Save the frame
        out.write(frame)

    # Release resources
    cap.release()
    out.release()

def run_server():
    host = ''  # Bind to all available interfaces
    port = 12345

    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a specific address and port
    server_socket.bind((host, port))

    # Listen for incoming connections
    server_socket.listen(1)

    print("Server is running and waiting for a client connection...")

    while True:
        # Accept a client connection
        client_socket, addr = server_socket.accept()
        print("Client connected:", addr)

        # Save camera feed
        save_camera_feed()

        # Send a notification to the client
        message = "Camera feed saved successfully!"
        client_socket.sendall(message.encode())

        # Close the connection
        client_socket.close()

        # Exit the loop to only serve one client at a time
        break

    # Close the server socket
    server_socket.close()

if __name__ == '__main__':
    run_server()

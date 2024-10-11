import cv2
import socket

def display_camera_feed():
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Define the server address and port
    server_address = ('localhost', 12345)

    # Connect to the server
    client_socket.connect(server_address)
    print("Connected to server.")

    # Receive the notification from the server
    message = client_socket.recv(1024).decode()
    print("Server message:", message)

    # Start reading the saved camera feed
    cap = cv2.VideoCapture('camera_feed.avi')

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Display the frame
        cv2.imshow('Camera Feed', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()

    # Close the client socket
    client_socket.close()

if __name__ == '__main__':
    display_camera_feed()

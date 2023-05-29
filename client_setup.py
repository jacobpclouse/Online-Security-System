import cv2
import socket
import pickle
import struct
import keyboard

def main():
    # Initialize the client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 8000))

    # Receive the frame from the server and display it
    data = b""
    payload_size = struct.calcsize("Q")
    while True:
        while len(data) < payload_size:
            packet = client_socket.recv(4 * 1024)  # 4KB
            if not packet:
                break
            data += packet
        if not data:
            break
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]
        while len(data) < msg_size:
            data += client_socket.recv(4 * 1024)
        frame_data = data[:msg_size]
        data = data[msg_size:]
        frame = pickle.loads(frame_data)
        cv2.imshow('Client Stream', frame)
        cv2.waitKey(1)

        # Check if 'q' is pressed
        if keyboard.is_pressed('q'):
            break

    # Close the client socket
    client_socket.close()

if __name__ == '__main__':
    main()

import socket

def main():
    # Initialize the client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 8000))

    # Send the shutdown command to the server
    client_socket.sendall(b"shutdown")

    # Close the client socket
    client_socket.close()

if __name__ == '__main__':
    main()

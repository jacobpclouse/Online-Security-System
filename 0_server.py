import socket, pickle, struct
#import imutils
import threading
import pyshine as ps  # pip install pyshine
import cv2

#get private ip inside network of the server computer
def get_private_ip():
    try:
        host_name = socket.gethostname()
        print(f"Computer Hostname: {host_name}")

        # Connect to an external server (Google's DNS server in this case)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        private_ip = s.getsockname()[0]
        s.close()
        return private_ip
    except Exception as e:
        return f"Unable to get IP: {e}"

# this hostname will be used later to get the host of the current computer and then use that as the host ip
# for now, we use localhost or 127.0.0.1

# host_ip = socket.gethostbyname(host_name) # will not get the correct ip, gets sever IP
host_ip = get_private_ip()
print("HOST IP:", host_ip)


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 9999
socket_address = (host_ip,port) # when deploying to a real server, use this -- gets wrong ip? gets ip of network?
#socket_address = ("127.0.0.1", port)
# socket_address = ("192.168.1.4", port) # for private ip, the other

server_socket.bind(socket_address)
server_socket.listen()
print(f"Listening at: {socket_address}")

# Function to handle client connection
def show_client(addr, client_socket):
    try:
        print("CLIENT {} CONNECTED!".format(addr))
        if client_socket:  # if a client socket exists
            data = b""
            payload_size = struct.calcsize("Q")
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for MP4
            out = None  # Initialize VideoWriter
            
            while True:
                while len(data) < payload_size:
                    packet = client_socket.recv(4 * 1024)  # 4K
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
                
                # Write text on frame for display
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
                )
                
                # If VideoWriter is not initialized, initialize it
                if out is None:
                    height, width, _ = frame.shape
                    out = cv2.VideoWriter(f'client_{addr[1]}.mp4', fourcc, 20.0, (width, height))

                # Write frame to video file
                out.write(frame)
                
                # Display the frame
                cv2.imshow(f"FROM {addr}", frame)
                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                    break

            # Release video file after client disconnects
            if out is not None:
                out.release()
                
            client_socket.close()
    except Exception as e:
        print(f"CLIENT {addr} DISCONNECTED: {e}")
        pass

# Main loop to accept clients
while True:
    client_socket, addr = server_socket.accept()
    thread = threading.Thread(target=show_client, args=(addr, client_socket))
    thread.start()
    print("TOTAL CLIENTS ", threading.activeCount() - 1)

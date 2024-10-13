import socket

# host_ip = socket.gethostbyname(host_name) # will not get the correct ip, gets sever IP

def get_private_ip():
    try:
        # Connect to an external server (Google's DNS server in this case)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        private_ip = s.getsockname()[0]
        s.close()
        return private_ip
    except Exception as e:
        return f"Unable to get IP: {e}"

if __name__ == "__main__":
    print("Private IP Address:", get_private_ip())

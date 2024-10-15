import datetime
import os
import re
from pathlib import Path # used to delete old files in folder
import time
import socket

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

# --- Function to print out my Logo ---
def myLogo():
    
    print("Welcome to your very own:")
    print("   ____        _ _               _____                      _ _            _____           _                 ")
    print("  / __ \      | (_)             / ____|                    (_) |          / ____|         | |                ")
    print(" | |  | |_ __ | |_ _ __   ___  | (___   ___  ___ _   _ _ __ _| |_ _   _  | (___  _   _ ___| |_ ___ _ __ ___  ")
    print(" | |  | | '_ \| | | '_ \ / _ \  \___ \ / _ \/ __| | | | '__| | __| | | |  \___ \| | | / __| __/ _ \ '_ ` _ \ ")
    print(" | |__| | | | | | | | | |  __/  ____) |  __/ (__| |_| | |  | | |_| |_| |  ____) | |_| \__ \ ||  __/ | | | | |")
    print("  \____/|_| |_|_|_|_| |_|\___| |_____/ \___|\___|\__,_|_|  |_|\__|\__, | |_____/ \__, |___/\__\___|_| |_| |_|")
    print("                                                                   __/ |          __/ |                      ")
    print("                                                                  |___/          |___/                       ")
    print("Safety through Vigilance! Dedicated to Mary Clouse and Harley Alderson III")



# --- Function to Defang date time ---
def defang_datetime():
    current_datetime = f"_{datetime.datetime.now()}"

    current_datetime = current_datetime.replace(":", "_")
    current_datetime = current_datetime.replace(".", "-")
    current_datetime = current_datetime.replace(" ", "_")

    return current_datetime


# --- Function to create a folder if it does not exist ---
def createFolderIfNotExists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Folder '{folder_path}' created successfully.")
    else:
        print(f"Folder '{folder_path}' already exists.")

# Take out any invalid characters for a filename
def sanitize_filename(filename: str) -> str:
    # Replace invalid characters with an underscore
    sanitized = re.sub(r'[\/:*?"<>|]', '_', filename)
    # Optionally strip leading/trailing spaces and dots
    sanitized = sanitized.strip().strip('.')
    return sanitized


# --- Function to delete files inside directory (without deleting directory itself) ---
def emptyFolder(directoryPath):
    [f.unlink() for f in Path(directoryPath).glob("*") if f.is_file()] 

def clear_screen():
    # Clears the terminal screen
    os.system('cls' if os.name == 'nt' else 'clear')

def eye_animation():
    # got eye template from: https://emojicombos.com/eye-ascii-art
    frames = [
        '''
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣤⣤⣤⣤⣴⣤⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣀⣴⣾⠿⠛⠋⠉⠁⠀⠀⠀⠈⠙⠻⢷⣦⡀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣤⣾⡿⠋⠁⠀⣠⣶⣿⡿⢿⣷⣦⡀⠀⠀⠀⠙⠿⣦⣀⠀⠀⠀⠀
⠀⠀⢀⣴⣿⡿⠋⠀⠀⢀⣼⣿⣿⣿  ⢻⣽⣿⡆⠀⠀⠀⠀⢻⣿⣷⣶⣄⠀
⠀⣴⣿⣿⠋⠀⠀⠀⠀⠸⣿⣿⣿⣿  ⢸⣿⣿⣿⠀⠀⠀⠐⡄⡌⢻⣿⣿⡷
⢸⣿⣿⠃⢂⡋⠄⠀⠀⠀⢿⣿⣿⣿ ⣴⣯⣿⣿⠏⠀⠀⠀⠀⢦⣷⣿⠿⠛⠁
⠀⠙⠿⢾⣤⡈⠙⠂⢤⢀⠀⠙⠿⢿⣿⣿⡿⠟⠁⠀⣀⣀⣤⣶⠟⠋⠁⠀⠀⠀
⠀⠀⠀⠀⠈⠙⠿⣾⣠⣆⣅⣀⣠⣄⣤⣴⣶⣾⣽⢿⠿⠟⠋⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠙⠛⠛⠙⠋⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀    
''',  # Center

        '''
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣤⣤⣤⣤⣴⣤⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣀⣴⣾⠿⠛⠋⠉⠁⠀⠀⠀⠈⠙⠻⢷⣦⡀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣤⣾⡿⠋⣠⣶⣿⡿⣿⣷⣦⡀⠁⠀⠀⠀⠀⠙⠿⣦⣀⠀⠀⠀⠀
⠀⠀⢀⣴⣿⡿⠋⢀⣼ ⠙⣿⣿⣾⣽⣿⡆⠀⠀⠀⠀⠀⠀ ⢻⣿⣷⣶⣄⠀
⠀⣴⣿⣿⠋⠀⠀⠸⣿   ⣯⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠐⡄⡌⢻⣿⣿⡷
⢸⣿⣿⠃⢂⡋⠄⢿⣿ ⣠⣿⣿⣯⣿⣿⠏⠀⠀⠀⠀⠀⠀⠀⢦⣷⣿⠿⠛⠁
⠀⠙⠿⢾⣤⡈⠙⠂⢤⠙⠿⢿⣿⣿⡿⠟⠁⢀⠀⠀⣀⣀⣤⣶⠟⠋⠁⠀⠀⠀
⠀⠀⠀⠀⠈⠙⠿⣾⣠⣆⣅⣀⣠⣄⣤⣴⣶⣾⣽⢿⠿⠟⠋⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠙⠛⠛⠙⠋⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀             
''',  # Left

        '''
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣤⣤⣤⣤⣴⣤⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣀⣴⣾⠿⠛⠋⠉⠁⠀⠀⠀⠈⠙⠻⢷⣦⡀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣤⣾⡿⠋⠁⠀⠀⠀⠀⣠⣶⣿⢿⡿⣷⣦⡀⠙⠿⣦⣀⠀⠀⠀⠀
⠀⠀⢀⣴⣿⡿⠋⠀⠀⠀⠀⠀⢀⣼⣿⣿⣿⣽⣾⠋ ⣿⡆⠀⢻⣿⣷⣶⣄⠀
⠀⣴⣿⣿⠋⠀⠀⠀⠀⠀⠀⠀⠸⣿⣿⣿⣿⣿⣿   ⣿⠐⡄⡌⢻⣿⣿⡷
⢸⣿⣿⠃⢂⡋⠄⠀⠀⠀⠀⠀⠀⢿⣿⣿⣿⣿⣿⣦ ⣿⠏⠀⢦⣷⣿⠿⠛⠁
⠀⠙⠿⢾⣤⡈⠙⠂⢤⢀⠀⠀⣀⠙⠿⢿⣿⣿⡿⠟⠁⣀⣤⣶⠟⠋⠁⠀⠀⠀
⠀⠀⠀⠀⠈⠙⠿⣾⣠⣆⣅⣀⣠⣄⣤⣴⣶⣾⣽⢿⠿⠟⠋⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠙⠛⠛⠙⠋⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀  
'''
    ]

    start_time = time.time()
    while time.time() - start_time < 2:
        for frame in frames:
            clear_screen()
            print("Online security system: Safety through Vigilance!\n")
            print(frame)
            time.sleep(0.2)

    # After the animation, clear the screen and show "LOADING"
    clear_screen()
    print("--- === --- START SERVER LOG --- === ---")

#eye_animation()


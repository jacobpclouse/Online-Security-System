import cv2

def list_available_webcams(max_webcams=10):
    available_webcams = []
    for i in range(max_webcams):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            available_webcams.append(i)
            cap.release()  # Release the camera when done
    return available_webcams

webcams = list_available_webcams()

if webcams:
    print(f"Available webcams: {webcams}")
else:
    print("No webcams found.")

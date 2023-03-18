'''
Snippet: save a stream of data from a remote webcam while that data is being live-streamed. 
'''

import cv2
import urllib.request

# Set the URL of the remote webcam stream
url = 'http://example.com/live/stream.mjpeg'

# Open the stream using urllib and initialize the video capture object
stream = urllib.request.urlopen(url)
cap = cv2.VideoCapture()

# Set the video resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Create video writer object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

# Read frames from the stream and save them as a video clip
while True:
    # Read the next frame from the stream
    bytes = bytes()
    while True:
        bytes += stream.read(1024)
        a = bytes.find(b'\xff\xd8')
        b = bytes.find(b'\xff\xd9')
        if a != -1 and b != -1:
            break
    jpg = bytes[a:b+2]
    bytes = bytes[b+2:]
    frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)

    # Display the frame
    cv2.imshow('frame', frame)

    # Save the frame as a video clip
    out.write(frame)

    # Wait for user input to exit
    if cv2.waitKey(1) == 27:
        break

# Release resources
cap.release()
out.release()
cv2.destroyAllWindows()
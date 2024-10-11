''' 
example resource
Python program that uses OpenCV library to capture video from your webcam and save it as a video clip when prompted by the user
'''
import cv2

# initialize video capture object
cap = cv2.VideoCapture(0)

# set video resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# create video writer object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

# loop over frames from the video stream
while True:
    # read the next frame from the video stream
    ret, frame = cap.read()

    # display the frame
    cv2.imshow('frame', frame)

    # wait for user input to start/stop recording
    if cv2.waitKey(1) == ord('q'):
        break
    elif cv2.waitKey(1) == ord('s'):
        # start recording
        print('Recording started...')
        while True:
            ret, frame = cap.read()
            out.write(frame)
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) == ord('q'):
                break
            elif cv2.waitKey(1) == ord('e'):
                # stop recording
                print('Recording stopped.')
                break

# release resources
cap.release()
out.release()
cv2.destroyAllWindows()
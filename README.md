# Online Security System - Jacob Clouse

## Overview:
- This client/server system should allow for a user to hook up multiple cameras and stream this data to a server that saves it for later
- System developed and run on: Linux (Debian/Ubuntu Based)

## Goals / Progression:
- [x] Created client and server files, setup .gitignore
- [x] Setup Virtual Environment that works (either PyCharm or vsCode Extensions)
- [x] Able to stream live video from single client to single server, no sound
- [ ] Able to save video feed from client to server for playback after stream ends, unique filename, no corruption
- [ ] Add Time Stamps and Location in video feed (on Client end)
- [ ] Allow port number and IP to be specified in bash command line as arguments (ie: python3 client.py 192.168.1.3 1025)
- [ ] Organize ongoing/saved feeds in database with timestamps, name, location, duration, etc.
- [ ] Setup Email Alerts to admin email to inform of new clients/client shutdowns and outages via Sendgrid API (socket server)
- [ ] Use Django web server (WITH LOGIN) to access videos and play them in browser (seperate user DB, salt & hash)
- [ ] Let users organize videos and query the db to filter videos by length, location, or timestamps
- [ ] Allow users to control socket server and socket clients from Django Web GUI (ie: terminate connections, start connections)
- [ ] Allow for the use of multiple client streams with a central socket server (can add/remove clients without disruptions)
- [ ] Use bootstrap and Css to make front end responsive and organized
- [ ] __OPTIONAL:__ Add Facial recognition to clients so they can identify who is in frame
- [ ] __OPTIONAL:__ Use Facial recognition on web GUI for login 

## Target Technologies:
- Python 3.8 - (OpenCV, Sockets)
- Flask (for Web GUI)
- SQLite (for Database)

## Sources:
- BASIS Transfer video over sockets from multiple clients: https://pyshine.com/Socket-Programming-with-multiple-clients/
- BASIS YT Video: https://youtu.be/1skHb3IjOr4
- Developing a Live Video Streaming Application using Socket Programming with Python: https://medium.com/nerd-for-tech/developing-a-live-video-streaming-application-using-socket-programming-with-python-6bc24e522f19
- OpenCV live stream video over socket in Python 3: https://stackoverflow.com/questions/49084143/opencv-live-stream-video-over-socket-in-python-3
- Streaming and Saving Video (Web Cam) with OpenCV and : https://www.youtube.com/watch?v=ChWvD3C7SgE
- How to record video from a webcam using Python & OpenCV: https://www.youtube.com/watch?v=frYotHLJ-Rc
- Python Virtual Environments: A Primer: https://realpython.com/python-virtual-environments-a-primer/
- Git CheatSheet PDF: https://www.atlassian.com/git/tutorials/atlassian-git-cheatsheet
- cv2 import error in virtual environment: https://stackoverflow.com/questions/35010064/cv2-import-error-in-virtual-environment
- Basic writing and formatting syntax: https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax
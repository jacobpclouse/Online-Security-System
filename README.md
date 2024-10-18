# Online Security System - Jacob Clouse

## Overview:
- This client/server system should allow for a user to hook up multiple cameras and stream this data to a server that saves it for later
- System developed and run on: Windows 10, Linux (Debian/Ubuntu Based)

## Goals / Progression:
- [x] Created client and server files, setup .gitignore
- [x] Setup Virtual Environment that works (either PyCharm or vsCode Extensions)
- [x] Able to stream live video from single client to single server, no sound
- [x] Allow port number and IP to be specified in bash command line as arguments (ie: python3 client.py 192.168.1.3 1025)
- [x] Able to save video feed from client to server for playback after stream ends, unique filename, no corruption
- [x] Add Time Stamps and Location in video feed
- * [x] Add framerate display in the feed
- * [x] Have preview images on client before streaming (grey color box around outside then red for recording)
- [ ] Add logic to only include webcams that aren't currently streaming or in use
- [x] Allow for the use of multiple client streams with a central socket server (can add/remove clients without disruptions)
- [x] Create Tkinter interfaces for client and server for user to put in their ip and port (default to localhost and 9999)
- * [x] And also have a box on top that shows the current private ip of the machine
- * [x] Put safeguards on the client and server so that if the input is not filled in or it is invalid it errors out and exits
- * [ ] Have a toggle button for the client to not show the feed that it is transmitting (lower power pc)
- * [x] Have a cut down console only client that the user passes ip and port into (and optionally video stream) as command line args
- [ ] Log entries into sqlite or postgres database (meta data like location, time start, time end, camera name, ip, etc)
- [X] Set client cameras to retry like 5 times and then give up and stop execution.
- * [X] When you add auto reconnect, add a tkinter box that will populate and say "Reconnecting"
- [ ] Add global variables to define resolution (height width) of video, how many retry attempts, name of json for client, etc
- [ ] Organize ongoing/saved feeds in database with timestamps, name, location, duration, etc.
- [ ] Setup Django/Flask so it can access the db across the network (not just locally on the same machine)
- [ ] Setup Email Alerts to admin email to inform of new clients/client shutdowns and outages via Sendgrid API (socket server)
- [ ] Use Django (or Flask) web server (WITH LOGIN) to access videos and play them in browser (seperate user DB, salt & hash) - Quasar Frontend
- [ ] Let users organize videos and query the db to filter videos by length, location, or timestamps
- [ ] Use Quasar/Vue.js in conjunction with Bootstrap to create a pretty/easy to use front end for the web client
- [ ] Beautify the interface for the client, allow user to specify location info and potentially camera selection
- [ ] Beautify the server interface with Tkinter(more than just start/stop buttons)
- [ ] Add motion detection in web interface so users can apply to camera feeds
- [ ] Add mp4 to other video format converter/vise versa so users can convert video to format that works on their device (outside scope?)
- [ ] Add toggle on client to live switch Feed from motion detection and normal vision
- * [ ] Also add a toggle in the server stream to switch motion detection on for the stream
- [ ] Add option to have streams capture audio (see how intensive this is)
- [ ] __OPTIONAL:__ Add Facial recognition to clients so they can identify who is in frame
- [ ] __OPTIONAL:__ Use Facial recognition on web GUI for login 
- [ ] __OPTIONAL:__ Integrate Terminal inside of Tkinter window
- [ ] __OPTIONAL:__ Integrate OAuth for login on the Web Dashboard
- [ ] __OPTIONAL:__ Let users in the web client see all the live feeds from the server
- [ ] __OPTIONAL:__ Find a way to Geotag videos recorded with webcams using network location/gps
- [ ] __OPTIONAL:__ Find a way to link metadata to video without using the video name of the .mp4 as the primary key (can rename and won't break this way)
- [ ] __OPTIONAL:__ Allow users to control socket server and socket clients from Tkinter GUI (ie: terminate connections, start connections) - Remote camera start/stop

## Target Technologies:
- Python 3.8 - (OpenCV, Sockets)
- Tkinter (for Client/Server GUI)
- Flask or Django (for Web back end)
- Quasar/Vue.js (for Web GUI front end)
- SQLite or Postgress (for Database)

### Sources used are listed in Snippets & Resources

## Testing:
When we are done with programing a build, we should test the client/server using x3 computers (two clients and a server):
- one run with all windows pcs, all webcam streams first, have client 1 join, then client 2 join, client 1 leave then client 1 join back, client 2 leave, then try streaming vides
- then do another test but this have one of the clients be a linux pc (otherwise same procedure as above)
- then another were the server is a linux pc (otherwise same procedure as above)

## Bugs:
- Currently looks like the start and stop times are not written correctly (videos that are minutes long are only logged as being seconds long)
- console only application is not passing video to the server correctly, it is able to pass pre made video though 
- reconnecting doesn't seem to be working, i need to adjust it so that if the client loses connection to the server it will try again and again to reconnect until it hits its timeout limit
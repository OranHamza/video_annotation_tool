﻿# video_annotation_tool
#Setting up ffmpeg 
Download ffmpeg with this link; https://drive.google.com/file/d/1r8pC5NDXZ5aPoLZy9EsrnZ1PvbaOSqiR/view
Download the zip file and save it to your computer.
Right-click on the zip file and select "Extract Here" or a similar option to extract the contents of the zip file.
Locate the extracted folder.
Right-click on the folder and select "Copy."
Open the "C:" drive on your computer.
Right-click in an empty area of the "C:" drive and select "Paste" to paste the folder into it.
After copt to bin folder path.
Open "Control Panel" and navigate to "System".
In the "System" window, select "Advanced system settings" from the left sidebar.
In the opened window, click on "Environment Variables".
In the "System Variables" section, select "Path" and click on "Edit".
In the new window, click on "New" and add the path to the directory where FFmpeg bin folder is located.
Confirm the changes by clicking "OK" in all windows to close them.

#Usage 
You need to run code with cli. 
Run this code in cli "python video_annotation_tool.py "your video path""
'Space' key toggles between pause and play.
's' marks the start of an annotation.
'e' marks the end of an annotation.
'n' clears all annotations.
'a' and 'd' allow navigating backward and forward in the video when paused.
Annotations are saved to a JSON file after the user exits the annotation process.

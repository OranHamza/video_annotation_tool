# Video Annotation Tool

## Setting up FFmpeg(For Windows)

1. **Download FFmpeg**: [Download FFmpeg](https://drive.google.com/file/d/1r8pC5NDXZ5aPoLZy9EsrnZ1PvbaOSqiR/view) from the provided link.
2. **Extract Files**: Extract the downloaded zip file to your computer.
3. **Copy Folder**: Locate the extracted folder and copy it.
4. **Paste to C Drive**: Navigate to your **"C:"** drive and paste the copied folder there.
5. **Set Path**: Open **"Control Panel"** -> **"System"** -> **"Advanced system settings"** -> **"Environment Variables"**
   - In the **User Variables** area, identify and select **Path** and then proceed to hit the **Edit** option.
    ![image](https://github.com/OranHamza/video_annotation_tool/assets/127665894/8bcde9f4-acee-41f5-9198-275cae2a6caf)
   - Select **New** in the following dialog box.
     ![image](https://github.com/OranHamza/video_annotation_tool/assets/127665894/1dffbf72-6363-4ca6-b9b4-35dd3cc0f995)
   - Enter **C:\ffmpeg\bin** in the provided space and select **OK** to confirm. This path indicates that the FFmpeg files are located at C:\. If FFmpeg files are located at a different location on your system, make sure that this path contains the correct location.
     ![image](https://github.com/OranHamza/video_annotation_tool/assets/127665894/d0f1bbad-a58c-4c52-b6b0-97c145e92a7e)

7. **Confirm Changes**: The final step is to verify that the FFmpeg is properly installed and available for use.
Start by launching the Command Prompt or PowerShell and enter ffmpeg.
**$ C:\ffmpeg**
If the installation is successful, you will see something like the following:
![image](https://github.com/OranHamza/video_annotation_tool/assets/127665894/e288813e-d773-4e91-8c1b-87da5153d781)

## Usage

1. **Run Code**: Execute the code using the command line interface (CLI).
- python video_annotation_tool.py "your videos folder path"
2. **Controls**:
- Press the **'Space'** key to toggle between pause and play.
- Press **'s'** to mark the start of an annotation.
- Press **'e'** to mark the end of an annotation.
- Press **'c'** to clear all annotations.
- Use **'a'** and **'d'** to navigate backward and forward in the video when paused.
- Press **'n'** to move to the next video.
- Press **'esc'** to close the tool.

3. **Saving Annotations**: Annotations are automatically saved to a JSON file after the user exits the annotation process.

## Interface

1. **Windows Title**: In the opened video window title, you will see the name of the video you are currently processing, along with annotations from the previous video if available. Additionally, any new video annotations, if added, will be visible.

![image](https://github.com/OranHamza/video_annotation_tool/assets/127665894/3c4d115f-f880-4dc8-8bd3-e01db4be1909)


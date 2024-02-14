# Video Annotation Tool

## Setting up FFmpeg

1. **Download FFmpeg**: [Download FFmpeg](https://drive.google.com/file/d/1r8pC5NDXZ5aPoLZy9EsrnZ1PvbaOSqiR/view) from the provided link.
2. **Extract Files**: Extract the downloaded zip file to your computer.
3. **Copy Folder**: Locate the extracted folder and copy it.
4. **Paste to C Drive**: Navigate to your "C:" drive and paste the copied folder there.
5. **Set Path**: Open "Control Panel" -> "System" -> "Advanced system settings" -> "Environment Variables". 
   - Select "Path" in the "System Variables" section and click "Edit".
   - Add the path to the directory where the FFmpeg bin folder is located.
6. **Confirm Changes**: Click "OK" in all windows to confirm and close them.

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


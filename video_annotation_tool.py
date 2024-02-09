import cv2
import argparse
import json
import os

def convert_webm_to_mp4(video_path):
    # Function to convert WebM video to MP4 format using FFmpeg
    output_mp4 = video_path.replace(".webm", ".mp4")
    cmd = f'ffmpeg -i "{video_path}" -c:v libx264 -crf 23 -c:a aac -strict experimental "{output_mp4}"'
    os.system(cmd)
    return output_mp4

def annotate_video(video_path):
    # Function to annotate time instants in a video
    # Convert WebM to MP4
    mp4_path = convert_webm_to_mp4(video_path)

    # Open the video file for annotation using OpenCV
    cap = cv2.VideoCapture(mp4_path)

    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    # Initialize variables
    annotations = []
    start_frame = None
    end_frame = None
    paused = False
    frame_buffer = []
    key_pressed = None

    # Main loop for video annotation
    while True:
        if not paused:
            ret, frame = cap.read()
            if not ret:
                # Reset video to beginning when it reaches the end
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue  # Continue to read the first frame of the video
            cv2.imshow('Video Annotation', frame)
            frame_buffer.append(frame)
        
        # Display information on the video window title
        frame_index = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
        time_in_seconds = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0
        title_text = f'Frame: {frame_index} | Time: {time_in_seconds:.2f}s'

        if annotations:
            annotation = annotations[-1]  # Get the last annotation
            start_time = annotation["start_time"]
            start_frame = annotation["start_frame"]
            end_frame = annotation["end_frame"]
            end_time = annotation["end_time"]
            title_text += f' | Annotation Start Frame: {start_frame} | Annotation Start Time: {start_time:.2f}s | Annotation End Frame: {end_frame} | Annotation End Time: {end_time:.2f}s'
        
        cv2.setWindowTitle('Video Annotation', title_text)

        # Process keyboard events
        key = cv2.waitKey(33)  # ~30 fps
        if key == 27:  # ESC key
            break
        elif key == 32:  # Space key to pause/play
            paused = not paused
        elif key == ord('s'):  # 's' key for marking start
            start_frame = frame_index
            start_time = time_in_seconds
            end_frame = None  # Reset end frame when marking start
            end_time = None   # Reset end time when marking start
        elif key == ord('e'):  # 'e' key for marking end
            if start_frame is not None:
                end_frame = frame_index
                end_time = time_in_seconds
                annotations.append({"start_frame": start_frame, "end_frame": end_frame, "start_time": start_time, "end_time": end_time})
        elif key == ord('n'):  # 'n' key to clear annotations
            annotations.clear()
        
        # Record key press/release events
        if key == ord('a'):
            key_pressed = 'a'
        elif key == ord('d'):
            key_pressed = 'd'
        elif key == -1:  # No key pressed
            key_pressed = None

        # Process continuous key press
        if key_pressed == 'a' and paused:
            if len(frame_buffer) > 0:
                cap.set(cv2.CAP_PROP_POS_FRAMES, cap.get(cv2.CAP_PROP_POS_FRAMES) - 2)
                ret, frame = cap.read()
                if ret:
                    cv2.imshow('Video Annotation', frame)
                    frame_buffer.pop()
        elif key_pressed == 'd' and paused:
            ret, frame = cap.read()
            if ret:
                cv2.imshow('Video Annotation', frame)
                frame_buffer.append(frame)

    cap.release()
    cv2.destroyAllWindows()
    
    # Save annotations to a JSON file
    if annotations:
        output_file = mp4_path.replace(".mp4", ".json")
        with open(output_file, 'w') as f:
            json.dump({"video_file": video_path, "annotations": annotations}, f, indent=4)
            print(f"Annotations saved to {output_file}")
    else:
        print("No annotations made.")

    # Remove MP4 file
    if os.path.exists(mp4_path):
        os.remove(mp4_path)

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Annotate time instants in a video.')
    parser.add_argument('video_path', type=str, help='Path to the video file')
    args = parser.parse_args()
    
    # Call annotate_video function with the provided video path
    annotate_video(args.video_path)

import cv2
import argparse
import json
import os


def convert_webm_to_mp4(video_path):
    # Function to convert a WebM video to MP4 format
    output_mp4 = video_path.replace(".webm", ".mp4")
    cmd = f'ffmpeg -i "{video_path}" -c:v libx264 -crf 23 -c:a aac -strict experimental "{output_mp4}"'
    os.system(cmd)
    return output_mp4


def annotate_video(video_path):
    # Function to annotate time instants in a video
    mp4_path = convert_webm_to_mp4(video_path)
    cap = cv2.VideoCapture(mp4_path)

    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    annotations = []
    start_frame = None
    end_frame = None
    paused = False
    frame_buffer = []
    key_pressed = None
    quit_app = False
    
    while True:
        if not paused:
            ret, frame = cap.read()
            if not ret:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue
            cv2.imshow('Video Annotation', frame)
            frame_buffer.append(frame)

        frame_index = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
        time_in_seconds = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0
        title_text = f'Frame: {frame_index} | Time: {time_in_seconds:.2f}s'

        if start_frame is not None:
            title_text += f' | Start Frame(Time): {start_frame}({start_time:.2f}s)'

        if end_frame is not None:
            title_text += f' | End Frame(Time): {end_frame}({end_time:.2f}s)'

        cv2.setWindowTitle('Video Annotation', title_text)

        key = cv2.waitKey(33)

        if key == 27:  # ESC key
            quit_app = True  # Set flag to quit application 
            break
        elif key == 32:  # Space key to pause/play
            paused = not paused
        elif key == ord('s'):  # 's' key for marking start
            start_frame = frame_index
            start_time = time_in_seconds
        elif key == ord('e'):  # 'e' key for marking end
            if start_frame is not None:
                end_frame = frame_index
                end_time = time_in_seconds
                annotations = ({"start_frame": start_frame, "end_frame": end_frame, "start_time": start_time, "end_time": end_time})
        elif key == ord('n'):  # 'n' key to move to the next video
            break
        elif key == ord('c'):  # 'c' key to clear annotations
            start_frame = None
            end_frame = None

        if key == ord('a'):
            key_pressed = 'a'
        elif key == ord('d'):
            key_pressed = 'd'
        elif key == -1:
            key_pressed = None

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

    if annotations:
        output_file = mp4_path.replace(".mp4", ".json")
        with open(output_file, 'w') as f:
            json.dump({"video_file": video_path, "annotations": annotations}, f, indent=4)
            print(f"Annotations for {video_path} saved to {output_file}.")
    else:
        print(f"No annotations made for {video_path}.")

    if os.path.exists(mp4_path):
        os.remove(mp4_path)

    return quit_app  # Return the flag value


def process_videos_in_folder(folder_path):
    video_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and f.lower().endswith(('.mp4', '.webm'))]

    for video_file in video_files:
        video_path = os.path.join(folder_path, video_file)
        quit_app = annotate_video(video_path)
        if quit_app:
            break  # Exit the loop if the flag indicates to quit


def main():
    parser = argparse.ArgumentParser(description='Annotate time instants in videos in a folder.')
    parser.add_argument('folder_path', type=str, help='Path to the folder containing video files')
    args = parser.parse_args()

    process_videos_in_folder(args.folder_path)


if __name__ == "__main__":
    main()

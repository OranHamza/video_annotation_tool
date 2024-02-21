import cv2
import argparse
import json
import os

def convert_webm_to_mp4(video_path):
    """
    Converting a WebM video to MP4 format using FFmpeg.(if needed)
    """
    if video_path.lower().endswith('.mp4'):
        return video_path
    
    output_mp4 = video_path.replace(".webm", ".mp4")
    cmd = f'ffmpeg -i "{video_path}" -c:v libx264 -crf 23 -c:a aac -strict experimental "{output_mp4}"'
    os.system(cmd)
    return output_mp4

def merge_annotations(video_path, new_annotations):
    """
    Merging new annotations with existing annotations for a video.(if there is previous annotations exists)
    """
    base_name, _ = os.path.splitext(video_path)
    json_path = base_name + ".json"

    existing_data = {}

   
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)

    existing_data["video_file"] = video_path

    if new_annotations:
        if "video_annotations" not in existing_data:
            existing_data["video_annotations"] = []
        existing_data["video_annotations"] = [new_annotations[-1]]

    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, indent=4)
        print(f"Annotations for {video_path} updated in {json_path}.")


def annotate_video(video_path):
    """
    Annotates time instants in a video by marking start and end frames.
    """
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
    
    base_name, _ = os.path.splitext(video_path)
    json_path = base_name + ".json"
    existing_annotations_title = ""
    
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
            if "video_annotations" in existing_data:
                existing_annotations = existing_data["video_annotations"]
                existing_annotations_title = " | Exists Annotations:"
                for annotation in existing_annotations:
                    existing_start_frame = annotation.get("start_frame")
                    existing_start_time = annotation.get("start_time")
                    existing_end_frame = annotation.get("end_frame")
                    existing_end_time = annotation.get("end_time")
                    existing_annotations_title += f" Start Frame(Time): {existing_start_frame}({existing_start_time:.2f}s) End Frame(Time): {existing_end_frame}({existing_end_time:.2f}s)"

    video_name_without_extension = os.path.splitext(os.path.basename(video_path))[0]

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

        title_text = f'{video_name_without_extension}{existing_annotations_title}'
        if start_frame is not None:
            title_text += f' | New Annotations : Start Frame(Time): {start_frame}({start_time:.2f}s)'

        if end_frame is not None:
            title_text += f' | End Frame(Time): {end_frame}({end_time:.2f}s)'

        cv2.setWindowTitle('Video Annotation', title_text)

        key = cv2.waitKey(33)

        if key == 27:  # ESC key
            quit_app = True
            break
        elif key == 32:  # Space key to pause/play
            paused = not paused
        elif key == ord('s'):  # 's' key for marking start
            start_frame = frame_index
            start_time = time_in_seconds
            if end_frame is not None and start_frame > end_frame:
                end_frame = None
                cv2.setWindowTitle('Video Annotation', f'End Frame reset | {title_text}')
        elif key == ord('e'):  # 'e' key for marking end
            if start_frame is not None:
                end_frame = frame_index
                end_time = time_in_seconds
                if end_frame is not None and end_frame < start_frame:
                    end_frame = None
                    cv2.setWindowTitle('Video Annotation', f'End Frame reset | {title_text}')
                else:
                    annotations.append({"start_frame": start_frame, "end_frame": end_frame, "start_time": start_time, "end_time": end_time})
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
        merge_annotations(video_path, annotations)
    else:
        print(f"No annotations made for {video_path}.")

    if mp4_path != video_path:
        os.remove(mp4_path)

    return quit_app

def process_videos_in_folder(folder_path):
    """
    Processes all video files in a folder by annotating time instants.
    """
    video_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and f.lower().endswith(('.mp4', '.webm'))]

    for video_file in video_files:
        video_path = os.path.join(folder_path, video_file)
        quit_app = annotate_video(video_path)
        if quit_app:
            break

def main():
    """
    Main function to initiate video annotation process.
    """
    parser = argparse.ArgumentParser(description='Annotate time instants in videos in a folder.')
    parser.add_argument('folder_path', type=str, help='Path to the folder containing video files')
    args = parser.parse_args()

    process_videos_in_folder(args.folder_path)

if __name__ == "__main__":
    main()
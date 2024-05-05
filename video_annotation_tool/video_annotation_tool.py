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
    base_name = os.path.splitext(os.path.basename(video_path))[0]
    json_path = os.path.join(os.path.dirname(video_path), base_name + ".json")

    existing_data = {}

    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)

    existing_data["video_file"] = os.path.basename(video_path)

    if "video_annotations" not in existing_data:
        existing_data["video_annotations"] = {}

    existing_data["video_annotations"].update(new_annotations)

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, indent=4)
        print(f"Annotations for {video_path} updated in {json_path}.")

def update_annotations(annotations, *frames_times):
    for i, (frame, time) in enumerate(frames_times, start=1):
        annotations[str(i)] = {"frame": frame, "time": time}
        
def annotate_video(video_path):
    """
    Annotates time instants in a video by marking e1 and end e2.
    """
    mp4_path = convert_webm_to_mp4(video_path)

    cap = cv2.VideoCapture(mp4_path)

    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    annotations = {}
    e1_frame = None
    e2_frame = None
    e3_frame = None
    e4_frame = None
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
                existing_annotations_title = " | Existing :"
                for key, value in existing_annotations.items():
                    frame = value.get("frame")
                    time = value.get("time")
                    if frame is not None and time is not None:
                        existing_annotations_title += f" {key}: F(T): {frame}({time:.2f}s)"
                    else:
                         existing_annotations_title = ""

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

        title_text = f'{os.path.basename(video_path)} | {frame_index}{"("}{time_in_seconds:.2f}{"s"}{")"}{existing_annotations_title}'
        if e1_frame is not None:
            title_text += f' | New : E1 F(T): {e1_frame}({e1_time:.2f}s)'

        if e2_frame is not None and e1_frame is not None and e1_frame<e2_frame:
            title_text += f' | E2 F(T): {e2_frame}({e2_time:.2f}s)'

        if e3_frame is not None and e2_frame is not None and e2_frame<=e3_frame and e1_frame<e2_frame:
            title_text += f' | E3 F(T): {e3_frame}({e3_time:.2f}s)'

        if e4_frame is not None and e3_frame is not None and e3_frame<=e4_frame and e2_frame<=e3_frame:
            title_text += f' | E4 F(T): {e4_frame}({e4_time:.2f}s)'

        cv2.setWindowTitle('Video Annotation', title_text)

        key = cv2.waitKey(33)

        if key == 27:  # ESC key
            quit_app = True
            break
        elif key == 32:  # Space key to pause/play
            paused = not paused
        elif key == ord('1'):  # '1' key for marking e1
            e1_frame = frame_index
            e1_time = time_in_seconds
            if e2_frame is not None and e1_frame > e2_frame:
                e2_frame = None
                e3_frame = None
                e4_frame = None
                cv2.setWindowTitle('Video Annotation', f'E2 Frame reset | {title_text}')
        elif key == ord('2'):  # '2' key for marking e2
            if e1_frame is not None:
                e2_frame = frame_index
                e2_time = time_in_seconds
                if e2_frame is not None and e2_frame < e1_frame:
                    e2_frame = None
                    e3_frame = None
                    e4_frame = None
                    cv2.setWindowTitle('Video Annotation', f'E2 Frame reset | {title_text}')
        elif key == ord('3'):  # '3' key for marking e3
            if e2_frame is not None:
                e3_frame = frame_index
                e3_time = time_in_seconds
                if e3_frame is not None and e3_frame < e2_frame:
                    e3_frame = None
                    cv2.setWindowTitle('Video Annotation', f'E3 Frame reset | {title_text}')
        elif key == ord('4'):  # '4' key for marking e4
            if e3_frame is not None:
                e4_frame = frame_index
                e4_time = time_in_seconds
                if e4_frame is not None and e4_frame < e3_frame:
                    e4_frame = None
                    cv2.setWindowTitle('Video Annotation', f'E4 Frame reset | {title_text}')
                update_annotations(annotations, (e1_frame, e1_time), (e2_frame, e2_time), (e3_frame, e3_time), (e4_frame, e4_time))

        elif key == ord('5'):  # '5' key for using existing annotation 1
            if "1" in existing_annotations:
                e1_frame = existing_annotations["1"]["frame"]
                e1_time = existing_annotations["1"]["time"]
        elif key == ord('6'):  # '6' key for using existing annotation 2
            if "2" in existing_annotations:
                e2_frame = existing_annotations["2"]["frame"]
                e2_time = existing_annotations["2"]["time"]
        elif key == ord('7'):  # '7' key for using existing annotation 3
            if "3" in existing_annotations:
                e3_frame = existing_annotations["3"]["frame"]
                e3_time = existing_annotations["3"]["time"]
        elif key == ord('8'):  # '8' key for using existing annotation 4
            if "4" in existing_annotations:
                e4_frame = existing_annotations["4"]["frame"]
                e4_time = existing_annotations["4"]["time"]
           
            update_annotations(annotations, (e1_frame, e1_time), (e2_frame, e2_time), (e3_frame, e3_time), (e4_frame, e4_time))
                    
        elif key == ord('n'):  # 'n' key to move to the next video
            break
        elif key == ord('c'):  # 'c' key to clear annotations
            e1_frame = None
            e2_frame = None
            e3_frame = None
            e4_frame = None
            e1_time = None
            e2_time = None
            e3_time = None
            e4_time = None
            update_annotations(annotations, (e1_frame, e1_time), (e2_frame, e2_time), (e3_frame, e3_time), (e4_frame, e4_time))

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
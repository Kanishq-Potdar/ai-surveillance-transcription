import cv2
import os

def extract_frames(video_path, frame_interval=30):
    
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found at: {video_path}")

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise ValueError("Error opening video file.")

    fps = cap.get(cv2.CAP_PROP_FPS)
    frames = []
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % frame_interval == 0:
            timestamp = frame_count / fps
            frames.append((timestamp, frame))

        frame_count += 1

    cap.release()
    return frames


# Testing this function (run directly to test)
if __name__ == "__main__":
    frames = extract_frames("footage/input.mp4", frame_interval=30)
    print(f"Extracted {len(frames)} frames.")
    for i, (timestamp, _) in enumerate(frames[:5]):
        print(f"Frame {i+1} at {timestamp:.2f}s")

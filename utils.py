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


# --- AI Surveillance: Run Detection on Video ---
from detection import detect_objects
import numpy as np

def run_detection(video_path, frame_interval=30, target_classes=None, conf_threshold=0.25):
    """
    Extract frames and run YOLOv8 detection on each frame.
    Returns: list of (timestamp, [ (label, (x, y, w, h)), ... ])
    """
    frames = extract_frames(video_path, frame_interval=frame_interval)
    detections = []
    for timestamp, frame in frames:
        # Convert frame to RGB if needed
        if frame.shape[2] == 3:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        else:
            frame_rgb = frame
        objects = detect_objects(frame_rgb, target_classes=target_classes, conf_threshold=conf_threshold)
        detections.append((timestamp, objects))
    return detections

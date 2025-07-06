from utils import extract_frames
from detection import detect_objects
from logger import save_transcript
import os

def main():
    video_path = "footage/input.mp4"
    output_path = "output/transcript.txt"

    print("[INFO] Extracting frames from video...")
    try:
        frames = extract_frames(video_path, frame_interval=30)
    except Exception as e:
        print(f"[ERROR] {e}")
        return

    print(f"[INFO] Extracted {len(frames)} frames.")

    detections = []

    for i, (timestamp, frame) in enumerate(frames):
        print(f"[INFO] Processing frame {i+1}/{len(frames)} at {timestamp:.2f}s...")

        try:
            labels = detect_objects(frame)
        except Exception as e:
            print(f"[ERROR] Object detection failed: {e}")
            labels = []

        detections.append((timestamp, labels))

    print(f"[INFO] Saving results to {output_path}...")
    save_transcript(detections, output_path)
    print("[✅] Done. Transcript saved.")


if __name__ == "__main__":
    main()

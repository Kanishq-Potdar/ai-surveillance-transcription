import argparse
from utils import extract_frames
from detection import detect_objects
from logger import save_transcript, save_transcript_csv

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", default="footage/input.mp4", help="Path to input video")
    parser.add_argument("--interval", type=int, default=30, help="Frame extraction interval")
    parser.add_argument("--output", default="output/transcript.txt", help="Output file path")
    parser.add_argument("--csv", action="store_true", help="Save as CSV instead of TXT")
    parser.add_argument("--filter", nargs="*", help="Filter for specific object classes")

    args = parser.parse_args()

    video_path = args.video
    output_path = args.output
    frame_interval = args.interval
    target_classes = args.filter if args.filter else None

    print("[INFO] Extracting frames from video...")
    try:
        frames = extract_frames(video_path, frame_interval=frame_interval)
    except Exception as e:
        print(f"[ERROR] {e}")
        return

    print(f"[INFO] Extracted {len(frames)} frames.")

    detections = []

    for i, (timestamp, frame) in enumerate(frames):
        print(f"[INFO] Processing frame {i+1}/{len(frames)} at {timestamp:.2f}s...")

        try:
            labels = detect_objects(frame, target_classes=target_classes)
        except Exception as e:
            print(f"[ERROR] Object detection failed: {e}")
            labels = []

        detections.append((timestamp, labels))

    print(f"[INFO] Saving results to {output_path}...")
    if args.csv:
        save_transcript_csv(detections, output_path)
    else:
        save_transcript(detections, output_path)

    print("[✅] Done. Transcript saved.")


if __name__ == "__main__":
    main()
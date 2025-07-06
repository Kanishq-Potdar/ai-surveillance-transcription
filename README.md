# AI Surveillance Transcription

This project processes surveillance video footage to detect objects in frames and generate a timestamped transcript of detected objects.

## Features

- Extracts frames from a video at regular intervals
- Runs object detection on each frame
- Logs detected objects with timestamps to a transcript file

## Project Structure

```
detection.py         # Object detection logic (e.g., using YOLOv8)
logger.py            # Transcript saving utilities
main.py              # Main script to run the pipeline
utils.py             # Frame extraction and utilities
requirements.txt     # Python dependencies
yolov8n.pt           # YOLOv8 model weights
footage/input.mp4    # Input video file
output/transcript.txt# Output transcript
```

## Usage

1. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
2. **Place your video:**
   - Put your input video in the `footage/` folder as `input.mp4` (or update the path in `main.py`).
3. **Run the pipeline:**
   ```sh
   python main.py
   ```
4. **View results:**
   - The transcript will be saved to `output/transcript.txt`.

## Customization

- **Frame Interval:** Adjust the `frame_interval` parameter in `main.py` to change how often frames are extracted.
- **Model:** Replace `yolov8n.pt` with your preferred YOLOv8 weights if needed.

## Requirements

- Python 3.8+
- See `requirements.txt` for required packages (e.g., OpenCV, torch, ultralytics, etc.)

## Notes

- Make sure the `output/` directory exists before running the script.
- The detection model and frame extraction logic can be customized in `detection.py` and `utils.py`.

## License

MIT License

## Run in terminal by :
If you want plain text file : ` python main.py `

If you want csv file format: ` python main.py --csv `

If you want to filter the object in frame :` python main.py --filter person car `    
#(will only show when car and person appaers)

for both filter and csv file format :` python main.py --video footage/input.mp4 --filter person car --csv `

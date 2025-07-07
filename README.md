# AI Surveillance Transcription

This project analyzes surveillance footage, detects objects, and generates a human-readable transcript and CSV log of detected events using a professional Streamlit web interface.

## Features

- Upload `.mp4` surveillance videos via a web UI
- Automated object detection and event logging
- Downloadable transcript (TXT) and CSV logs
- Summary of detected object classes

## Project Structure

```
detection.py         # Object detection logic (e.g., using YOLOv8)
logger.py            # Transcript saving utilities
main.py              # Main script to run the pipeline (CLI)
app.py               # Streamlit web app
utils.py             # Frame extraction and utilities
requirements.txt     # Python dependencies
yolov8n.pt           # YOLOv8 model weights
footage/input.mp4    # Input video file
output/transcript.txt# Output transcript
```

## Setup

1. **Clone the repository** and navigate to the project directory.

2. **Create and activate a virtual environment** (recommended):

   **Windows:**

   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

   **Mac/Linux:**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Create required folders** (if not present):
   - `footage`
   - `output`

## Running the App

**On Windows:**

```bash
python -m streamlit run app.py
```

**On Mac/Linux:**

```bash
streamlit run app.py
```

The app will open in your default browser. Upload a video file to begin processing.

## Output

- **Transcript:** Human-readable summary of detected events.
- **CSV:** Structured log of all detections.

Both files are available for download after processing.

---

## Command Line Usage (Optional)

You can still use the original CLI pipeline:

- Plain text file: `python main.py`
- CSV file format: `python main.py --csv`
- Filter objects: `python main.py --filter person car`
- Both filter and CSV: `python main.py --video footage/input.mp4 --filter person car --csv`

---

## Requirements

- Python 3.8+
- See `requirements.txt` for required packages (e.g., OpenCV, torch, ultralytics, streamlit, etc.)

---

## License

MIT License

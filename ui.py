import streamlit as st
import os
import tempfile
from utils import extract_frames
from detection import detect_objects
from logger import save_transcript, save_transcript_csv

st.set_page_config(page_title="AI Surveillance Transcription")

st.title("🔍 AI Surveillance Transcription")

st.markdown("""
Upload a surveillance video, detect objects frame by frame using YOLOv8, and download the transcription as TXT or CSV.
""")

# --- Upload file ---
uploaded_file = st.file_uploader("Upload MP4 video", type=["mp4"])

if uploaded_file is not None:
    # Save uploaded video to a temporary file
    temp_dir = tempfile.mkdtemp()
    video_path = os.path.join(temp_dir, uploaded_file.name)

    with open(video_path, "wb") as f:
        f.write(uploaded_file.read())

    st.success("Video uploaded successfully!")

    # --- Settings ---
    st.subheader("Processing Options")

    frame_interval = st.number_input(
        "Frame interval (every N frames):", min_value=1, max_value=500, value=30, step=1
    )

    filter_classes = st.text_input(
        "Filter objects (comma separated, e.g. person, car)", value=""
    )

    output_format = st.radio(
        "Output format:", ["Text (.txt)", "CSV (.csv)"]
    )

    if st.button("Start Processing"):
        st.info("Extracting frames...")

        frames = extract_frames(video_path, frame_interval=frame_interval)

        st.success(f"Extracted {len(frames)} frames.")

        target_classes = None
        if filter_classes.strip():
            target_classes = [c.strip() for c in filter_classes.split(",") if c.strip()]

        detections = []
        progress = st.progress(0)

        for i, (timestamp, frame) in enumerate(frames):
            st.write(f"Processing frame {i+1}/{len(frames)} at {timestamp:.2f}s...")
            try:
                labels = detect_objects(frame, target_classes=target_classes)
            except Exception as e:
                st.error(f"Detection failed: {e}")
                labels = []
            detections.append((timestamp, labels))
            progress.progress((i+1)/len(frames))

        # --- Save output ---
        output_path = os.path.join(temp_dir, "transcript")

        if output_format == "Text (.txt)":
            output_path += ".txt"
            save_transcript(detections, output_path)
            # --- Transcript Search (TXT) ---
            st.subheader("Search Transcript")
            search_query = st.text_input("Enter search term (TXT)")
            transcript_lines = []
            with open(output_path, "r", encoding="utf-8") as f:
                transcript_lines = f.readlines()
            if search_query:
                results = [line for line in transcript_lines if search_query.lower() in line.lower()]
                st.write(f"Found {len(results)} matching lines:")
                for line in results:
                    st.write(line)
            else:
                st.write("Enter a search term to filter transcript lines.")
            with open(output_path, "rb") as f:
                st.download_button(
                    label="Download Transcript (.txt)",
                    data=f,
                    file_name="transcript.txt",
                    mime="text/plain"
                )
        else:
            import csv
            output_path += ".csv"
            save_transcript_csv(detections, output_path)
            # --- Transcript Search (CSV) ---
            st.subheader("Search Transcript")
            search_query = st.text_input("Enter search term (CSV)")
            transcript_rows = []
            with open(output_path, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                transcript_rows = list(reader)
            if search_query:
                results = [row for row in transcript_rows if any(search_query.lower() in str(cell).lower() for cell in row)]
                st.write(f"Found {len(results)} matching rows:")
                for row in results:
                    st.write(row)
            else:
                st.write("Enter a search term to filter transcript rows.")
            with open(output_path, "rb") as f:
                st.download_button(
                    label="Download Transcript (.csv)",
                    data=f,
                    file_name="transcript.csv",
                    mime="text/csv"
                )

        st.success("✅ Processing complete!")
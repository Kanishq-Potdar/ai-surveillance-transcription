import streamlit as st
import os
from logger import save_transcript, save_transcript_csv
import utils

st.set_page_config(page_title="AI Surveillance Transcription", layout="centered")
st.title("AI Surveillance Transcription")

st.markdown("""
This app analyzes surveillance footage, detects objects, and generates a human-readable transcript and CSV log of detected events.
""")

uploaded_file = st.file_uploader("Upload a video file (mp4)", type=["mp4"])

if uploaded_file is not None:
    # Save uploaded file to a temp location
    input_path = os.path.join("footage", uploaded_file.name)
    with open(input_path, "wb") as f:
        f.write(uploaded_file.read())
    st.success(f"Uploaded {uploaded_file.name}")

    # Run detection (assuming utils.run_detection exists)
    with st.spinner("Processing video and detecting objects..."):
        detections = utils.run_detection(input_path)

    st.success("Detection complete!")

    # Save transcript and CSV
    transcript_path = os.path.join("output", "transcript.txt")
    csv_path = os.path.join("output", "transcript.csv")
    save_transcript(detections, transcript_path)
    save_transcript_csv(detections, csv_path)

    # Display transcript
    st.subheader("Transcript")
    with open(transcript_path, "r") as f:
        transcript = f.read()
    st.text_area("Transcript", transcript, height=300)

    # Download buttons
    st.download_button("Download Transcript (TXT)", transcript, file_name="transcript.txt")
    with open(csv_path, "r") as f:
        csv_content = f.read()
    st.download_button("Download Transcript (CSV)", csv_content, file_name="transcript.csv")

    # Optionally, show detected objects summary
    st.subheader("Detected Objects Summary")
    all_labels = set()
    for _, items in detections:
        for label, _ in items:
            all_labels.add(label)
    if all_labels:
        st.write(", ".join(sorted(all_labels)))
    else:
        st.write("No significant objects detected.")
else:
    st.info("Please upload a video file to begin.")

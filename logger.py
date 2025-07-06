def format_time(seconds):
    """
    Converts seconds to HH:MM:SS
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"

def save_transcript(detections, path):
    """
    Writes detections to a text file.

    Args:
        detections: list of (timestamp, list_of_objects)
        path: output file path
    """
    with open(path, "w") as f:
        for ts, objects in detections:
            time_str = format_time(ts)
            if objects:
                obj_str = ", ".join(objects)
            else:
                obj_str = "No objects detected"
            f.write(f"[{time_str}] {obj_str}\n")
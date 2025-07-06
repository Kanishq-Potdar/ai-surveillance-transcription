import csv

def format_time(seconds):
    """
    Converts seconds to HH:MM:SS
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"

def save_transcript(detections, output_path):
    seen_objects = set()
    last_objects = set()

    with open(output_path, "w") as f:
        for timestamp, items in detections:
            time_str = f"[{timestamp:06.2f}s]"
            labels = [label for label, _ in items]

            current_set = set(labels)
            scene_changed = current_set != last_objects
            last_objects = current_set

            if not labels:
                description = "No significant objects detected."
            else:
                descriptions = []
                for label, (x, y, w, h) in items:
                    position = get_position(x)
                    if label in seen_objects:
                        descriptions.append(f"A {label} appeared again near the {position}.")
                    else:
                        descriptions.append(f"A {label} was seen near the {position}.")
                        seen_objects.add(label)

                description = " ".join(descriptions)

            if scene_changed and labels:
                f.write("\n--- Scene changed ---\n")

            f.write(f"{time_str} {description}\n")

def save_transcript_csv(detections, output_path):
    """
    Saves detections to a CSV file.
    """
    with open(output_path, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "Objects"])

        for timestamp, items in detections:
            time_str = format_time(timestamp)
            if not items:
                writer.writerow([time_str, "No significant objects detected."])
            else:
                labels = [label for label, _ in items]
                obj_str = ", ".join(labels)
                writer.writerow([time_str, obj_str])


def get_position(x):
    if x < 213:
        return "left side"
    elif x < 426:
        return "center"
    else:
        return "right side"


if __name__ == "__main__":
    test_data = [
        (0.0, [("person", (200, 50, 100, 150)), ("car", (300, 60, 120, 160))]),
        (1.5, []),
        (3.2, [("dog", (400, 70, 110, 140))]),
    ]

    save_transcript(test_data, "output/transcript.txt")
    save_transcript_csv(test_data, "output/transcript.csv")
    print("Transcript files saved.")
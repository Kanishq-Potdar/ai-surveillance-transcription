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

            # Scene change detection (if objects changed significantly)
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


def get_position(x):
    if x < 213:
        return "left side"
    elif x < 426:
        return "center"
    else:
        return "right side"

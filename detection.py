from ultralytics import YOLO

# Load YOLO model once
model = YOLO("yolov8n.pt")

def detect_objects(frame, conf_threshold=0.25):
    """
    Runs YOLOv8 on the input frame.

    Args:
        frame: np.array (BGR)
        conf_threshold: confidence threshold

    Returns:
        List of detected class names
    """
    results = model.predict(frame, conf=conf_threshold, verbose=False)
    names = []

    for r in results:
        for box in r.boxes:
            class_id = int(box.cls[0])
            name = model.names[class_id]
            names.append(name)

    return names
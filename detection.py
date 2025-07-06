from ultralytics import YOLO

model = YOLO("yolov8n.pt")

def detect_objects(frame, target_classes=None, conf_threshold=0.25):
    """
    Detect objects in a frame.

    Args:
        frame: np.ndarray
        target_classes: list of class names to keep (e.g. ["person", "car"]) or None
        conf_threshold: float confidence threshold

    Returns:
        list of (label, (x_center, y_top, width, height))
    """
    results = model.predict(frame, conf=conf_threshold, verbose=False)[0]
    detections = []

    for box in results.boxes:
        cls = int(box.cls[0])
        label = model.names[cls]

        if target_classes is not None and label not in target_classes:
            continue

        x1, y1, x2, y2 = map(int, box.xyxy[0])
        x_center = (x1 + x2) // 2
        w = x2 - x1
        h = y2 - y1
        detections.append((label, (x_center, y1, w, h)))

    return detections


if __name__ == "__main__":
    import cv2

    cap = cv2.VideoCapture("footage/input.mp4")
    ret, frame = cap.read()
    cap.release()

    if ret:
        # EXAMPLE: test filter for person and car
        objects = detect_objects(frame, target_classes=["person", "car"])
        print("Detected objects:", objects)
    else:
        print("Could not read frame.")
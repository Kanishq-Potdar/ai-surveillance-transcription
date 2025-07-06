from ultralytics import YOLO

model = YOLO("yolov8n.pt")

def detect_objects(frame):
    results = model(frame, verbose=False)[0]
    detections = []

    for box in results.boxes:
        cls = int(box.cls[0])
        label = model.names[cls]
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
        objects = detect_objects(frame)
        print("Detected objects:", objects)
    else:
        print("Could not read frame.")
from ultralytics import YOLO

model = YOLO("yolov8m.pt")

def detect(path):
    results = model.predict(path)
    result = results[0]

    detected_objects = []

    for box in result.boxes:
        class_id = result.names[box.cls[0].item()]
        cords = box.xyxy[0].tolist()
        cords = [round(x) for x in cords]
        conf = round(box.conf[0].item(), 2)

        object_info = {
            "Object type": class_id,
            "Coordinates": cords,
            "Probability": conf
        }

        detected_objects.append(object_info)

    return detected_objects

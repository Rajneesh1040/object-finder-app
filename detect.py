import cv2
from ultralytics import YOLO
import pygame

# Load YOLO model (make sure yolov8n.pt is downloaded or use a custom model if trained)
model = YOLO("yolov8n.pt")

# Notification sound function
def trigger_notification():
    pygame.mixer.init()
    pygame.mixer.music.load("alert.mp3")  # Ensure this file exists and is a valid mp3
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue

# Object detection function
def detect_object(target_object, ip_stream_url):
    cap = cv2.VideoCapture(ip_stream_url)

    if not cap.isOpened():
        print("❌ Could not open IP camera stream. Check the IP URL.")
        return

    found = False

    while True:
        ret, frame = cap.read()
        if not ret:
            print("⚠️ Failed to grab frame from the IP stream.")
            break

        results = model(frame)

        for r in results:
            for box in r.boxes.data:
                class_id = int(box[5])
                label = model.names[class_id]

                if target_object.lower() in label.lower():
                    found = True
                    x1, y1, x2, y2 = map(int, box[:4])
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, label, (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                    print(f"✅ Found: {label}")
                    trigger_notification()

        cv2.imshow("📷 IP Camera Object Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q') or found:
            break

    cap.release()
    cv2.destroyAllWindows()

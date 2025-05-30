import streamlit as st
import speech_recognition as sr
import cv2
from ultralytics import YOLO
import pygame

# Load YOLO model
model = YOLO("yolov8n.pt")

# Notification
def trigger_notification():
    pygame.mixer.init()
    pygame.mixer.music.load("alert.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue

# Voice input
def get_object_name():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Speak now: Example - 'Where is my mobile?'")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        st.success(f"You said: {text}")
        keywords = text.lower().split()
        if "my" in keywords:
            idx = keywords.index("my")
            return keywords[idx + 1] if idx + 1 < len(keywords) else keywords[-1]
        return keywords[-1]
    except:
        st.error("Sorry, I couldn't understand you.")
        return None

# Detection
def detect_object(object_name, stream_url):
    cap = cv2.VideoCapture(stream_url)
    found = False

    stframe = st.empty()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            st.warning("📡 Stream broken.")
            break

        results = model(frame)

        for r in results:
            for box in r.boxes.data:
                class_id = int(box[5])
                label = model.names[class_id]
                if object_name in label.lower():
                    found = True
                    x1, y1, x2, y2 = map(int, box[:4])
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, label, (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    trigger_notification()
        stframe.image(frame, channels="BGR")

        if found:
            break
    cap.release()

# Streamlit UI
st.title("📱 Object Finder with Voice")
st.markdown("Say: **'Where is my mobile?'**")

ip_url = st.text_input("📷 Enter your phone camera IP stream (e.g., http://192.168.1.3:8080/video):")

if st.button("🎤 Start Voice Command"):
    object_name = get_object_name()
    if object_name and ip_url:
        st.info(f"Looking for your `{object_name}`...")
        detect_object(object_name, ip_url)

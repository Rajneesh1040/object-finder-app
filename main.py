from voice_input import get_object_name
from detect import detect_object

# Your phone's IP camera stream URL (use IP Webcam app or similar)
IP_CAMERA_URL = "http://192.168.1.3:8080/video"  # 🔁 Replace with actual IP if needed

def main():
    object_name = get_object_name()
    if object_name:
        print(f"Looking for your {object_name}...")
        detect_object(object_name, IP_CAMERA_URL)
    else:
        print("Could not understand the object name.")

if __name__ == "__main__":
    main()

import speech_recognition as sr

def get_object_name():
    recognizer = sr.Recognizer()
    mic = sr.Microphone(device_index=1)  # Change index based on your mic list

    with mic as source:
        print("🎤 Listening... Ask: 'Where is my mobile?'")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("You said:", text)

        # Extract object name (last word or after 'my')
        keywords = text.lower().split()
        if "my" in keywords:
            idx = keywords.index("my")
            if idx + 1 < len(keywords):
                return keywords[idx + 1]
        return keywords[-1]  # fallback
    except sr.UnknownValueError:
        print("⚠️ Could not understand audio.")
        return None

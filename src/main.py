import cv2
import time
import snowboydecoder
import voice
import camera

# Set up the Snowboy wake word detector
detector = snowboydecoder.HotwordDetector("data/models/mymodel.pmdl", sensitivity=0.5)

# Set up the camera and face detector
cam = camera.Camera()
face_cascade = cv2.CascadeClassifier("data/haarcascade_frontalface_default.xml")

# Start the voice assistant
voice.start_assistant()

# Define a function to handle voice commands
def handle_command(command):
    if "hello" in command:
        response = "Hello! How can I assist you?"
    elif "goodbye" in command:
        response = "Goodbye!"
    else:
        response = "Sorry, I didn't understand that."
    voice.generate_audio(response, "data/sounds/response.wav")
    voice.play_audio("data/sounds/response.wav")

# Define a function to handle wake word detection
def detected_callback():
    voice.play_audio("data/sounds/start_listening.wav")
    print("Wake word detected! Listening for commands...")
    while True:
        # Capture an image from the camera
        img = cam.capture_image()

        # Detect faces in the image
        faces = face_cascade.detectMultiScale(img, scaleFactor=1.1, minNeighbors=5)

        # If a face is detected, stop listening and handle the command
        if len(faces) > 0:
            voice.play_audio("data/sounds/stop_listening.wav")
            command = voice.recognize_speech()
            print(f"Command: {command}")
            handle_command(command)
            break

# Start the Snowboy detector with the detected_callback function
detector.start(detected_callback)

# Clean up resources when finished
detector.terminate()
voice.stop_assistant()
cam.release()

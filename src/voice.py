import os
import wave
import pyaudio
import speech_recognition as sr
import requests
import json
import pyttsx3

# Set up the PyAudio audio stream
audio = pyaudio.PyAudio()

# Define the audio format
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

# Set up the Google Speech Recognition API
r = sr.Recognizer()
r.energy_threshold = 500
r.dynamic_energy_threshold = True

# Set up the pyttsx3 TTS engine
engine = pyttsx3.init()

# Define the API endpoint for ChatGPT
API_ENDPOINT = "https://api.openai.com/v1/engine/davinci-codex/completions"

# Set up the API headers and payload
API_HEADERS = {
    "Content-Type": "application/json",
    "Authorization": "Bearer YOUR_API_KEY_HERE"
}
API_PAYLOAD = {
    "prompt": "",
    "max_tokens": 64,
    "n": 1,
    "stop": "\n"
}

# Define a function to start the voice assistant
def start_assistant():
    engine.startLoop()

# Define a function to stop the voice assistant
def stop_assistant():
    engine.endLoop()

# Define a function to generate an audio file from text using TTS
def generate_audio(text, filename):
    engine.save_to_file(text, filename)
    engine.runAndWait()

# Define a function to play an audio file
def play_audio(filename):
    # Open the audio file
    wf = wave.open(filename, 'rb')

    # Open the audio stream
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        output=True)

    # Read data from the audio file and write it to the stream
    data = wf.readframes(CHUNK)
    while data:
        stream.write(data)
        data = wf.readframes(CHUNK)

    # Clean up resources
    stream.stop_stream()
    stream.close()
    wf.close()

# Define a function to recognize speech using Google Speech Recognition API
def recognize_speech():
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio)
        print(f"Recognized: {command}")
        return command.lower()
    except sr.UnknownValueError:
        print("Could not understand audio")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return ""

# Define a function to generate a response using the ChatGPT API
def generate_response(prompt):
    # Set the prompt for the API request
    API_PAYLOAD["prompt"] = prompt

    # Send the API request and parse the response
    response = requests.post(API_ENDPOINT, headers=API_HEADERS, data=json.dumps(API_PAYLOAD))
    data = json.loads(response.text)

    # Extract the response text from the API response
    response_text = data["choices"][0]["text"].strip()

    return response_text

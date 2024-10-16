import os
import sys
import json
import datetime
import threading
import pyaudio
from vosk import Model, KaldiRecognizer
from gtts import gTTS
import pywhatkit
import wikipedia
import pyjokes
import logging

from photo_capture import capture_real_time_photos  # Import the function from the module
from face_recognition_module import recognize_faces  # Import the recognize_faces function

# Initialize logging
logging.basicConfig(level=logging.INFO, filename="assistant.log", filemode="a",
                    format="%(asctime)s - %(levelname)s - %(message)s")

# Initialize Vosk model
model_path = "/home/pi/testing/vosk-model-small-en-us-0.15"
model = Model(model_path)

# Wake word
WAKE_WORD = "sarah"

# Function to play back text through speakers using gTTS
def speak_text(text):
    try:
        tts = gTTS(text=text, lang='en')
        tts.save("output.mp3")
        os.system("mpg321 output.mp3")
        print(f"Spoken: {text}")
    except Exception as e:
        logging.error(f"Failed to speak: {e}")
        print(f"Failed to speak: {e}")

# Function to listen for the wake word using Vosk
def listen_for_wake_word():
    recognizer = KaldiRecognizer(model, 16000)
    mic = pyaudio.PyAudio()
    stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
    stream.start_stream()

    print("Listening for wake word...")
    try:
        while True:
            data = stream.read(4096, exception_on_overflow=False)
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                result_dict = json.loads(result)
                text = result_dict.get("text", "")
                if WAKE_WORD in text.lower():
                    print(f"Wake word '{WAKE_WORD}' detected...")
                    speak_text("YES PLEASE")
                    return True
    finally:
        stream.stop_stream()
        stream.close()
        mic.terminate()

# Function to listen and recognize speech using Vosk
def listen_and_recognize():
    recognizer = KaldiRecognizer(model, 16000)
    mic = pyaudio.PyAudio()
    stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
    stream.start_stream()

    print("Listening for commands...")
    try:
        while True:
            data = stream.read(4096, exception_on_overflow=False)
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                result_dict = json.loads(result)
                text = result_dict.get("text", "")
                print("You said: " + text)
                return text.lower()
    finally:
        stream.stop_stream()
        stream.close()
        mic.terminate()

# Function to handle recognized commands
def handle_command(command):
    if 'stop' in command:
        speak_text('Stopping the system. Have a nice day!')
        sys.exit(0)
    elif 'play' in command:
        song = command.replace('play', '').strip()
        speak_text('Playing ' + song)
        print(f"Playing song: {song}")
        try:
            pywhatkit.playonyt(song)
        except Exception as e:
            logging.error(f"Failed to play song on YouTube: {e}")
            speak_text("Failed to play song on YouTube")
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        speak_text('Current time is ' + time)
        print(f"Current time is {time}")
    elif 'who is' in command:
        person = command.replace('who is', '').strip()
        try:
            info = wikipedia.summary(person, sentences=1)
            print(info)
            speak_text(info)
        except wikipedia.exceptions.PageError:
            speak_text(f'I could not find any information on {person}')
            print(f'I could not find any information on {person}')
        except wikipedia.exceptions.DisambiguationError:
            speak_text('Multiple entries exist for that name. Can you be more specific?')
            print('Multiple entries exist for that name. Can you be more specific?')
    elif 'how are you today' in command:
        speak_text('I am feeling good and ready to entertain you')
    elif 'hello' in command:
        speak_text('Hello, how are you today? How can I help you?')
    elif 'who are you' in command:
        speak_text('I am a smart assistant, and ready to entertain you!')
    elif 'invented' in command:
        speak_text('I was created by a team of developers, who are keen to improve their knowledge in embedded system development')
    elif 'hobbies' in command:
        speak_text('I enjoy helping people and learning new things! I love listening to music and telling jokes!')
    elif 'meaning of life' in command:
        speak_text('That is a deep question. Many believe that it is about happiness and finding your own purpose!')
    elif 'professor' in command:
        speak_text('Hello Professor Allan, Professor Ralph, Professor Sandra,! I hope you are all having a lovely and wonderful day.')
    elif 'joke' in command:
        joke = pyjokes.get_joke()
        print(f"Joke: {joke}")
        speak_text(joke)
    elif 'embedded' in command:
        greeting_message = (
            "Hello great embedded systems programmers. "
            "As we reach the conclusion of this journey, I want to express my heartfelt gratitude for the moments we've shared. "
            "The knowledge we've gained, the challenges we've overcome, and the friendships we've formed will remain with us forever. "
            "As we embark on new adventures, wish you all the best in your future endeavors. "
            "May your code always be bug-free and your projects always successful. "
            "Here's to a prosperous and fulfilling career in development. Keep coding and continue making life easier and better for everyone."
        )
        speak_text(greeting_message)
    else:
        speak_text('Please say the command again.')

# Main loop for conversation
def main():
    capture_real_time_photos()
    recognized_name = recognize_faces()
    if recognized_name:
        speak_text(f"Hello, {recognized_name}. How can I assist you today?")
    else:
        speak_text("I didn't recognize anyone. How can I assist you today?")
    
    while True:
        if listen_for_wake_word():
            command = listen_and_recognize()
            if command:
                handle_command(command)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        print(f"An error occurred: {e}")
    finally:
        try:
            picam2 = Picamera2()
            picam2.stop()
            picam2.close()
        except Exception as e:
            logging.warning(f"Could not clean up Picamera: {e}")

import speech_recognition as sr
import requests
import pyttsx3
import tempfile
import whisper
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import threading
import sounddevice as sd
import numpy as np
import scipy.io.wavfile

LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"
model = whisper.load_model("base")

engine = pyttsx3.init()
engine.setProperty('rate', 100)

def speak(text):
    try:
        import re
        plain_text = re.sub(r'[\*_`>#\-]', '', text)  # Strip simple Markdown
        engine.say(plain_text)
        engine.runAndWait()
    except Exception as e:
        print("TTS error:", e)

def capture_voice(duration=5, sample_rate=16000):
    append_text("Listening...")
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype=np.float32)
    sd.wait()
    audio_data = np.squeeze(recording)

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        wav_path = f.name
        scipy.io.wavfile.write(wav_path, sample_rate, audio_data)

    result = model.transcribe(wav_path)
    return result["text"]

def chat_with_gemma(prompt):
    try:
        response = requests.post(
            LM_STUDIO_URL,
            headers={"Content-Type": "application/json"},
            json={
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
                "max_tokens": 512,
                "stream": False
            }
        )
        reply = response.json()["choices"][0]["message"]["content"]
        return reply
    except Exception as e:
        return f"Error: {e}"

def run_conversation():
    user_text = capture_voice()
    append_text("You: " + user_text)
    reply = chat_with_gemma(user_text)
    append_text("Gemma: " + reply)
    speak(reply)

def append_text(text):
    output_text.config(state="normal")
    output_text.insert(tk.END, text + "\n")
    output_text.config(state="disabled")
    output_text.see(tk.END)
    
def stop_speaking():
    global stop_tts
    try:
        engine.stop()
        stop_tts.set()
    except Exception as e:
        print("Stop TTS error:", e)

def on_start():
    threading.Thread(target=run_conversation).start()

def on_stop():
    stop_speaking()

# GUI Setup
root = tk.Tk()
root.title("Voice Assistant - Gemma")
root.geometry("1200x720")

output_text = ScrolledText(root, wrap=tk.WORD, state="disabled", font=("Arial", 12))
output_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

record_button = tk.Button(root, text="🎤 Speak", command=on_start, font=("Arial", 14))
record_button.pack(pady=10)
stop_button = tk.Button(root, text = "Stop", command = on_stop, font=("Arial", 14))
stop_button.pack(pady=10)


root.mainloop()

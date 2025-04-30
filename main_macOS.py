import speech_recognition as sr
import requests
import tempfile
import whisper
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import threading
import sounddevice as sd
import numpy as np
import scipy.io.wavfile
import re
import subprocess

# Use your LM Studio local API endpoint
LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"

# Load Whisper model
model = whisper.load_model("base")

# Chat history for context
chat_history = [{"role": "system", "content": "Ti si korisni asistent."}]

def speak(text):
    try:
        result = subprocess.run(
            ["espeak", "-v", "Serbian", text], 
            capture_output=True, text=True
        )
        if result.returncode != 0:
            print("Error:", result.stderr)
        else:
            print("Output:", result.stdout)
    except Exception as e:
        print("Error with TTS:", e)

# Voice capture using mic + Whisper
def capture_voice(duration=5, sample_rate=16000):
    append_text("🎤 Slušam...")
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype=np.float32)
    sd.wait()
    audio_data = np.squeeze(recording)

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        wav_path = f.name
        scipy.io.wavfile.write(wav_path, sample_rate, audio_data)

    result = model.transcribe(wav_path,  language="sr")
    return result["text"]

# Send prompt to LLM via LM Studio
def chat_with_model(prompt):
    chat_history.append({"role": "user", "content": prompt})
    try:
        response = requests.post(
            LM_STUDIO_URL,
            headers={"Content-Type": "application/json"},
            json={
                "messages": chat_history,
                "temperature": 0.7,
                "max_tokens": 512,
                "stream": False
            }
        )
        reply = response.json()["choices"][0]["message"]["content"]
        chat_history.append({"role": "assistant", "content": reply})
        return reply
    except Exception as e:
        return f"Greška: {e}"

# Main conversation thread
def run_conversation():
    user_text = capture_voice()
    append_text("🧑‍💬 Ti: " + user_text)
    reply = chat_with_model(user_text)
    append_text("🤖 Asistent: " + reply)
    speak(reply)

# Append text to GUI
def append_text(text):
    output_text.config(state="normal")
    output_text.insert(tk.END, text + "\n")
    output_text.config(state="disabled")
    output_text.see(tk.END)

# GUI button handlers
def on_start():
    threading.Thread(target=run_conversation).start()

# Setup GUI
root = tk.Tk()
root.title("Glasovni Asistent - YugoGPT-Florida + say TTS")
root.geometry("1200x720")

output_text = ScrolledText(root, wrap=tk.WORD, state="disabled", font=("Arial", 12))
output_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

record_button = tk.Button(root, text="🎤 Pričaj", command=on_start, font=("Arial", 14))
record_button.pack(pady=5)

root.mainloop()


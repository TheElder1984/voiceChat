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
import asyncio
import edge_tts
import os

LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"
model = whisper.load_model("base")

tts_cancelled = threading.Event()
tts_thread = None

def speak(text):
    async def run_edge_tts():
        try:
            # Strip simple Markdown and emoji
            plain_text = re.sub(r'[\*_`>#\-]', '', text)
            plain_text = re.sub(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U00002600-\U000026FF\U00002700-\U000027BF]+', '', plain_text)

            temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            communicate = edge_tts.Communicate(text=plain_text, voice="en-US-AriaNeural")
            await communicate.save(temp_audio.name)
            if not tts_cancelled.is_set():
                os.system(f"ffplay -nodisp -autoexit -loglevel quiet {temp_audio.name}")
            os.unlink(temp_audio.name)
        except Exception as e:
            print("TTS error:", e)

    global tts_thread
    tts_cancelled.clear()
    tts_thread = threading.Thread(target=lambda: asyncio.run(run_edge_tts()))
    tts_thread.start()

def stop_speaking():
    global tts_cancelled
    tts_cancelled.set()
    # Playback is handled by ffplay, which exits automatically with stop signal


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
record_button.pack(pady=5)

stop_button = tk.Button(root, text="⏹ Stop", command=on_stop, font=("Arial", 14))
stop_button.pack(pady=5)

root.mainloop()

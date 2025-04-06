import speech_recognition as sr
import requests
import pyttsx3
import tempfile
import whisper
import scipy.io.wavfile

model = whisper.load_model("medium")  # or "small", "medium", "large"


def capture_voice(duration=5, sample_rate=16000):
    print("Speak now...")
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype=np.float32)
    sd.wait()
    audio_data = np.squeeze(recording)

    # Save to temporary WAV file
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        wav_path = f.name
        scipy.io.wavfile.write(wav_path, sample_rate, audio_data)

    result = model.transcribe(wav_path)
    print("You said:", result["text"])
    return result["text"]
        print("You said:", result["text"])
        return result["text"]
    except Exception as e:
        print("Error:", e)
        return ""

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
        return f"Error communicating with Gemma: {e}"

def speak(text):
    engine.say(text)
    engine.runAndWait()

def main():
    print("=== Voice Chat with Gemma ===")
    print("Say 'exit' to quit.")
    while True:
        user_input = capture_voice()
        if user_input.strip().lower() in ["exit", "quit"]:
            break
        reply = chat_with_gemma(user_input)
        print("Gemma:", reply)
        speak(reply)

if __name__ == "__main__":
    main()

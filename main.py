import speech_recognition as sr
import requests
import pyttsx3
import tempfile
import whisper

model = whisper.load_model("medium")  # or "small", "medium", "large"


def capture_voice():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak now...")
        audio = r.listen(source)

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp:
            wav_path = temp.name
            with open(wav_path, "wb") as f:
                f.write(audio.get_wav_data())
        
        result = model.transcribe(wav_path)
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

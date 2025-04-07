# Voice Gemma Chat (GUI Edition)

A GUI-based Python assistant app that combines:
- OpenAI Whisper for voice transcription
- Local LLM (Gemma via LM Studio)
- TTS via pyttsx3
- Tkinter GUI for a better user experience

## Features
- One-click voice input
- Real-time responses from Gemma
- Markdown-cleaned spoken responses

## Prerequisites
- Python 3.10+
- LM Studio with Gemma model running and API enabled (http://localhost:1234)
- Microphone access

## Installation
```bash
pip install -r requirements.txt
```

## Usage
```bash
python main.py
```

Click the microphone button and start speaking. Say "exit" or close the window to stop.

## Notes
- TTS removes markdown symbols to improve audio clarity.
- Ensure microphone access is allowed.
- If PyAudio gives install errors, use sounddevice instead.

## License
MIT

## Acknowledgments
- Whisper by OpenAI
- Gemma via LM Studio
- Python TTS and GUI libraries

# Srpski glasovni asistent za Linuks

A GUI-based Python assistant app that combines:
- Whisper for voice transcription
- Local LLM (e.g. Gemma via LM Studio)
- TTS RHVoice with ffplay playback
- Tkinter GUI for a better user experience

## Features
- One-click voice input
- Live transcription via Whisper
- Real-time responses from Gemma or any other LLM available in LM Studio
- Markdown and emoji are stripped from spoken text
- Stop button to interrupt speech immediately
- TTS runs in a separate thread using RHVoice
- SoundDevice-based recording for smoother audio capture

## Prerequisites
- Python 3.10+
- LM Studio with Gemma model running and API enabled (http://localhost:1234)
- ffplay (from ffmpeg) must be installed and available in PATH
- Microphone access

## Installation
```bash
pip install -r requirements.txt
```

## Usage
```bash
python main.py
```

Click the microphone button and start speaking. Use the stop button to interrupt speech output. Say "exit" or close the window to stop.

## Notes
- TTS removes markdown and emojis to improve audio clarity.
- Uses SoundDevice + Whisper for accurate voice capture.
- Uses RHVoice (rhvoice-macedonian) and high-quality speech.
- Ensure microphone access is allowed.

## License
GPL

## Acknowledgments
- Whisper
- an LLM via LM Studio
- RHVoice
- Python TTS and GUI libraries

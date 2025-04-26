# Srpski glasovni asistent za Linuks



![](https://github.com/TheElder1984/voiceChat/blob/4e762182867d0d92ace8f6ca25ff0e92e1418275/Zomi.png)






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
- an LLM via LM Studio [https://github.com/lmstudio-ai]
- RHVoice [https://github.com/RHVoice/RHVoice]
- Python TTS and GUI libraries


Want to customize or extend it?

    Try swapping the speech engine (e.g., Edge TTS, eSpeak, OpenAI Whisper).

    Add your favorite GUI tweaks!

    Hook up another model from LM Studio or Ollama!

If you like it, feel free to ⭐️ the repo and share your experiments!

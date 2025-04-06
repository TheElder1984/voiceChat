
# Voice Gemma Chat

Voice Gemma Chat is a Python-based voice assistant that integrates:
- OpenAI Whisper for speech recognition
- LM Studio with the Gemma model for local language processing
- Text-to-speech (TTS) using pyttsx3 for spoken responses

## Features
- Voice input via microphone
- Real-time interaction with the Gemma LLM
- Spoken replies using built-in TTS

## Prerequisites
- Python 3.10+
- [LM Studio](https://lmstudio.ai/) installed and running with the Gemma model
- LM Studio API enabled (default: http://localhost:1234)

## Installation
Clone the repository and install dependencies:

```bash
pip install -r requirements.txt
```

## Usage
Ensure LM Studio is running and listening on the API port. Then start the application:

```bash
python main.py
```

Say "exit" or "quit" to stop the session.

## Notes
- Microphone access is required
- Responses depend on the quality of the voice input and the configured model in LM Studio

## License
MIT License

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Acknowledgments
- [OpenAI Whisper](https://github.com/openai/whisper)
- [LM Studio](https://lmstudio.ai/)

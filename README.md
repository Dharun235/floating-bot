# Floating Bot 🤖

A lightweight desktop AI assistant that uses Ollama for real-time offline conversations with multilingual support and voice input.

## Features

- 🖥️ **Floating Desktop Window**: Always-on-top draggable window for quick access
- 🤖 **Offline AI**: Uses Ollama for completely offline AI conversations
- 🌍 **Multilingual**: Supports English and Swedish (easily extensible)
- 🎤 **Voice Input**: Speak your questions using microphone input
- ⚡ **Lightweight**: Uses efficient models like Phi-3 Mini for fast responses
- 🔒 **Privacy-First**: All data stays on your machine - no internet required for AI responses

## Prerequisites

### 1. Install Ollama

Download and install Ollama from [https://ollama.ai/](https://ollama.ai/)

For Linux/macOS:
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

For Windows:
Download the installer from the Ollama website.

### 2. Pull a Lightweight Model

After installing Ollama, pull a lightweight model:

```bash
# Recommended: Phi-3 Mini (3.8GB - fast and capable)
ollama pull phi3:mini

# Alternative: TinyLlama (0.6GB - very fast but less capable)
ollama pull tinyllama
```

### 3. Start Ollama Service

Make sure Ollama is running:
```bash
ollama serve
```

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/Dharun235/floating-bot.git
cd floating-bot
```

### 2. Install Python dependencies

#### On Ubuntu/Debian:
```bash
# Install system dependencies for audio
sudo apt-get update
sudo apt-get install python3-pyaudio portaudio19-dev espeak

# Install Python packages
pip install -r requirements.txt
```

#### On macOS:
```bash
# Install portaudio
brew install portaudio

# Install Python packages
pip install -r requirements.txt
```

#### On Windows:
```bash
# Install Python packages
pip install -r requirements.txt
```

**Note**: If you have trouble installing PyAudio, you can download pre-built wheels from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio).

## Usage

### Running the Application

```bash
python3 floating_bot.py
```

Or make it executable:
```bash
chmod +x floating_bot.py
./floating_bot.py
```

### Using the Bot

1. **Text Input**: Type your message in the input box and press Enter or click "Send"
2. **Voice Input**: Click the "🎤 Mic" button, speak your question, and it will automatically send
3. **Change Language**: Select your preferred language from the dropdown menu
4. **Change Model**: Update the model name if you want to use a different Ollama model
5. **Move Window**: Click and drag anywhere on the window to reposition it

### Keyboard Shortcuts

- **Enter**: Send message
- **Shift+Enter**: New line in input

## Configuration

Edit `config.json` to customize settings:

```json
{
  "model": "phi3:mini",           // Ollama model to use
  "language": "english",          // Default language
  "window_width": 400,            // Window width in pixels
  "window_height": 500,           // Window height in pixels
  "always_on_top": true,          // Keep window on top
  "supported_languages": {
    "english": "en-US",
    "swedish": "sv-SE"
  }
}
```

### Adding More Languages

To add more languages, update the `supported_languages` section in `config.json`:

```json
"supported_languages": {
  "english": "en-US",
  "swedish": "sv-SE",
  "spanish": "es-ES",
  "german": "de-DE",
  "french": "fr-FR"
}
```

## Recommended Models

For optimal performance, use these lightweight models:

| Model | Size | Speed | Quality | Command |
|-------|------|-------|---------|---------|
| phi3:mini | 3.8GB | Fast | High | `ollama pull phi3:mini` |
| tinyllama | 0.6GB | Very Fast | Medium | `ollama pull tinyllama` |
| gemma:2b | 1.4GB | Fast | Medium | `ollama pull gemma:2b` |

## Troubleshooting

### Ollama Connection Issues

If you see "Error connecting to Ollama":
1. Make sure Ollama is installed and running: `ollama serve`
2. Check that the Ollama API is accessible at `http://localhost:11434`
3. Verify your model is installed: `ollama list`

### Microphone Issues

If the microphone button doesn't work:
1. Make sure you have a working microphone connected
2. Check microphone permissions for your terminal/application
3. On Linux, ensure you have PulseAudio or ALSA properly configured
4. Try running: `python -m speech_recognition` to test your setup

### Model Not Found

If you see "Model not found" error:
```bash
# Pull the model first
ollama pull phi3:mini

# Or use a different model you have installed
ollama list  # See available models
```

### PyAudio Installation Issues

If PyAudio installation fails:
- **Linux**: `sudo apt-get install python3-pyaudio portaudio19-dev`
- **macOS**: `brew install portaudio && pip install pyaudio`
- **Windows**: Download wheel from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)

## Privacy & Data

- ✅ **All conversations happen locally** - no data is sent to external servers
- ✅ **Voice recognition requires internet** - Google Speech API is used for speech-to-text
- ✅ **AI processing is offline** - Ollama runs completely on your machine
- ✅ **No data collection** - this app doesn't collect or store any personal data

**Note**: If you need completely offline voice recognition, you can modify the code to use offline alternatives like Vosk or Whisper.

## Requirements

- Python 3.7+
- Ollama (for AI responses)
- Microphone (for voice input)
- 4GB+ RAM recommended
- 5GB+ disk space for models

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Author

Dharun235

## Acknowledgments

- [Ollama](https://ollama.ai/) - For providing the excellent local LLM platform
- [SpeechRecognition](https://github.com/Uberi/speech_recognition) - For speech-to-text capabilities
- [pyttsx3](https://github.com/nateshmbhat/pyttsx3) - For text-to-speech support
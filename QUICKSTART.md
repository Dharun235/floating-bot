# Quick Start Guide

## First Time Setup

1. **Install Ollama** (if not already installed):
   ```bash
   # Linux/macOS
   curl -fsSL https://ollama.ai/install.sh | sh
   
   # Windows - download from https://ollama.ai/
   ```

2. **Start Ollama service**:
   ```bash
   ollama serve
   ```

3. **Pull a model** (in a new terminal):
   ```bash
   ollama pull phi3:mini
   ```

4. **Install system dependencies** (Linux only):
   ```bash
   sudo apt-get update
   sudo apt-get install python3-pyaudio portaudio19-dev espeak
   ```

5. **Run the bot**:
   ```bash
   # Linux/macOS
   ./run.sh
   
   # Windows
   run.bat
   ```

## Daily Use

1. Start Ollama (if not running): `ollama serve`
2. Run the bot: `./run.sh` (or `run.bat` on Windows)
3. Type or speak your questions!

## Common Issues

### "Ollama not running"
- Make sure Ollama is started: `ollama serve`
- Check if it's accessible: `curl http://localhost:11434`

### "Model not found"
- Pull the model: `ollama pull phi3:mini`
- Or use another model you have: `ollama list`

### Microphone not working
- Check microphone permissions
- On Linux: Install `python3-pyaudio portaudio19-dev`
- Test: `python -m speech_recognition`

## Features

✅ **Text Chat**: Type messages and get AI responses
✅ **Voice Input**: Click mic button and speak
✅ **Multilingual**: Switch between English/Swedish
✅ **Offline**: No internet needed for AI (only voice recognition)
✅ **Floating Window**: Always on top, draggable
✅ **Fast**: Uses lightweight models

## Tips

- Press **Enter** to send messages
- Press **Shift+Enter** for new line
- **Drag** the window to move it
- Change **language** in settings dropdown
- Try different **models** for different speeds/quality

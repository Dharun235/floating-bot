#!/usr/bin/env python3
"""
Floating Bot - Desktop AI Assistant with Ollama
A lightweight, offline desktop bot that uses Ollama for real-time conversations
with support for multiple languages and voice input.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import json
import threading
import os
import sys

try:
    import ollama
except ImportError:
    print("Error: ollama package not installed. Run: pip install ollama")
    sys.exit(1)

try:
    import speech_recognition as sr
except ImportError:
    print("Error: speech_recognition package not installed. Run: pip install SpeechRecognition")
    sys.exit(1)

try:
    import pyttsx3
except ImportError:
    print("Warning: pyttsx3 package not installed. Text-to-speech will be disabled.")
    pyttsx3 = None


class FloatingBot:
    def __init__(self, root):
        self.root = root
        self.root.title("Floating Bot")
        
        # Load configuration
        self.config = self.load_config()
        
        # Setup window
        self.setup_window()
        
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.is_listening = False
        
        # Initialize text-to-speech
        if pyttsx3:
            try:
                self.tts_engine = pyttsx3.init()
                self.tts_enabled = True
            except Exception:
                self.tts_enabled = False
        else:
            self.tts_enabled = False
        
        # Create UI
        self.create_ui()
        
        # Check Ollama connection
        self.check_ollama()
        
    def load_config(self):
        """Load configuration from config.json"""
        config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Default configuration
            return {
                "model": "phi3:mini",
                "language": "english",
                "window_width": 400,
                "window_height": 500,
                "always_on_top": True,
                "supported_languages": {
                    "english": "en-US",
                    "swedish": "sv-SE"
                }
            }
    
    def save_config(self):
        """Save current configuration to config.json"""
        config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        with open(config_path, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def setup_window(self):
        """Configure the floating window"""
        width = self.config.get('window_width', 400)
        height = self.config.get('window_height', 500)
        
        # Center window on screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        # Make window stay on top if configured
        if self.config.get('always_on_top', True):
            self.root.attributes('-topmost', True)
        
        # Make window draggable
        self.root.bind('<Button-1>', self.start_move)
        self.root.bind('<B1-Motion>', self.do_move)
        
    def start_move(self, event):
        """Start moving the window"""
        self.x = event.x
        self.y = event.y
        
    def do_move(self, event):
        """Move the window"""
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")
    
    def create_ui(self):
        """Create the user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="🤖 Floating Bot", font=('Arial', 14, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        # Settings frame
        settings_frame = ttk.LabelFrame(main_frame, text="Settings", padding="5")
        settings_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        settings_frame.columnconfigure(1, weight=1)
        
        # Language selection
        ttk.Label(settings_frame, text="Language:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.language_var = tk.StringVar(value=self.config.get('language', 'english'))
        language_combo = ttk.Combobox(
            settings_frame, 
            textvariable=self.language_var,
            values=list(self.config.get('supported_languages', {}).keys()),
            state='readonly',
            width=15
        )
        language_combo.grid(row=0, column=1, sticky=tk.W)
        language_combo.bind('<<ComboboxSelected>>', self.on_language_change)
        
        # Model selection
        ttk.Label(settings_frame, text="Model:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5), pady=(5, 0))
        self.model_var = tk.StringVar(value=self.config.get('model', 'phi3:mini'))
        model_entry = ttk.Entry(settings_frame, textvariable=self.model_var, width=20)
        model_entry.grid(row=1, column=1, sticky=tk.W, pady=(5, 0))
        
        # Chat display
        chat_frame = ttk.LabelFrame(main_frame, text="Conversation", padding="5")
        chat_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        chat_frame.columnconfigure(0, weight=1)
        chat_frame.rowconfigure(0, weight=1)
        
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame, 
            wrap=tk.WORD, 
            height=15,
            font=('Arial', 10)
        )
        self.chat_display.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.chat_display.config(state=tk.DISABLED)
        
        # Input frame
        input_frame = ttk.Frame(main_frame)
        input_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E))
        input_frame.columnconfigure(0, weight=1)
        
        # Text input
        self.input_text = tk.Text(input_frame, height=3, font=('Arial', 10))
        self.input_text.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        self.input_text.bind('<Return>', self.on_enter_key)
        
        # Buttons frame
        buttons_frame = ttk.Frame(input_frame)
        buttons_frame.grid(row=0, column=1)
        
        # Microphone button
        self.mic_button = ttk.Button(
            buttons_frame, 
            text="🎤 Mic", 
            command=self.toggle_microphone,
            width=8
        )
        self.mic_button.grid(row=0, column=0, pady=(0, 5))
        
        # Send button
        self.send_button = ttk.Button(
            buttons_frame, 
            text="Send", 
            command=self.send_message,
            width=8
        )
        self.send_button.grid(row=1, column=0)
        
        # Clear button
        clear_button = ttk.Button(
            buttons_frame, 
            text="Clear", 
            command=self.clear_chat,
            width=8
        )
        clear_button.grid(row=2, column=0, pady=(5, 0))
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(5, 0))
    
    def on_language_change(self, event):
        """Handle language change"""
        self.config['language'] = self.language_var.get()
        self.save_config()
        self.update_status(f"Language changed to {self.language_var.get()}")
    
    def check_ollama(self):
        """Check if Ollama is running and model is available"""
        def check():
            try:
                # Try to list models
                models = ollama.list()
                model_name = self.config.get('model', 'phi3:mini')
                
                # Check if the configured model is available
                model_exists = any(model.get('model', '') == model_name or 
                                 model.get('name', '') == model_name 
                                 for model in models.get('models', []))
                
                if not model_exists:
                    self.update_chat(
                        "System", 
                        f"Model '{model_name}' not found. Please run:\n"
                        f"ollama pull {model_name}\n"
                        f"Alternative lightweight models: phi3:mini, tinyllama"
                    )
                else:
                    self.update_status(f"Connected to Ollama - Model: {model_name}")
                    self.update_chat("System", f"Ready! Using model: {model_name}")
            except Exception as e:
                self.update_chat(
                    "System", 
                    f"Error connecting to Ollama: {str(e)}\n"
                    "Please make sure Ollama is installed and running.\n"
                    "Visit: https://ollama.ai/"
                )
        
        threading.Thread(target=check, daemon=True).start()
    
    def update_status(self, message):
        """Update status bar"""
        self.status_var.set(message)
    
    def update_chat(self, sender, message):
        """Update chat display"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"{sender}: {message}\n\n")
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
    
    def clear_chat(self):
        """Clear chat display"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.config(state=tk.DISABLED)
        self.update_status("Chat cleared")
    
    def on_enter_key(self, event):
        """Handle Enter key press"""
        if event.state & 0x1:  # Shift+Enter - new line
            return
        else:  # Enter - send message
            self.send_message()
            return 'break'  # Prevent default behavior
    
    def send_message(self):
        """Send message to Ollama"""
        message = self.input_text.get(1.0, tk.END).strip()
        if not message:
            return
        
        # Clear input
        self.input_text.delete(1.0, tk.END)
        
        # Update chat
        self.update_chat("You", message)
        
        # Disable buttons during processing
        self.send_button.config(state=tk.DISABLED)
        self.mic_button.config(state=tk.DISABLED)
        self.update_status("Thinking...")
        
        # Process in separate thread
        threading.Thread(target=self.get_ollama_response, args=(message,), daemon=True).start()
    
    def get_ollama_response(self, message):
        """Get response from Ollama"""
        try:
            model = self.model_var.get()
            language = self.language_var.get()
            
            # Create language-specific prompt
            if language == "swedish":
                system_prompt = "Du är en hjälpsam assistent. Svara på svenska."
            else:
                system_prompt = "You are a helpful assistant."
            
            # Get response from Ollama
            response = ollama.chat(
                model=model,
                messages=[
                    {'role': 'system', 'content': system_prompt},
                    {'role': 'user', 'content': message}
                ]
            )
            
            bot_response = response['message']['content']
            
            # Update UI
            self.root.after(0, lambda: self.update_chat("Bot", bot_response))
            self.root.after(0, lambda: self.update_status("Ready"))
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            self.root.after(0, lambda: self.update_chat("System", error_msg))
            self.root.after(0, lambda: self.update_status("Error occurred"))
        finally:
            # Re-enable buttons
            self.root.after(0, lambda: self.send_button.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.mic_button.config(state=tk.NORMAL))
    
    def toggle_microphone(self):
        """Toggle microphone listening"""
        if self.is_listening:
            self.stop_listening()
        else:
            self.start_listening()
    
    def start_listening(self):
        """Start listening to microphone"""
        self.is_listening = True
        self.mic_button.config(text="⏹ Stop")
        self.update_status("Listening...")
        
        threading.Thread(target=self.listen_to_microphone, daemon=True).start()
    
    def stop_listening(self):
        """Stop listening to microphone"""
        self.is_listening = False
        self.mic_button.config(text="🎤 Mic")
        self.update_status("Ready")
    
    def listen_to_microphone(self):
        """Listen to microphone and convert speech to text"""
        try:
            with sr.Microphone() as source:
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                # Listen for audio
                audio = self.recognizer.listen(source, timeout=10)
                
                # Stop listening
                self.root.after(0, self.stop_listening)
                self.root.after(0, lambda: self.update_status("Processing speech..."))
                
                # Get language code
                language = self.language_var.get()
                language_code = self.config.get('supported_languages', {}).get(language, 'en-US')
                
                # Convert speech to text
                text = self.recognizer.recognize_google(audio, language=language_code)
                
                # Insert text into input field and send
                self.root.after(0, lambda: self.input_text.insert(1.0, text))
                self.root.after(0, self.send_message)
                
        except sr.WaitTimeoutError:
            self.root.after(0, lambda: self.update_status("No speech detected"))
            self.root.after(0, self.stop_listening)
        except sr.UnknownValueError:
            self.root.after(0, lambda: self.update_status("Could not understand speech"))
            self.root.after(0, self.stop_listening)
        except sr.RequestError as e:
            self.root.after(0, lambda: self.update_status(f"Speech recognition error: {e}"))
            self.root.after(0, self.stop_listening)
        except Exception as e:
            self.root.after(0, lambda: self.update_chat("System", f"Microphone error: {str(e)}"))
            self.root.after(0, self.stop_listening)


def main():
    """Main entry point"""
    root = tk.Tk()
    app = FloatingBot(root)
    root.mainloop()


if __name__ == "__main__":
    main()

# Floating Bot UI Design

## Window Layout

```
┌─────────────────────────────────────────┐
│         🤖 Floating Bot                 │  ← Title Bar (Draggable)
├─────────────────────────────────────────┤
│ ┌─ Settings ──────────────────────────┐ │
│ │ Language:  [English        ▼]       │ │  ← Language Selector
│ │ Model:     [phi3:mini___________]   │ │  ← Model Input
│ └─────────────────────────────────────┘ │
│                                         │
│ ┌─ Conversation ──────────────────────┐ │
│ │                                     │ │
│ │ System: Ready! Using model:         │ │
│ │ phi3:mini                           │ │
│ │                                     │ │
│ │ You: What's the weather like?       │ │
│ │                                     │ │  ← Chat Display
│ │ Bot: I apologize, but I don't      │ │    (Scrollable)
│ │ have access to real-time weather   │ │
│ │ information...                      │ │
│ │                                     │ │
│ │▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒│ │  ← Scrollbar
│ └─────────────────────────────────────┘ │
│                                         │
│ ┌──────────────────────┐  ┌─────────┐  │
│ │                      │  │ 🎤 Mic  │  │  ← Mic Button
│ │  Type message here   │  ├─────────┤  │
│ │                      │  │  Send   │  │  ← Send Button
│ └──────────────────────┘  ├─────────┤  │
│                           │  Clear  │  │  ← Clear Button
│                           └─────────┘  │
│                                         │
│ Ready                                   │  ← Status Bar
└─────────────────────────────────────────┘

Window Size: 400x500 pixels
```

## UI Elements Description

### Header
- **Title**: "🤖 Floating Bot" - Identifies the application
- **Draggable**: Click and drag anywhere on the title to move window

### Settings Panel
- **Language Dropdown**: Select conversation language (English/Swedish)
- **Model Field**: Configure which Ollama model to use
- Updates are saved automatically to config.json

### Conversation Display
- **Scrollable Text Area**: Shows conversation history
- **Message Format**: 
  - "System:" for system messages
  - "You:" for user messages
  - "Bot:" for AI responses
- **Auto-scroll**: Automatically scrolls to latest message

### Input Area
- **Text Box**: Multi-line input for typing messages
  - Enter: Send message
  - Shift+Enter: New line
- **Mic Button**: 
  - Click to start listening
  - Changes to "⏹ Stop" while recording
  - Automatically sends recognized speech
- **Send Button**: Sends the typed message
- **Clear Button**: Clears conversation history

### Status Bar
- Shows current status:
  - "Ready" - Idle state
  - "Listening..." - Recording audio
  - "Processing speech..." - Converting speech to text
  - "Thinking..." - Waiting for AI response
  - Error messages when issues occur

## Window Behavior

### Always On Top
- Window stays above other applications
- Can be disabled in config.json

### Draggable
- Click and hold title bar to move window
- Position is not saved between sessions

### Resizable
- Current implementation has fixed size
- Width: 400px, Height: 500px
- Can be modified in config.json

## Color Scheme
- Default system theme (matches OS)
- Clean, minimal design
- Standard tkinter styling

## Keyboard Shortcuts
- **Enter**: Send message
- **Shift+Enter**: New line in input

## States

### Ready State
```
🎤 Mic button: Active
Send button: Active
Input field: Editable
Status: "Ready"
```

### Listening State
```
🎤 Mic button: Changes to "⏹ Stop"
Send button: Disabled
Input field: Disabled
Status: "Listening..."
```

### Processing State
```
🎤 Mic button: Disabled
Send button: Disabled
Input field: Editable but queued
Status: "Thinking..."
```

## Responsive Design
- Text wraps automatically in chat display
- Scrollbar appears when content exceeds view
- Buttons remain accessible at all times

## Accessibility
- Clear visual feedback for all actions
- Status bar provides text updates
- Keyboard navigation supported
- Screen reader compatible (tkinter standard)

## Examples

### Example Conversation
```
System: Ready! Using model: phi3:mini

You: Hej! Hur mår du?

Bot: Hej! Jag mår bra, tack för att du frågar. 
Hur kan jag hjälpa dig idag?

You: What's the capital of Sweden?

Bot: The capital of Sweden is Stockholm. It's the 
largest city in Sweden and serves as the country's 
political, economic, and cultural center.
```

### Example with Voice Input
```
[User clicks 🎤 Mic button]
Status: "Listening..."

[User speaks: "Tell me about Stockholm"]
Status: "Processing speech..."

You: Tell me about Stockholm

Status: "Thinking..."

Bot: Stockholm is the capital and largest city 
of Sweden. It's known for its beautiful archipelago, 
historic old town (Gamla Stan), and modern design...
```

## Platform Differences

### Linux
- Native GTK/Qt theme integration
- Standard window decorations

### macOS
- Aqua theme integration
- May have rounded corners

### Windows
- Windows 10/11 theme integration
- Standard title bar

All platforms maintain the same functionality and layout.

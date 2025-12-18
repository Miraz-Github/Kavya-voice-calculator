# Kavya-voice-calculator



### System Dependencies

**For macOS:**
```bash
brew install portaudio
```

**For Windows:**
- No additional system packages needed

## Installation

1. **Clone or download this project**

2. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

If you encounter issues with PyAudio on Windows, try:
```bash
pip install pipwin
pipwin install pyaudio
```

## Usage

1. **Start the Flask server:**
```bash
python app.py
```

2. **Open your browser and navigate to:**
```
http://127.0.0.1:5000
```

3. **Use the calculator:**
   - **Manual Mode**: Click the buttons to input numbers and operations
   - **Voice Mode**: 
     - Click the 🎤 microphone icon in the top right
     - Click "Start Listening"
     - Speak your calculation (e.g., "five plus three times two")
     - The result will appear automatically

## Voice Commands Operations
- **Addition**: "plus", "add"
- **Subtraction**: "minus", "subtract"
- **Multiplication**: "times", "multiply", "multiplied by"
- **Division**: "divide", "divided by"
- **Power**: "power", "to the power of", "squared", "cubed"



## Troubleshooting

### Microphone Not Working
- Ensure your browser has microphone permissions
- Check system microphone settings
- Try a different browser (Chrome recommended)

### PyAudio Installation Issues
**Windows:**
```bash
pip install pipwin
pipwin install pyaudio
```

**Linux:**
```bash
sudo apt-get install python3-pyaudio portaudio19-dev
```

**macOS:**
```bash
brew install portaudio
pip install pyaudio
```

### Speech Recognition Errors
- Check your internet connection (Google Speech API requires internet)
- Speak clearly and at a moderate pace
- Reduce background noise

### pyttsx3 Not Speaking
**Linux:** Install espeak
```bash
sudo apt-get install espeak
```

**macOS/Windows:** Should work out of the box

## API Endpoints

### POST /api/listen
Listens for voice input and returns calculation result
- **Response**: `{success: bool, text: string, expression: string, result: string}`

### POST /api/speak
Speaks the provided text
- **Body**: `{text: string}`
- **Response**: `{success: bool}`

### POST /api/calculate
Calculates expression from text command
- **Body**: `{command: string}`
- **Response**: `{success: bool, expression: string, result: string}`


## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Speech Recognition**: Google Speech Recognition API
- **Text-to-Speech**: pyttsx3
- **Natural Language Processing**: word2number

## License

Free to use and modify for personal and educational purposes.

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## Support

If you encounter any issues:
1. Check the troubleshooting section
2. Ensure all dependencies are installed correctly
3. Verify your microphone is working
4. Check the browser console for error messages

---


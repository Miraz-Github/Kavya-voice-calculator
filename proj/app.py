from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import speech_recognition as sr
import pyttsx3
from word2number import w2n
import re
import threading
import queue

app = Flask(__name__)
CORS(app)

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty("rate", 160)
voices = engine.getProperty("voices")
if voices:
    engine.setProperty("voice", voices[0].id)

# Initialize speech recognizer
recognizer = sr.Recognizer()

# Queue for thread-safe speech operations
speech_queue = queue.Queue()

def speak_worker():
    """Background worker to handle speech synthesis"""
    while True:
        text = speech_queue.get()
        if text is None:
            break
        try:
            engine.say(text)
            engine.runAndWait()
        except:
            pass
        speech_queue.task_done()

# Start speech worker thread
speech_thread = threading.Thread(target=speak_worker, daemon=True)
speech_thread.start()

def speak(text):
    """Queue text for speech synthesis"""
    speech_queue.put(text)

def words_to_numbers(text):
    """Convert word numbers to digit numbers"""
    words = text.split()
    converted = []

    for word in words:
        try:
            converted.append(str(w2n.word_to_num(word)))
        except ValueError:
            converted.append(word)

    return " ".join(converted)

def calculate(command):
    """Parse voice command and calculate result"""
    try:
        # Replace operation words with symbols
        replacements = {
            "plus": "+",
            "add": "+",
            "minus": "-",
            "subtract": "-",
            "times": "*",
            "multiply": "*",
            "multiplied by": "*",
            "x": "*",
            "divide": "/",
            "divided by": "/",
            "power": "**",
            "to the power of": "**",
            "open parenthesis": "(",
            "open bracket": "(",
            "close parenthesis": ")",
            "close bracket": ")",
            "squared": "** 2",
            "cubed": "** 3",
            "percent": "/ 100",
            "percentage": "/ 100"
        }

        # Apply replacements
        for word, symbol in replacements.items():
            command = command.replace(word, symbol)

        # Convert word numbers to digits
        command = words_to_numbers(command)
        
        # Remove any non-mathematical characters
        command = re.sub(r"[^0-9+\-*/(). ]", "", command)
        
        # Remove extra spaces
        command = command.strip()

        print(f"Evaluating: {command}")
        
        if not command:
            return None, None
            
        # Evaluate the mathematical expression
        result = eval(command)
        
        # Format result
        if isinstance(result, float):
            if result.is_integer():
                result = int(result)
            else:
                result = round(result, 4)
        
        return command, result

    except (SyntaxError, ZeroDivisionError, NameError, TypeError) as e:
        print(f"Calculation error: {e}")
        return None, None

@app.route('/')
def index():
    """Serve the calculator HTML page"""
    return render_template('index.html')

@app.route('/api/listen', methods=['POST'])
def listen():
    """Listen for voice input and return recognized text"""
    try:
        with sr.Microphone() as source:
            print("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            
            print("Listening for speech...")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
        
        try:
            text = recognizer.recognize_google(audio)
            print(f"Recognized: {text}")
            
            # Calculate the result
            expression, result = calculate(text.lower())
            
            if result is not None:
                speak(f"The result is {result}")
                return jsonify({
                    'success': True,
                    'text': text,
                    'expression': expression,
                    'result': str(result)
                })
            else:
                speak("Sorry, I could not calculate that")
                return jsonify({
                    'success': False,
                    'error': 'Could not calculate',
                    'text': text
                })
        
        except sr.UnknownValueError:
            return jsonify({
                'success': False,
                'error': 'Could not understand audio'
            })
        except sr.RequestError as e:
            return jsonify({
                'success': False,
                'error': f'Speech recognition error: {str(e)}'
            })
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/speak', methods=['POST'])
def speak_text():
    """Speak the given text"""
    data = request.get_json()
    text = data.get('text', '')
    
    if text:
        speak(text)
        return jsonify({'success': True})
    
    return jsonify({'success': False, 'error': 'No text provided'})

@app.route('/api/calculate', methods=['POST'])
def api_calculate():
    """Calculate expression from text"""
    data = request.get_json()
    command = data.get('command', '')
    
    expression, result = calculate(command.lower())
    
    if result is not None:
        return jsonify({
            'success': True,
            'expression': expression,
            'result': str(result)
        })
    else:
        return jsonify({
            'success': False,
            'error': 'Invalid calculation'
        })

if __name__ == '__main__':
    print("Starting Voice Calculator Server...")
    print("Open http://127.0.0.1:5000 in your browser")
    app.run(debug=True, host='0.0.0.0', port=5000)

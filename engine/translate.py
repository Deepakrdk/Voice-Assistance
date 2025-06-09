import speech_recognition as sr
from deep_translator import GoogleTranslator
import pyttsx3

# Initialize components
recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()

def speak(text):
    """Convert text to speech"""
    tts_engine.say(text)
    tts_engine.runAndWait()

def listen():
    """Listen for voice command"""
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, timeout=5)
        
        try:
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't understand that")
            return None
        except sr.RequestError:
            speak("Speech service unavailable")
            return None

def translate_text(text, target_lang='es'):
    """Translate text using Google Translate"""
    try:
        translation = GoogleTranslator(source='auto', target=target_lang).translate(text)
        return translation
    except Exception as e:
        print(f"Translation error: {e}")
        return None

def main():
    speak("Welcome to voice translator. Say 'translate' followed by your phrase")
    
    while True:
        command = listen()
        
        if not command:
            continue
            
        if 'exit' in command or 'quit' in command:
            speak("Goodbye!")
            break
            
        if 'translate' in command:
            phrase = command.replace('translate', '').strip()
            if phrase:
                speak("What language should I translate to? For example, say Spanish, French, etc.")
                lang_command = listen()
                
                if lang_command:
                    lang_map = {
                        'spanish': 'es',
                        'french': 'fr',
                        'german': 'de',
                        'japanese': 'ja',
                        'chinese': 'zh-CN',
                        'arabic': 'ar',
                        'russian': 'ru',
                        'hindi': 'hi'
                    }
                    
                    target_code = 'es'  # Default to Spanish
                    for lang in lang_map:
                        if lang in lang_command:
                            target_code = lang_map[lang]
                            break
                    
                    translation = translate_text(phrase, target_code)
                    if translation:
                        speak(f"The translation is: {translation}")
                        print(f"Original: {phrase}\nTranslation: {translation}")
                    else:
                        speak("Translation failed")
            else:
                speak("Please say the phrase to translate after the word 'translate'")

if __name__ == "__main__":
    main()
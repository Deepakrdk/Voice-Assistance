import email
from email.header import decode_header
import imaplib
from io import BytesIO
import os
import random
import re
from shlex import quote
import smtplib
import sqlite3
import struct
import subprocess
import time
import webbrowser
import screen_brightness_control as sbc
import platform
import socket
from datetime import datetime
import pygetwindow as gw
from deep_translator import GoogleTranslator
import psutil
import requests
from playsound import playsound 
import eel
import pvporcupine
import pyaudio
import pyautogui
from engine.command import speak, takecommand
from engine.config import ASSISTANT_NAME
# playing assistant sound function
import pywhatkit as kit

from engine.helper import extract_yt_term, remove_words
from hugchat import hugchat


con = sqlite3.connect("nova.db")
cursor = con.cursor()

@eel.expose
def playAssistantSound():
    music_dir="www\\assets\\audio\\start_sound.mp3"
    playsound(music_dir)


def opencommand(query):
    try:
        # Clean and prepare the query
        query = query.replace(ASSISTANT_NAME, "").replace("open", "").strip().lower()
        
        if not query:
            speak("Please specify what to open")
            return

        # Try to find in local applications
        cursor.execute('SELECT path FROM sys_command WHERE LOWER(name) = ?', (query,))
        results = cursor.fetchall()
        
        if results:
            speak(f"Opening {query}")
            os.startfile(results[0][0])
            return

        # Try to find in web commands
        cursor.execute('SELECT url FROM web_command WHERE LOWER(name) = ?', (query,))
        results = cursor.fetchall()
        
        if results:
            speak(f"Opening {query}")
            webbrowser.open(results[0][0])
            return

        # Try direct system command as fallback
        try:
            speak(f" Opening {query}")
            os.system(f'start {query}')
        except Exception as e:
            speak(f"Sorry, I couldn't find {query}")
            print(f"Error: {e}")

    except sqlite3.Error as db_error:
        speak("There was a database error")
        print(f"Database error: {db_error}")
    except Exception as e:
        speak("An unexpected error occurred")
        print(f"Error: {e}")








def closecommand(query):
    try:
        # Clean and prepare the query
        query = query.replace(ASSISTANT_NAME, "").replace("close", "").strip().lower()

        if not query:
            speak("Please specify what to close")
            return

        # Try to find in local applications
        cursor.execute('SELECT process_name FROM sys_close WHERE LOWER(name) = ?', (query,))
        results = cursor.fetchall()

        if results:
            exe_name = results[0][0]  # e.g., "chrome.exe"
            speak(f"Closing {query}")
            os.system(f'taskkill /f /im {exe_name}')
            return

        # Try direct kill as fallback
        speak(f" Closing {query}")
        os.system(f'taskkill /f /im {query}.exe')

    except sqlite3.Error as db_error:
        speak("There was a database error")
        print(f"Database error: {db_error}")
    except Exception as e:
        speak("An unexpected error occurred while trying to close the application")
        print(f"Error: {e}")










def PlayYoutube(query):
    search_term = extract_yt_term(query)
    speak("Playing "+search_term+" on Youtube")
    kit.playonyt(search_term)
    
    
    
    
    

    
    
save_path = "C:\\Users\\deepa\\OneDrive\\Pictures\\Screenshots"
def take_screenshot_with_custom_name():
    speak("What should I name the screenshot?")
    filename = takecommand()
    if filename:
        filename = filename.replace(" ", "_") + ".png"
        full_path = os.path.join(save_path, filename)
        screenshot = pyautogui.screenshot()
        screenshot.save(full_path)
        speak(f"Screenshot saved as {filename}")
    else:
        speak("No valid name provided. Screenshot not saved.")    
        
        
        
    

    
    
    
    
    


def hotword():
    porcupine=None
    paud=None
    audio_stream=None
    try:
       
        # pre trained keywords    
        porcupine=pvporcupine.create(keywords=["jarvis","bumblebee",]) 
        paud=pyaudio.PyAudio()
        audio_stream=paud.open(rate=porcupine.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=porcupine.frame_length)
        
        # loop for streaming
        while True:
            keyword=audio_stream.read(porcupine.frame_length)
            keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)

            # processing keyword comes from mic 
            keyword_index=porcupine.process(keyword)

            # checking first keyword detetcted for not
            if keyword_index>=0:
                print("hotword detected")

                # pressing shorcut key win+j
                import pyautogui as autogui
                autogui.keyDown("win")
                autogui.press("j")
                time.sleep(2)
                autogui.keyUp("win")
                
    except:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()

 
# Find contacts
def findContact(query):
    
    
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'whatsapp', 'video']
    query = remove_words(query, words_to_remove)

    try:
        query = query.strip().lower()
        cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
        results = cursor.fetchall()
        print(results[0][0])
        mobile_number_str = str(results[0][0])

        if not mobile_number_str.startswith('+91'):
            mobile_number_str = '+91' + mobile_number_str

        return mobile_number_str, query
    except:
        speak('not exist in contacts')
        return 0, 0
    

def whatsApp(mobile_no, message, flag, name):

    if flag == 'message':
        target_tab = 20
        jarvis_message = "message send successfully to "+name
           
    elif flag == 'call':
        target_tab = 14
        message = ''
        jarvis_message = "calling to "+name

    else:
        target_tab = 13
        message = ''
        jarvis_message = "staring video call with "+name

        #hi deepak how are you

    # Encode the message for URL
    encoded_message = quote(message)
    print(encoded_message)
    # Construct the URL
    whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"

    # Construct the full command
    full_command = f'start "" "{whatsapp_url}"'

    # Open WhatsApp with the constructed URL using cmd.exe
    subprocess.run(full_command, shell=True)
    time.sleep(5)
    subprocess.run(full_command, shell=True)
    
    pyautogui.hotkey('ctrl', 'f')

    for i in range(1, target_tab):
        pyautogui.hotkey('tab')

    pyautogui.hotkey('enter')
    speak(jarvis_message)  


















# chat bot 
def chatBot(query):
    user_input = query.lower()
    chatbot = hugchat.ChatBot(cookie_path="engine\\cookies.json")
    id = chatbot.new_conversation()
    chatbot.change_conversation(id)
    
    # Get response (this returns a Message object)
    msg = chatbot.chat(f"Respond briefly in 30 words: {user_input}")
    
    # Convert Message to string and limit words
    response = str(msg)
    response = ' '.join(response.split()[:40])  # Force 30-word limit
    
    print(response)
    speak(response)
    return response

#chatbot for calculation

def chatBots(query):
    user_input = query.lower()
    chatbot = hugchat.ChatBot(cookie_path="engine\\cookies.json")
    id = chatbot.new_conversation()
    chatbot.change_conversation(id)
    
    # Get response (this returns a Message object)
    msg = chatbot.chat(f"Respond briefly in 2 words or less: {user_input}")
    
    # Convert Message to string and limit words
    response = str(msg)
    response = ' '.join(response.split()[:40])  # Force 30-word limit
    
    print("The answer is : "+response)
    speak("The answer is : "+response)
    return response



def get_weather(city):
    """Fetch weather data from OpenWeatherMap API"""
    API_KEY = "2d12b935291d97573e11ee087a0acf34"  # Get a free API key from https://openweathermap.org/
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
    
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'  # Celsius (use 'imperial' for Fahrenheit)
    }
    
    try:
        response = requests.get(BASE_URL, params=params)
        data = response.json()
        
        if data["cod"] != 200:
            speak(f"Sorry, I couldn't find weather for {city}.")
            return
        
        weather = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        
        result = f"Weather in {city}: {weather}, Temperature: {temp}°C, Humidity: {humidity}%"
        print(result)
        speak(result)
    
    except Exception as e:
        speak("Sorry, there was an error fetching weather data.")
        print(f"Error: {e}")
        
        
        
        



def translate_text(text, target_lang='es'):
    """Translate the text into the target language"""
    try:
        translation = GoogleTranslator(source='auto', target=target_lang).translate(text)
        return translation
    except Exception as e:
        print(f"Translation error: {e}")
        return None
    
    
    
    


def check_battery():
    battery = psutil.sensors_battery()
    percent = battery.percent
    plugged = "plugged in" if battery.power_plugged else "not plugged in"
    message = f"Our system battery is {percent}% and {plugged}"
    
    if not battery.power_plugged and percent < 20:
        message += ". Warning! Low battery!"
    
    print(message)
    speak(message)
    
    
def test_download_speed():
    try:
        test_url = "https://eu.httpbin.org/stream-bytes/10000000"  # 10MB test file
        start_time = time.time()
        response = requests.get(test_url, stream=True)
        total_bytes = 0
        for chunk in response.iter_content(chunk_size=1024):
            total_bytes += len(chunk)
            if time.time() - start_time > 10:  # Limit to 10 seconds
                break
        duration = time.time() - start_time
        return (total_bytes * 8) / duration / 1_000_000  # Convert to Mbps
    except Exception as e:
        speak(f"Download test failed: {str(e)}")
        return None    
    
def test_upload_speed():
    try:
        upload_url = "https://httpbin.org/post"
        test_data = BytesIO(b'0' * 5_000_000)  # 5MB test data
        start_time = time.time()
        requests.post(upload_url, files={'file': test_data})
        duration = time.time() - start_time
        return (5_000_000 * 8) / duration / 1_000_000  # Convert to Mbps
    except Exception as e:
        speak(f"Upload test failed: {str(e)}")
        return None
    
    
def run_speed_test():
    speak("Starting speed test...")
    print("Starting speed test...")
    
    # Test download speed
    speak("Testing download speed...")
    print("Testing download speed...")
    download_speed = test_download_speed()
    
    # Test upload speed
    speak("Testing upload speed...")
    print("Testing upload speed...")
    upload_speed = test_upload_speed()
    
    # Report results
    if download_speed and upload_speed:
        result = (f"The Download Speed is : {download_speed:.2f} Mbps, "
                 f"The Upload Speed is : {upload_speed:.2f} Mbps")
        speak("Speed test completed Sir. " )
        print("Speed test completed Sir. " )
        speak(result)
        print(result)
    else:
        speak("Speed test could not be completed") 
        print("Speed test could not be completed") 
        

def set_volume(change_type):
    """Change volume using Windows native commands"""
    try:
        if change_type == "increase":
            os.system(r'powershell -command "(New-Object -ComObject WScript.Shell).SendKeys([char]175)"')
            speak("Volume increased")
        elif change_type == "decrease":
            os.system(r'powershell -command "(New-Object -ComObject WScript.Shell).SendKeys([char]174)"')
            speak("Volume decreased")
        elif change_type == "mute":
            os.system(r'powershell -command "(New-Object -ComObject WScript.Shell).SendKeys([char]173)"')
            speak("Volume muted")
    except Exception as e:
        speak(f"Error: {str(e)}")   
        
        
        
def adjust_brightness(query):
    """Adjust brightness based on voice command"""
    
    try:
        current = sbc.get_brightness()
        if isinstance(current, list):
            current = current[0]  # Take first display if multiple

        if "increase system brightness" in query or "brightness up" in query :
            new_level = min(100, current + 10)
            sbc.set_brightness(new_level)
            speak(f"Brightness increased to {new_level}%")
            print(f"Brightness increased to {new_level}%")
        elif "decrease system brightness" in query or "brightness down" in query:
            new_level = max(0, current - 10)
            sbc.set_brightness(new_level)
            speak(f"Brightness decreased to {new_level}%")
            print(f"Brightness decreased to {new_level}%")
        else:
            print("Command not recognized. Say 'increase' or 'decrease'.")
    except Exception as e:
        print(f"Error adjusting brightness: {e}")
                
    
    
    
def minimize_window():
    """Minimize the currently active window"""
    try:
        active_window = gw.getActiveWindow()
        if active_window:
            active_window.minimize()
            print("Window minimized")
        else:
            print("No active window found")
    except Exception as e:
        print(f"Error minimizing window: {e}")

def maximize_window():
    """Maximize the currently active window"""
    try:
        active_window = gw.getActiveWindow()
        if active_window:
            active_window.maximize()
            print("Window maximized")
        else:
            print("No active window found")
    except Exception as e:
        print(f"Error maximizing window: {e}")

def toggle_window():
    """Minimize or restore window based on current state"""
    try:
        active_window = gw.getActiveWindow()
        if active_window:
            if active_window.isMaximized:
                active_window.restore()
                print("Window restored")
            else:
                active_window.maximize()
                print("Window maximized")
        else:
            print("No active window found")
    except Exception as e:
        print(f"Error toggling window: {e}")    
        
        
     
     



def get_basic_system_info():
    speak(" BASIC SYSTEM INFO ")
    print(" BASIC SYSTEM INFO ")
    
    # Operating System
    speak("Operating System info :")
    print("Operating System info :")
    speak(f"System: {platform.system()}")
    print(f"System: {platform.system()}")
    speak(f"Computer Name: {platform.node()}")
    print(f"Computer Name: {platform.node()}")
    speak(f"Release: {platform.release()}")
    print(f"Release: {platform.release()}")
    speak(f"Version: {platform.version()}")
    print(f"Version: {platform.version()}")
    
    # Processor
    speak("Processor info :")
    print("Processor info :")
    speak(f"Processor: {platform.processor()}")
    print(f"Processor: {platform.processor()}")
    speak(f"Architecture: {platform.machine()}")
    print(f"Architecture: {platform.machine()}")
    
    # Memory (Simplified Windows version)
    speak("Memory info :")
    print("Memory info :")
    if platform.system() == "Windows":
        try:
            import psutil
            mem = psutil.virtual_memory()
            speak(f"Total RAM: {round(mem.total / (1024**3), 2)} GB")
            print(f"Total RAM: {round(mem.total / (1024**3), 2)} GB")
            speak(f"Available: {round(mem.available / (1024**3), 2)} GB")
            print(f"Available: {round(mem.available / (1024**3), 2)} GB")
        except ImportError:
            speak("Install 'psutil' for detailed memory info (pip install psutil)")
            print("Install 'psutil' for detailed memory info (pip install psutil)")
    else:
        # Linux/Mac alternative
        try:
            with open('/proc/meminfo') as f:
                meminfo = f.read()
            total_mem = int(meminfo.split('MemTotal:')[1].split()[0])
            speak(f"Total RAM: {round(total_mem / 1024, 2)} GB")
            print(f"Total RAM: {round(total_mem / 1024, 2)} GB")
        except:
            speak("Could not determine memory info")
            print("Could not determine memory info")
    
    # Disk
    speak("Disk info :")
    print("Disk info :")
    speak(f"Current Directory: {os.getcwd()}")
    print(f"Current Directory: {os.getcwd()}")
    try:
        import psutil
        disk = psutil.disk_usage(os.getcwd())
        speak(f"Total Space: {round(disk.total / (1024**3), 2)} GB")
        print(f"Total Space: {round(disk.total / (1024**3), 2)} GB")
        speak(f"Used Space: {round(disk.used / (1024**3), 2)} GB")
        print(f"Used Space: {round(disk.used / (1024**3), 2)} GB")
        speak(f"Free Space: {round(disk.free / (1024**3), 2)} GB")
        print(f"Free Space: {round(disk.free / (1024**3), 2)} GB")
    except ImportError:
        speak("Install 'psutil' for disk info (pip install psutil)")
        print("Install 'psutil' for disk info (pip install psutil)")
    
    # Network
    speak("Network info :")
    print("Network info :")
    speak(f"Hostname: {socket.gethostname()}")
    print(f"Hostname: {socket.gethostname()}")
    try:
        speak(f"IP Address: {socket.gethostbyname(socket.gethostname())}")
        print(f"IP Address: {socket.gethostbyname(socket.gethostname())}")
    except:
        speak("Could not determine IP address")
        print("Could not determine IP address")
        
        
        
def enable_battery_saver_shortcut():
    try:
        # Open Action Center (Win + A)
        pyautogui.hotkey('win', 'a')
        time.sleep(1)
        pyautogui.hotkey('down')
        pyautogui.hotkey('enter')
        pyautogui.hotkey('win', 'a')
        
      
        print("Battery Saver activated via UI")
    except Exception as e:
        print(f"Error: {e}")      
        
def enable_night_light_shortcut():
    try:
        # Open Action Center (Win + A)
        pyautogui.hotkey('win', 'a')
        time.sleep(1)
        pyautogui.hotkey('down')
        pyautogui.hotkey('right')
        time.sleep(1)
        pyautogui.hotkey('enter')
        pyautogui.hotkey('win', 'a')
        
      
        print("Night light activated via UI")
    except Exception as e:
        print(f"Error: {e}")         
        
        
def enable_hotspot_shortcut():
    try:
        # Open Action Center (Win + A)
        pyautogui.hotkey('win', 'a')
        time.sleep(1)
        pyautogui.hotkey('down')
        pyautogui.hotkey('down')
        pyautogui.hotkey('right')
        time.sleep(1)
        pyautogui.hotkey('enter')
        pyautogui.hotkey('win', 'a')
        
      
        print("Hotspot activated via UI")
    except Exception as e:
        print(f"Error: {e}")  
        
      
def enable_bluetooth_shortcut():
    try:
        # Open Action Center (Win + A)
        pyautogui.hotkey('win', 'a')
        time.sleep(1)
        pyautogui.hotkey('right')
        time.sleep(1)
        pyautogui.hotkey('enter')
        pyautogui.hotkey('win', 'a')
        
      
        print("Bluetooth activated via UI")
    except Exception as e:
        print(f"Error: {e}")        
        
        
        
        
contacts = {
    "deepak": "deepakrdk50@gmail.com",
    "dinesh": "dineshkumar974704@gmail.com",
    "sivaji": "sivaji2001sivaji@gmail.com"
}

        
        
                      
               
def send_email(to_address, subject, message, from_address, password):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_address, password)
        email_content = f"Subject: {subject}\n\n{message}"
        server.sendmail(from_address, to_address, email_content)
        server.quit()
        speak("Email has been sent successfully!")
    except Exception as e:
        print(e)
        speak("Failed to send the email.")

def email_flow():
    speak("Who do you want to send the email to?")
    recipient = takecommand().replace(" ", "")  # Remove spaces from name
    to_address = contacts.get(recipient)

    if not to_address:
        # If name not found, treat input as email username and add @gmail.com
        to_address = recipient + "@gmail.com"
        speak(f"No saved contact found. Sending to {to_address}.")

    speak("What is the subject?")
    subject = takecommand()

    speak("What should I say in the email?")
    message = takecommand()

    from_address = "bumblebee2bumblebee@gmail.com"
    password = "tjjl dkaq qlru jpwg"  # Use app-specific password

    send_email(to_address, subject, message, from_address, password)



def read_emails():
    # Replace with your email and password (use App Password if 2FA is enabled)
    username = "deepakrdk50@gmail.com"
    password = "ioyp zetk bbdt ucpc"

    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(username, password)
        mail.select("inbox")

        status, messages = mail.search(None, 'UNSEEN')
        email_ids = messages[0].split()

        if not email_ids:
            speak("You have no new emails.")
            print("You have no new emails.")
        else:
            speak(f"You have {len(email_ids)} new email(s). Reading now.")
            print(f"You have {len(email_ids)} new email(s). Reading now.")
            for i, email_id in enumerate(email_ids[:5]):  # Read up to 5 emails
                res, msg_data = mail.fetch(email_id, "(RFC822)")
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        subject, encoding = decode_header(msg["Subject"])[0]
                        if isinstance(subject, bytes):
                            subject = subject.decode(encoding or "utf-8")
                        from_ = msg.get("From")
                        speak(f"Email {i+1} from {from_}. Subject: {subject}")
                        print(f"Email {i+1} from {from_}. Subject: {subject}")
        mail.logout()
    except Exception as e:
        speak("Failed to read emails.")
        print("Error:", str(e))



def get_roast():
    roasts = [
        "You're like a cloud. When you disappear, it's a beautiful day.",
        "You're like a broken pencil — ,pointless and hard to write with.",
        "You bring everyone so much joy..., when you leave the room.",
        "You have something on your face..., oh wait, that’s just your face.",
        "You're like Monday mornings — nobody likes you, and everyone just wants you to go away.",
        "You're like a software update—annoying and never on time.",
        "You're like a voice assistant stuck in airplane mode—useless and confused.",
        "You’re like a software update at 2AM — ,nobody asked for you, and you ruin everything.",
        "Your birth certificate is an apology letter from the hospital.",
        "Your parents must be so proud..., because at least they know they have one kid with a chance of success.",
        " If there was a contest for being dumb, you’d still manage to come second.",
        " Your parents must be so proud…, because at least they have one kid who didn’t turn out like you.",
        "I’d roast you, but I don’t want to be accused of bullying the mentally challenged.",
        "You’re the human equivalent of a ‘404 Error’—,nobody knows why you’re here.",
        "You’re not single by choice, you’re single by design.",
        "Your mirror must be cracked, because that confidence is delusional.",
        "You’re as useless as Meg…, and at least she has potential to be ignored."
    ]
    return random.choice(roasts)


def get_pickup_line():
    pickup = [
        "Are you French?, Because Eiffel for you.",
        "Are you a magician?, Because whenever I look at you, everyone else disappears.",
        "Do you have a name, or can I call you mine?",
        "Is your name Google?, Because you have everything I’ve been searching for.",
        "Is your dad a boxer?, Because you're a knockout!",
        "Do you believe in love at first sight, or should I walk by again?",
        "Are you made of copper and tellurium?, Because you're Cu-Te.",
        "Are you a campfire?, Because you're hot and I want s'more.",
        "Do you have a map?, Because I keep getting lost in your eyes.",
        "Do you have a Band-Aid?, Because I just scraped my knee falling for you."
    ]
    
    return random.choice(pickup)

def get_motivational_quote():
    motivation = [
        "The only way to do great work is to love what you do. – Steve Jobs",
        "Success is not the key to happiness. Happiness is the key to success. – Albert Schweitzer",
        "Believe you can and you're halfway there. – Theodore Roosevelt",
        "It always seems impossible until it’s done. – Nelson Mandela",
        "Don’t watch the clock; do what it does. Keep going. – Sam Levenson",
        "The future belongs to those who believe in the beauty of their dreams. – Eleanor Roosevelt",
        "You are never too old to set another goal or to dream a new dream. – C.S. Lewis",
        "The only limit to our realization of tomorrow is our doubts of today. – Franklin D. Roosevelt",
        "Success is the sum of small efforts, repeated day in and day out. – Robert Collier",
        "It’s not whether you get knocked down, it’s whether you get up. – Vince Lombardi",
        "Do not wait to strike till the iron is hot, but make it hot by striking. – William Butler Yeats",
        "Your limitation—it's only your imagination.",
        "Push yourself, because no one else is going to do it for you.",
        "Great things never come from comfort zones.",
        "Dream it. Wish it. Do it."
    ]
    
    return random.choice(motivation)
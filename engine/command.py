from datetime import datetime
import os
import random
import subprocess
import sys
import webbrowser
from deep_translator import GoogleTranslator
import pyautogui
import pyttsx3
import requests
import speech_recognition as sr
import urllib
import eel
import time
import pywhatkit as kit
import imdb
import tempfile
import os
import pygame
from gtts import gTTS
from requests import get
import pyjokes
import winshell


lang_map = {
    'spanish': 'es',
    'french': 'fr',
    'german': 'de',
    'japanese': 'ja',
    'chinese': 'zh-CN',
    'arabic': 'ar',
    'russian': 'ru',
    'hindi': 'hi',
    'italian': 'it',
    'korean': 'ko',
    'tamil': 'ta',
    'telugu': 'te'
}







def speak(text):
   text = str(text)
   engine = pyttsx3.init('sapi5')
   voices = engine.getProperty('voices')
   engine.setProperty('voice', voices[1].id)
   engine.setProperty('rate',174)
   eel.DisplayMessage(text)
   engine.say(text)
   eel.receiverText(text)
   engine.runAndWait()


def speaks(text, lang='en'):
    """Speak the given text in the given language using gTTS."""
    try:
        
        
        eel.DisplayMessage(text)
        eel.receiverText(text)
        
        # Create the speech file in the temp directory
        tts = gTTS(text=text, lang=lang)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            # Save speech to the file
            temp_path = fp.name
            print(f"Saving speech to {temp_path}")  # Debugging: Show the file path
            tts.save(temp_path)
        
        # Ensure pygame is initialized and play the speech
        pygame.mixer.init()
        pygame.mixer.music.load(temp_path)
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            continue
        
        pygame.mixer.quit()

        # Clean up the temp file
        os.remove(temp_path)
    except Exception as e:
        print(f"Speech error: {e}")
        
        







def takecommand():  
  
   r = sr.Recognizer()
   
   with sr.Microphone() as source:
      
      print('listening ...')
      eel.DisplayMessage('listening ...')
      r.pause_threshold = 1
      r.adjust_for_ambient_noise(source)

      audio = r.listen(source)

   try:
      print('recognizing ...')
      eel.DisplayMessage('recognizing ...')
      query = r.recognize_google(audio, language='en-in')
      print(f"user said: {query}")
      eel.DisplayMessage(query)
      time.sleep(1)
      
   except Exception as e:
      return ""
   
   return query.lower()

import sys

@eel.expose
def allCommands():
    speak("Welcome back Sir ,  How can I help you !")
    print("Welcome back Sir ,  How can I help you !")
    while True:  # Keep listening in a loop
        query = takecommand()
        
        if query == "exit":
            speak("Thanks for using me Sir , have a good day!")
            print("Thanks for using me Sir , have a good day!")
            eel.DisplayMessage("Thanks for using me Sir , have a good day!")
            eel.ShowHood()  # Return to main page
            break  # Exit the loop
        
        if query:  # Only process non-empty queries
            eel.senderText(query)
            try:
                if "open" in query:
                    from engine.features import opencommand
                    opencommand(query) 
                    
                elif "close" in query:
                    from engine.features import closecommand
                    closecommand(query) 
                       
                elif "on youtube" in query:
                    from engine.features import PlayYoutube
                    PlayYoutube(query)

                #Greetings

                elif "about you" in query:
                    speak("Hello sir , I am your Personnal voice assistant. My name is Bumblebee , How can I help you !")
                    print("Hello sir , I am your Personnal voice assistant. My name is Bumblebee , How can I help you !")
                    
                #jokes
                
                elif "say some joke" in query:
                        joke = pyjokes.get_joke()
                        speak(joke)
                        print(joke)
                        
                elif "roast me" in query:
                    from engine.features import get_roast
                    roast = get_roast()
                    speak(roast)       
                    print(roast) 
                    
                elif "say some pick up line" in query:
                    from engine.features import get_pickup_line
                    pickup = get_pickup_line()
                    speak(pickup)       
                    print(pickup)    
                    
                elif "motivate me" in query:
                    from engine.features import get_motivational_quote
                    motivation = get_motivational_quote()
                    speak(motivation)       
                    print(motivation)         
                        
                #news
                elif "say some news" in query:
                     speak("Please waiting sir, Fetching the latest news!")  
                     for i, article in enumerate(requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey=efed33514ec14b4a823ffb7783987bcd").json()["articles"][:3], 1):
                         print(f"{i}. {article['title']} ({article['source']['name']})")   
                         speak(f"{i}. {article['title']} ({article['source']['name']})")    
                        
                        
                #system off commands
                
                elif"shutdown the system" in query:
                    speak("System is going to Shutdown")
                    print("System is going to Shutdown")
                    os.system("shutdown /s /t 5")
                    
                elif"restart the system" in query:
                    speak("System is going to Restart")
                    print("System is going to Restart")
                    os.system("shutdown /r /t 5")    
                        
                elif"sleep the system" in query:
                    speak("System is going to Sleep")
                    print("System is going to Sleep")
                    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")          
                    
                #Time and Date
               
                elif "what's the time" in query:
                    now = datetime.now()
                    time_str = now.strftime("%H:%M:%S")
                    speak("The current time is " + time_str)    
                    print("The current time is " + time_str)
                    
                elif "what's the date" in query:
                    now = datetime.now()
                    date_str = now.strftime("%A, %B %d, %Y")
                    speak("Today's date is " + date_str)
                    print("Today's date is " + date_str)
            
                #whatsapp command
                
                elif "send message" in query or "phone call" in query or "video call" in query:
                    from engine.features import findContact, whatsApp
                    contact_no, name = findContact(query)
                    if contact_no != 0:
                        message = "message" if "send message" in query else "call" if "phone call" in query else "video call"
                        if message == "message":
                            speak("What message to send?")
                            query = takecommand()
                        whatsApp(contact_no, query, message, name)
                     
                        
                elif "hang up" in query:
                    speak("Call will be ended")
                    print("Call will be ended")
                    pyautogui.keyDown('alt')  # Hold Alt
                    pyautogui.press('f4')     # Press F4
                    pyautogui.keyUp('alt')    # Release Alt
                    pyautogui.press('enter')
                    speak("Call ended")        
                    print("Call ended") 
                    
                #mail commands
                elif "send email" in query :
                    from engine.features import email_flow
                    email_flow()     
                    
                elif "read email"  in query :
                    from engine.features import read_emails
                    read_emails()    
                    
                #Activate commands
                
                elif "activate whatsapp" in query:
                    os.system(f'start "" "whatsapp://"')
                    speak("Opening whatsapp")
                    print("Opening whatsapp")
                    
                    
                elif "clear files explorer" in query or "clear file explorer" in query:
                     pyautogui.keyDown('alt')
                     pyautogui.hotkey('f4')
                     pyautogui.keyUp('alt')
                     speak("Closing files explorer")  
                     print("Closing files explorer")  
                    
                
                #system commands
                
                elif "take screenshot" in query:
                    from engine.features import take_screenshot_with_custom_name
                    take_screenshot_with_custom_name()
                    
                elif "take the photo" in query:
                    speak("Prepare yourself , Photo will be taken in 3 seconds")
                    print("Prepare yourself , Photo will be taken in 3 seconds")
                    time.sleep(3)
                    pyautogui.press('space')
                    speak("Photo is taken")
                    print("Photo is taken")
                    
                elif "take the video" in query:
                    speak("Prepare yourself , Video will be taken in 3 seconds")
                    print("Prepare yourself , Video will be taken in 3 seconds")
                    pyautogui.press('up')
                    time.sleep(3)
                    pyautogui.press('space')
                    speak("video is taking")
                    print("video is taking")
                 
                elif "cut the video" in query:
                    speak("Video is going to be ended")
                    print("Video is going to be ended")
                    pyautogui.press('space')
                    speak("Video is ended")
                    print("Video is ended")
                    time.sleep(1)
                    pyautogui.press('down')
                    
                    
                elif "type" in query.lower():
                    text = query.lower().split("type", 1)[1].strip()
                    pyautogui.write(text + " ")


                elif "my ip address" in query:
                    try:
                    # Get public IP address
                       ip = requests.get('https://api.ipify.org').text
                       response = f"Your IP address is: {ip}"
                       speak(response)
                       print(response)
                    except Exception as e:
                       error_msg = "Sorry, I couldn't fetch the IP address"
                       speak(error_msg)
                       print(f"{error_msg}. Error: {e}")
                       
                       
                elif "check the battery" in query:
                    from engine.features import check_battery
                    check_battery()   
                    
                elif "check the internet speed" in query:
                    from engine.features import  run_speed_test
                    run_speed_test()
                    
                    
                elif "system volume up" in query:
                    from engine.features import set_volume
                    set_volume("increase")
                elif "system volume down" in query:
                    from engine.features import set_volume
                    set_volume("decrease")
                elif "system volume mute" in query or "system volume unmute" in query:
                    from engine.features import set_volume
                    set_volume("mute")   
                    
                elif "increase system brightness" in query or "brightness up" in query:
                    from engine.features import adjust_brightness
                    adjust_brightness(query)   
                elif "decrease system brightness" in query or "brightness down" in query:
                    from engine.features import adjust_brightness
                    adjust_brightness(query)   
                 
                 
                elif "minimise window" in query:
                    speak("Window minimized")
                    print("Window minimized")
                    from engine.features import minimize_window
                    minimize_window()
                elif "maximize window" in query:
                    speak("Window maximized")
                    print("Window maximized")
                    from engine.features import maximize_window
                    maximize_window()
                elif "toggle window" in query or "switch window" in query:
                    speak("Window toggled")
                    print("Window toggled")
                    from engine.features import toggle_window
                    toggle_window()
                    
                    
                elif "empty bin" in query or "empty recycle bin" in query:
                    winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=False)
                    speak("Recycle Bin emptied successfully")
                    print("Recycle Bin emptied successfully")   
                
                elif "system information" in query or"system info" in query:
                    from engine.features import get_basic_system_info
                    get_basic_system_info()    
                    
                elif "battery saver" in query:
                    from engine.features import enable_battery_saver_shortcut
                    enable_battery_saver_shortcut() 
                    
                elif "night light" in query or "nightlight" in query:
                    from engine.features import enable_night_light_shortcut
                    enable_night_light_shortcut()   
                
                elif"mobile hotspot" in query:
                    from engine.features import enable_hotspot_shortcut
                    enable_hotspot_shortcut() 
                    
                elif "bluetooth" in query:
                    from engine.features import enable_bluetooth_shortcut
                    enable_bluetooth_shortcut()   
                   
                elif "windows search" in query:
                    pyautogui.hotkey('win')             
                    
                
                #weather funtions
                
                elif "weather" in query:
                    from engine.features import get_weather
                    city = query.split("weather in")[-1].strip()
                    if city:
                        speak(f"Checking weather for {city}...")
                        get_weather(city)
                    else:
                        speak("Please specify a city.")
                   
                
               
                #youtube commands
                
                elif "play video" in query or "resume" in query:
                    pyautogui.press('space')
                    speak(" Video Played")
                    print(" Video Played")
    
                elif "pass video" in query or "pass" in query:
                    pyautogui.press('space')
                    speak(" Video Paused")
                    print(" Video Paused")
    
                elif "skip ad" in query:
                    for _ in range(4):  
                      pyautogui.press('tab')
                    pyautogui.press('enter')
                    speak(" Ad Skipped")
                    print(" Ad Skipped")
    
                elif "increase youtube volume" in query:
                    pyautogui.press('up')
                    speak(" Volume Increased")
                    print(" Volume Increased")
    
                elif "decrease youtube volume" in query:
                    pyautogui.press('down')
                    speak(" Volume Decreased")
                    print(" Volume Decreased")
    
                elif "fullscreen on" in query or "full screen on" in query or "fullscreen off" in query or "full screen off" in query:
                    pyautogui.press('f')
                    speak(" Fullscreen Toggled")
                    print("Fullscreen Toggled")
    
                elif "mute youtube" in query or "unmute youtube" in query:
                    pyautogui.press('m')
                    speak(" Mute Toggled")
                    print(" Mute Toggled")
    
                elif "next video" in query:
                    pyautogui.hotkey('shift', 'n')
                    speak(" Next Video")
                    print(" Next Video")
    
                elif "previous video" in query:
                    pyautogui.hotkey('shift', 'p')
                    speak(" Previous Video")
                    print(" Previous Video")
    
    
                #Translate command
                elif 'translate' in query:
                    from engine.features import translate_text
                    phrase = query.replace('translate', '').strip()
                    if not phrase:
                        speaks("Please say the phrase to translate after the word 'translate'.")
                        print("Please say the phrase to translate after the word 'translate'.")
                        continue

                    speaks("Which language should I translate to? For example, say Spanish, French, etc.")
                    print("Which language should I translate to? For example, say Spanish, French, etc.")
                    lang_command = takecommand()

                    if not lang_command:
                        speaks("I couldn't understand the language name.")
                        print("I couldn't understand the language name.")
                        continue

                     # Detect language code
                    target_code = None
                    for lang_name in lang_map:
                        if lang_name in lang_command:
                            target_code = lang_map[lang_name]
                            break

                    if not target_code:
                        speaks("Sorry, I couldn't recognize that language.")
                        print("Sorry, I couldn't recognize that language.")
                        continue

                    translation = translate_text(phrase, target_code)
                    if translation:
                        print(f"Original: {phrase}")
                        # For printing with proper encoding
                        sys.stdout.buffer.write(f"Translation ({target_code}): {translation}\n".encode('utf-8'))
                        speaks(f"The translation is: {translation}", lang=target_code)
                        print(f"The translation is: {translation}", lang=target_code)
                    else:
                        speaks("Sorry, translation failed.")
                        print("Sorry, translation failed.")
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                #edge commands
                
                elif query.startswith("information for"):
                    search_query = query.replace("information for", "").strip()  # Remove "search for" and extra spaces
                    if search_query:  # Check if there's an actual query
                          # Open Microsoft Edge with Bing search
                          edge_path = "C://Program Files (x86)//Microsoft//Edge//Application//msedge.exe"
                          webbrowser.register('edge', None, webbrowser.BackgroundBrowser(edge_path))
                          webbrowser.get('edge').open(f"https://en.wikipedia.org/wiki/Special:Search?search={search_query}")
                    else:
                          print("No search query detected after 'information for'.")
               
                
                
                elif query.startswith("search for"):
                    search_query = query.replace("search for", "").strip()  # Remove "search for" and extra spaces
                    if search_query:  # Check if there's an actual query
                          # Open Microsoft Edge with Bing search
                          edge_path = "C://Program Files (x86)//Microsoft//Edge//Application//msedge.exe"
                          webbrowser.register('edge', None, webbrowser.BackgroundBrowser(edge_path))
                          webbrowser.get('edge').open(f"https://www.bing.com/search?q={search_query}")
                    else:
                          print("No search query detected after 'search for'.")
                
                elif "enter" in query:
                    pyautogui.hotkey('enter')
                    speak("Pressing enter")
                    print("Pressing enter")
                
                elif "clear all tabs" in query:
                    pyautogui.hotkey('ctrl','shift','w')
                    speak("All tabs cleared")
                    print("All tabs cleared")
                
                elif "new tab" in query or "newtab" in query:
                    pyautogui.hotkey('ctrl', 't')
                    speak(" Opening new tab")
                    print(" Opening new tab")
                    
                elif "clear tab" in query or "cleartab" in query:
                    pyautogui.hotkey('ctrl', 'w')
                    speak(" Closing the tab")
                    print("Closing the tab")
                    
                elif "next tab" in query or "nexttab" in query:
                    pyautogui.hotkey('ctrl', 'tab')
                    speak(" Opening next tab")
                    print("Opening next tab")
                    
                elif "previous tab" in query:
                    pyautogui.hotkey('ctrl', 'shift', 'tab')
                    speak("Opening Previous tab")
                    print("Opening Previous tab")
                    
                elif "refresh" in query:
                    pyautogui.hotkey('f5')
                    speak("Refresh page")
                    print("Refresh page")    
                    
                elif "go back" in query or "goback " in query:
                    pyautogui.hotkey('alt', 'left')
                    speak(" Going back")
                    print("Going back")
                    
                elif "go forward" in query or " goforward" in query:
                    pyautogui.hotkey('alt', 'right')
                    speak(" Going forward")
                    print("Going forward")   
                    
                elif "zoom in" in query or " zoomin" in query:
                    pyautogui.hotkey('ctrl', '+')
                    speak("Zooming in")
                    print("Zooming in")   
                    
                elif "zoom out" in query or " zoomout" in query:
                    pyautogui.hotkey('ctrl', '-')
                    speak(" Zooming out")
                    print("Zooming out")   
                    
                elif "reset zoom" in query or " resetzoom" in query:
                    pyautogui.hotkey('ctrl', '0')
                    speak(" Reset Zoom")
                    print("Reset Zoom")   
                    
                elif "browser history" in query or " history" in query:
                    pyautogui.hotkey('ctrl', 'h')
                    speak(" Opening history")
                    print("Opening history")   
                    
                elif "browser download" in query or " downloads" in query:
                    pyautogui.hotkey('ctrl', 'j')
                    speak(" Opening downloads")
                    print("Opening downloads")   
                    
                elif "new window" in query or " newwindow" in query:
                    pyautogui.hotkey('ctrl', 'n')
                    speak(" Opening new window")
                    print(" Opening new window")  
                    
                elif "clear window" in query or " clearwindow" in query:
                    pyautogui.hotkey('ctrl', 'shift','w')
                    speak(" Closing the window")
                    print(" Closing the window")       
                    
                elif "homepage" in query or "home page" in query:
                    pyautogui.keyDown('alt')
                    pyautogui.hotkey('home')
                    pyautogui.keyUp('alt')
                    speak("Opening the home page")
                    print("Opening the home page")

                    
                elif "incognito window" in query or " incognito" in query:
                    pyautogui.hotkey('ctrl', 'shift', 'n')
                    speak(" Opening incognito window")
                    print("Opening incognito window")   
                    
                elif "scroll up" in query or " scrollup" in query:
                    pyautogui.scroll(300)
                    speak(" Scrolling up")
                    print("Scrolling up")   
                    
                elif "scroll down" in query or " scrolldown" in query:
                    pyautogui.scroll(-300)
                    speak(" Scrolling down")
                    print("Scrolling down")   
                    
                elif "page top" in query or " pagetop" in query:
                    pyautogui.hotkey('home')
                    speak(" Going page top")
                    print("Going page top")   
                    
                elif "page bottom" in query or " pagebottom" in query:
                    pyautogui.hotkey('end')
                    speak(" Going page bottom")
                    print("Going page bottom")   
                    
                    
                elif "searchbox" in query or "search box" in query:
                    pyautogui.keyDown('ctrl')  
                    pyautogui.hotkey('k')
                    pyautogui.keyUp('ctrl')  
                    speak("Opening search box")
                    print("Opening Search box")
                    
                elif "full tab" in query or "normal tab" in query:
                    pyautogui.hotkey('f11')
                    speak("task performed")
                    print("task performed")    
                
    
        
                     

                
                
                    
                #calculations
                                 
                elif "calculate" in query:
                    from engine.features import chatBots
                    chatBots(query)     
                    
                    
                                                                                           
                                                                        
                
                elif "tell me " in query:
                    from engine.features import chatBot
                    chatBot(query)
                 
                else:
                    speak("Say the command again , Please!")
                    print("Say the command again , Please!")    
            
            except Exception as e:
                print("Error:", e)
    
    # When "quit" is detected, we exit the function and go back to ShowHood

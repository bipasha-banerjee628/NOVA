import os
import re
from shlex import quote
import struct
import subprocess
import time
import webbrowser
import eel
import pvporcupine
import pyaudio
import pyautogui
import pywhatkit as kit
import pygame
from backend.command import speak
from backend.config import ASSISTANT_NAME
import sqlite3

from backend.helper import extract_yt_term, remove_words
from hugchat import hugchat

ACCESS_KEY = "LK7AcLSSMsAAJVE6H4I/O2JkKXRaea50vk8F61o5KIrFfYoIA1wNRA=="
# ACCESS_KEY = "Q5U9RtRRCWjnO1dys0dKxCEPVedmjzBBPqJ7JEFTHr7RRXfWew735Q=="
# ACCESS_KEY = "MK5O6xFscJpURuV7ud48/HFHbiPxMYpP0pbbC3sMBLt93G8Ct9DUGA=="

conn = sqlite3.connect("nova.db")
cursor = conn.cursor()


pygame.mixer.init()


@eel.expose
def playAssistantSound():
   
   sound_file = r"C:\Users\bbipa\Documents\webdev\personal_ai_assistant\NOVA\frontend\assests\audio\start_sound.mp3"
   pygame.mixer.music.load(sound_file)
   pygame.mixer.music.play()


def openCommand(query):
   query= query.replace(ASSISTANT_NAME,"")
   query= query.replace("open","")
   query.lower()
  
   app_name = query.strip()
   if app_name != "":
      try:
            cursor.execute( 
                'SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Opening "+query)
                os.startfile(results[0][0])

            elif len(results) == 0: 
                cursor.execute(
                'SELECT url FROM web_command WHERE name IN (?)', (app_name,))
                results = cursor.fetchall()
                
                if len(results) != 0:
                    speak("Opening "+query)
                    webbrowser.open(results[0][0])

                else:
                    speak("Opening "+query)
                    try:
                        os.system('start '+query)
                    except:
                        speak("not found")
      except:
          speak("some thing went wrong")

   # if query!="":
   #    speak("Opening "+query)
   #    os.system('start '+query)
   # else:
   #    speak("I am not sure what you want to open")


def PlayYoutube(query):
   search_term = extract_yt_term(query)
   speak("Playing "+search_term+" on youtube")
   kit.playonyt(search_term)



# def hotword():
#     porcupine=None
#     paud=None
#     audio_stream=None
#     try:
       
#         # pre trained keywords    
#         porcupine=pvporcupine.create(keywords=["nova","nexas"]) 
#         paud=pyaudio.PyAudio()
#         audio_stream=paud.open(rate=porcupine.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=porcupine.frame_length)
        
#         # loop for streaming
#         while True:
#             keyword=audio_stream.read(porcupine.frame_length)
#             keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)

#             # processing keyword comes from mic 
#             keyword_index=porcupine.process(keyword)

#             # checking first keyword detetcted for not
#             if keyword_index>=0:
#                 print("hotword detected")

#                 # pressing shorcut key win+j
#                 import pyautogui as autogui
#                 autogui.keyDown("win")
#                 autogui.press("j")
#                 time.sleep(2)
#                 autogui.keyUp("win")
                
#     except:
#         if porcupine is not None:
#             porcupine.delete()
#         if audio_stream is not None:
#             audio_stream.close()
#         if paud is not None:
#             paud.terminate()

def hotword():
    porcupine = None
    paud = None
    audio_stream = None

    try:
        # Path to your custom keyword file
        keyword_path = os.path.join("keywords", "hey-nova.ppn")
        # keyword_path = os.path.join("keywords", "Hey-nexus.ppn")
        print("Loading keyword file:", keyword_path)

        # Check if file exists
        if not os.path.exists(keyword_path):
            raise FileNotFoundError(f"Keyword file not found at: {keyword_path}")

        # Create porcupine instance with the custom keyword and the access key
        porcupine = pvporcupine.create(
            access_key=ACCESS_KEY,  # Add your access key here
            keyword_paths=[keyword_path]
        )

        # Set up audio stream without 'exception_on_overflow'
        paud = pyaudio.PyAudio()
        audio_stream = paud.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length
        )

        print("Listening for hotword...")

        # Stream loop
        while True:
            pcm = audio_stream.read(porcupine.frame_length)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

            result = porcupine.process(pcm)

            if result >= 0:
                print("Hotword detected!")

                # Press Windows + J as the trigger action
                pyautogui.keyDown("win")
                pyautogui.press("j")
                time.sleep(2)
                pyautogui.keyUp("win")

    except Exception as e:
        print("Error:", e)

    finally:
        # Clean up
        if porcupine:
            porcupine.delete()
        if audio_stream:
            audio_stream.close()
        if paud:
            paud.terminate()
            
def findContact(query):
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'whatsapp', 'video','vista']
    query = remove_words(query, words_to_remove)

    try:
        query = query.strip().lower()
        cursor.execute("SELECT Phone FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", 
                       ('%' + query + '%', query + '%'))
        results = cursor.fetchall()

        if not results:
            raise Exception("Contact not found")

        mobile_number_str = str(results[0][0])
        if not mobile_number_str.startswith('+91'):
            mobile_number_str = '+91' + mobile_number_str

        return mobile_number_str, query
    except Exception as e:
        speak('Contact does not exist in saved contacts.')
        print(f"[ERROR] {e}")
        return 0, 0





def whatsApp(Phone, message, flag, name):
    encoded_message = quote(message) if message else ''
    whatsapp_url = f"whatsapp://send?phone={Phone}&text={encoded_message}"
    full_command = f'start "" "{whatsapp_url}"'

    # Open WhatsApp chat
    subprocess.run(full_command, shell=True)
    time.sleep(6)  # Let it load

    # Focus on chat with Ctrl+F and Tab through UI
    pyautogui.hotkey('ctrl', 'f')
    time.sleep(1)

    if flag == 'message':
        # Tab 12 times to reach message input field
        for _ in range(12):
            pyautogui.press('tab')
            time.sleep(0.1)
        pyautogui.press('enter')  # Focus message box
        pyautogui.write(message)
        pyautogui.press('enter')
        speak(f"Message sent successfully to {name}")

    elif flag == 'call':
        # Tab 6 times to reach voice call button
        for _ in range(6):
            pyautogui.press('tab')
            time.sleep(0.1)
        pyautogui.press('enter')
        speak(f"Calling {name}")

    elif flag == 'vista':
        # Tab 5 times to reach video call button
        for _ in range(5):
            pyautogui.press('tab')
            time.sleep(0.1)
        pyautogui.press('enter')
        speak(f"Starting video call with {name}")

    else:
        speak("Unknown action requested.")

# chat bot

# def chatBot(query):
#     user_input = query.lower()
#     chatbot = hugchat.ChatBot(cookie_path="backend\cookies.json")
#     id = chatbot.new_conversation()
#     chatbot.change_conversation(id)
#     response = chatbot.chat(user_input)
#     print(response)
#     speak(response)
#     return response






def chatBot(query):
    user_input = query.lower()
    chatbot = hugchat.ChatBot(cookie_path="backend\\cookies.json")
    conversation_id = chatbot.new_conversation()
    chatbot.change_conversation(conversation_id)
    
    # Custom system prompt to set the assistant's identity as NOVA
    system_prompt = (
        "You are NOVA, a smart and friendly AI assistant created by Bipasha Banerjee. "
        "You always refer to yourself as NOVA, never as LLaMA or anything else. "
        "You are always helpful, friendly, and never mention Meta or Hugging Face. "
        "Your job is to assist the user and answer their questions. "
    )
    chatbot.chat(system_prompt)
    
    # Check for specific commands and provide responses accordingly
    if "introduce yourself" in user_input or "who are you" in user_input:
        # Override the response to force NOVA to introduce itself correctly
        response = "Hello! My name is NOVA, and I am your friendly AI assistant."
    elif "who made you" in user_input or "who invented you" in user_input:
        # Provide the correct response for who created NOVA
        response = "I was created by Bipasha Banerjee. She is my master and the brilliant mind behind my existence"
    else:
        # Process the user input and get a response from the chatbot
        response = chatbot.chat(user_input)
    
    print(response)
    speak(response)  # Assuming you have a speak function to read the response out loud
    
    return response

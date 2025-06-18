import time
import pyttsx3
import speech_recognition as sr
import eel


def speak(text):
    text = str(text)
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    # print(voices)
    engine.setProperty('voice', voices[1].id)
    eel.DisplayMessage(text)
    engine.say(text)
    engine.runAndWait()
    engine.setProperty('rate', 174)
    eel.receiverText(text)
    


# speek("Hello , I am NOVA. How can I help you today?")

# @eel.expose
def takecommand():
    r= sr.Recognizer()
    with sr.Microphone() as source:
        print("I am listening...")
        eel.DisplayMessage("I am listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source,10,8)
  

    try:
        print("Recognizing...")
        eel.DisplayMessage("Recognizing...")
        query = r.recognize_google(audio, language='en-US')
        print(f"User said: {query}\n")
        eel.DisplayMessage(query)
        eel.senderText(query)


        
        # time.sleep(3)
        # speak(query)
    except Exception as e:
        print(f"Error:{str(e)}\n")
        return None
    
    return query.lower()



@eel.expose
def takeAllCommands(message=None):
    
    if message is None:
        query = takecommand()
        if not query:
            return
        print(query)
        eel.senderText(query)
    else:
        query = message
        print(f"Message recieved: {query}")
        eel.senderText(query)
    try:
     if query:
         
        if "open" in query:
            from backend.feature import openCommand
            openCommand(query)
        
        
        
        elif "send message" in query or "call" in query or "vista" in query:
            from backend.feature import findContact, whatsApp
            flag = ""
            Phone, name = findContact(query)
            if Phone != 0:
                if "send message" in query:
                    flag = 'message'
                    speak("What message to send?")
                    query = takecommand()  # Ask for the message text
                elif "call" in query:
                    flag = 'call'
                else:
                    flag = 'vista'
                whatsApp(Phone, query, flag, name)
        elif "on youtube" :
            from backend.feature import PlayYoutube
            PlayYoutube(query)

        else:
            print("i am not sure what to do")

    except:
        from backend.feature import chatBot
        chatBot(query)

    eel.ShowHood()


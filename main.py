import os
import eel
from backend.feature import *
from backend.command import *
from backend.auth import recoganize


def start():
    eel.init("frontend")
    
    playAssistantSound()

    @eel.expose
    def init():
        eel.hideLoader()
        speak("Get ready for face authentication")
        flag = recoganize.AuthenticateFace()
        if flag == 1:
            eel.hideFaceAuth()
            speak("Face authentication successful")
            eel.hideFaceAuthSuccess()
            speak("Hello mam, I am your assistant")
            eel.hideStart()
            playAssistantSound()
            
        else:
            speak("Face authentication failed")
    

    

    os.system('start msedge.exe --app="http://127.0.0.1:8000/index.html"')
    eel.start("index.html", mode=None, host="localhost", port=8000, block=True)


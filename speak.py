import pyttsx3
import threading

def Speak(command):
    engine = pyttsx3.init('sapi5') 
    voices = engine.getProperty('voices')
    engine.setProperty('volume',1)
    engine.setProperty('rate',150)
    engine.setProperty('voice',voices[2].id)
    engine.say(command) 
    engine.runAndWait()

def Speak_thread(command):
    x = threading.Thread(target=Speak, args=(command,))
    x.start()


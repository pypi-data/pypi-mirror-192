import kenu_ai as kenu
from gtts import gTTS
import random
import os
from playsound import playsound
import speech_recognition as sr
import tkinter as tk

rec = sr.Recognizer()

def record():   
    print("Dinliyorum.")
    try:
        with sr.Microphone() as source:
            rec.adjust_for_ambient_noise(source,1)
            voice_rec = ''
            audio = rec.listen(source)
            voice_rec = rec.recognize_vosk(audio,language='tr-TR')
    except sr.UnknownValueError:
        speak('Anlayamadım,lütfen tekrarlayın!')
    except sr.RequestError:
        speak('Dahili hata meydana geldi. Lütfen tekrar deneyin!')
    if(voice_rec != ''):
        return voice_rec
    else:
        record()

def speak(text):
    tts = gTTS(text, lang = 'tr')
    rand = random.randint(1,10000)
    file = 'voice' + str(rand) + '.mp3'
    tts.save(file)
    playsound(file)
    os.remove(file)

while True:
    try:
        yazi = kenu.chat(record())
        speak(yazi)
    except sr.WaitTimeoutError:
        pass
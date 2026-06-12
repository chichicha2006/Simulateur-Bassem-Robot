# -*- coding: utf-8 -*-

import pyttsx3

#pour pas afficher le texte de pygame en console
import warnings

warnings.filterwarnings(
    "ignore",
    message="pkg_resources is deprecated as an API"
)
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame

import time
import threading
import socket
import getpass

engine = pyttsx3.init()
engine.setProperty("rate", 200)
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)


import speech_recognition as sr

recognizer = sr.Recognizer()

def wav_to_text(audio_path):
    """Transforme un fichier WAV en texte."""
    try:
        with sr.AudioFile(audio_path) as source:
            audio = recognizer.record(source)

        texte = recognizer.recognize_google(audio, language="fr-FR")
        print("Texte reconnu depuis WAV :", texte)
        return texte.lower().strip()

    except sr.UnknownValueError:
        print("Audio incompris")
        return None

    except sr.RequestError as e:
        print("Erreur service speech_recognition :", e)
        return None


def reagir_au_wav(audio_path):
    """Fonction appelée par server.py quand Unity envoie un fichier WAV."""
    texte = wav_to_text(audio_path)

    if texte:
        reagir_au_texte(texte)
    else:
        parler("Je n'ai pas compris.")
#-----------------------------------------------------------------------
# je reprend bassem_son et j'ajoute des print apres parler() dans chaque fonction pour pouvoir tester



def parler(text):
    print("BASSEM :", text)
    engine.say(text)
    engine.runAndWait()

 
def allo():
        parler("Oué, c'est greg?")
        
def musique(a):
    def play():
        pygame.mixer.init()
        pygame.mixer.music.load(a)
        pygame.mixer.music.play()
        print(f"Lecture de {a} en cours...")
    parler("Pas de soucis, écoute ça")
    threading.Thread(target=play).start()

def stop():
    if pygame.mixer.get_init():
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
    else:
        print("Aucune musique en cours.")

def volume(val):
    if pygame.mixer.get_init():
        pygame.mixer.music.set_volume(val)
        parler(f"Volume réglé à {int(val * 100)} %")
    else:
        print("La musique n'est pas encore lancée.")


def juke():
    global etat_juke
    parler("Veux-tu écouter de la musique ?")
    etat_juke = 1
        

def get_ip():
    try:
        # Crée une connexion fictive pour obtenir l’IP locale
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # on ne contacte pas vraiment Google
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return ""
        
def mots_interdits(a):
    vulgaire=["enculé", "enculer", "pute","connard","merde","test contrôle"]
    wesh = ["wesh", "wech"]
    for element in vulgaire:
        if a in element :
            
            avertissement = "❌ grossier personnage. j'ai ton adresse I P ("+get_ip()+"), le login de ton compte utilisateur ("+getpass.getuser()+") et la machine où tu te trouve ("+socket.gethostname()+") . J'envoie tes identifiants et le message que tu as essayé de me faire dire aux services concernés." 
            parler(avertissement)
            return True
        elif a in wesh:
            parler("on ne dit pas wesh dans une salle de classe")
            return True
    return False

etat_juke = 0
def reagir_au_texte(texte):
    """
    Fonction appelée par server.py à chaque audio reçu depuis unity puis traduit en texte par reagir_au_wav.
    Elle garde la logique de bassem_son.
    """
    if mots_interdits(texte):
        return
    
    global etat_juke

    texte = texte.lower().strip()

    if etat_juke == 1:
        if "oui" in texte or "yes" in texte:
            parler("Quel genre souhaites-tu écouter ? J'ai du romantique, de la pop, du jazz fusion, du rock.")
            etat_juke = 2
            return
        else:
            parler("pas de musique alors")
            etat_juke = 0
            return

    if etat_juke == 2:
        if "romantique" in texte:
            musique("son/rizz.mp3")
        elif "pop" in texte:
            musique("son/pop.mp3")
        elif "jazz" in texte:
            musique("son/jazz_fusion.mp3")
        elif "rock" in texte:
            musique("son/lotta.mp3")
        else:
            parler("Je n'ai pas compris le genre de musique.")

        etat_juke = 0
        return

    if "allô bassem" in texte or "bassem" in texte:
        allo()

    elif "musique" in texte:
        juke()

    elif "stop" in texte or "arrête" in texte:
        stop()
        parler("Ok, j'arrête.")

    #elif "test contrôle" in texte:
     #   avertissement = "❌ grossier personnage. j'ai ton adresse I P ("+get_ip()+"), le login de ton compte utilisateur ("+getpass.getuser()+") et la machine où tu te trouve ("+socket.gethostname()+") . J'envoie tes identifiants et le message que tu as essayé de me faire dire aux services concernés."
     #   parler(avertissement)
    
    else:
        parler("Je n'ai pas compris.")













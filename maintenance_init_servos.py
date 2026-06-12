# -*- coding: utf-8 -*-
"""
  ____           _____ _____ ______ __  __ 
 |  _ \   /\    / ____/ ____|  ____|  \/  |
 | |_) | /  \  | (___| (___ | |__  | \  / |
 |  _ < / /\ \  \___ \\___ \|  __| | |\/| |
 | |_) / ____ \ ____) |___) | |____| |  | |
 |____/_/    \_\_____/_____/|______|_|  |_|
 maintenance_init_servos
@author: TNSI 2024 2025 : Ethan, Amina, Lucas (et un peu le prof)

interface graphique : graph()

"""

#from dynamixel_sdk import * 
import time
import tkinter as tk
import sys
import io
import builtins
import json


pm=[0,0,0,0,0,0]
current_angles = {"servo_1": 0, "servo_2": 0, "servo_3": 0, "servo_4": 0, "servo_5": 0, "servo_6": 0}
global tork_on, tork_off, compteur_erreur_saisie
tork_on=True
compteur_erreur_saisie=0

# IDs des servos 
DXL_IDS = [1, 2, 3, 4, 5, 6]  #  1,2 MX-64 / 3,4,5,6 AX-12A

# Adresses 
ADDR_TORQUE_ENABLE     = 24
ADDR_GOAL_POSITION     = 30
ADDR_PRESENT_POSITION  = 36
ADDR_MOVING_SPEED      = 32
ADDR_CW_ANGLE_LIMIT    = 6
ADDR_CCW_ANGLE_LIMIT   = 8

# Punch à appliquer (entre 0 et 1023)
AX12_PUNCH = 20
MX64_PUNCH = 30

# ADRESSES MEMOIRE PUNCH
# AX-12A
ADDR_AX_PUNCH_L = 48
ADDR_AX_PUNCH_H = 49
# MX-64
ADDR_MX_PUNCH_L = 48
ADDR_MX_PUNCH_H = 49


TORQUE_ENABLE  = 1
TORQUE_DISABLE = 0

RATIO_MX64 = 4096/360
RATIO_AX12 = 1024/300


# Limites des positions 
LIMITS = {
    1: (0, 1902),
    2: (298, 1956),
    3: (510, 961),
    4: (0, 1023),
    5: (200,800),
    6: (348,652)
}

LIMITS_angles = {
    1: (-18, 150),
    2: (0, 145),
    3: (0, 132),
    4: (-145, 145),
    5: (-88,88),
    6: (-40,40)
}

# Vitesse par servo 
SPEEDS = {
    1: 120,
    2: 120,
    3: 100,
    4: 200,
    5: 150,
    6: 80
}

# id des articulations
epaule1=1
epaule2=2
coude=3
poignet=4
cououi=5
counon=6

"""
def print(*args, **kwargs):
    builtins.print("\033[42m", end="")   
    builtins.print(*args, **kwargs)
    builtins.print("\033[0m", end="")    # reset
"""
def ouvrir_port():
    def print(*args, **kwargs):
        builtins.print("\033[42m", end="")   
        builtins.print(*args, **kwargs)
        builtins.print("\033[0m", end="")    # reset
    print("  ✔ Servos : Port série ouvert et baudrate réglé.")

def pon():
    def print(*args, **kwargs):
        builtins.print("\033[42m", end="")   
        builtins.print(*args, **kwargs)
        builtins.print("\033[0m", end="")    # reset
    print("  ✔ Servos : Port série ouvert et baudrate réglé.")

        
def fermer_port():
    """ ferme le port COM (fait doublon avec poff() )"""
    def print(*args, **kwargs):
        builtins.print("\033[42m", end="")   
        builtins.print(*args, **kwargs)
        builtins.print("\033[0m", end="")    # reset
    print("  ✘ Servos : Port série fermé")
    
def poff():
    """ ferme le port COM"""
    poff=True
    def print(*args, **kwargs):
        builtins.print("\033[42m", end="")   
        builtins.print(*args, **kwargs)
        builtins.print("\033[0m", end="")    # reset
    print("  ✘ Servos : Port série fermé")
    
def pof():
    """ ferme les ports COM"""
    def print(*args, **kwargs):
        builtins.print("\033[42m", end="")   
        builtins.print(*args, **kwargs)
        builtins.print("\033[0m", end="")    # reset
    print("  ✘ Ports COM servo et yeux fermés")
    
def toff():
    global tork_off, tork_on
    tork_off=True
    tork_on=False
    def print(*args, **kwargs):
        builtins.print("\033[42m", end="")   
        builtins.print(*args, **kwargs)
        builtins.print("\033[0m", end="")    # reset
    print("  ✘ torques desactivés")
    
def ton():
    """active les torques"""
    global tork_off, tork_on
    tork_off=False
    tork_on=True
    def print(*args, **kwargs):
        builtins.print("\033[42m", end="")   
        builtins.print(*args, **kwargs)
        builtins.print("\033[0m", end="")    # reset
    print("  ✔ torques activés")
    
def lecturepos():
    """ renvoie une liste contenant respectivement la position des servos d'id 1,2,3,4,5 et 6"""
    return pm

def lire_position(id):
    """lire_position(id) : renvoie en pas la position du servo d’id id"""
    return pm

def affiche_pos(id):
    """affiche_pos(id) : affiche en pas la position du servo d’id id"""
    def print(*args, **kwargs):
        builtins.print("\033[42m", end="")   
        builtins.print(*args, **kwargs)
        builtins.print("\033[0m", end="")    # reset
    print( pm[id-1])
        
def config():    
    """configuration de base (vitesses, limites,punch, active les torques)"""
    
    def print(*args, **kwargs):
        builtins.print("\033[42m", end="")   
        builtins.print(*args, **kwargs)
        builtins.print("\033[0m", end="")    # reset
    print("  Initialisation en cours")
    time.sleep(0.2)
    print("")
    print("  Initialisation effectuée (vitesses, limites,punchs,torques)")
    ton()
    #print("  ✔ Torques activés")
    #print("  →  positions des servos 1 à 6 : ", pm)
    #print("     - - - - ")
    init_servos_lecturepos()
    time.sleep(0.2)

def init():
    #time.sleep(0.5)
    config()
    bouge(0,0,0,0,0,0) 
    lecture()
    print("  Tout semble en place - pret à recevoir des ordres")
    print("  👍 ")
    

def fixer_limites(id, min_angle, max_angle):
    def print(*args, **kwargs):
        builtins.print("\033[42m", end="")   
        builtins.print(*args, **kwargs)
        builtins.print("\033[0m", end="")    # reset
    
    print("  ⚠️ pas possible de fixer les limites en mode maintenance ⚠️")
    
def set_punch(dxl_id, punch, addr_l):
    def print(*args, **kwargs):
        builtins.print("\033[42m", end="")   
        builtins.print(*args, **kwargs)
        builtins.print("\033[0m", end="")    # reset
    print("  ✔  servos : punch reglé pour servo ", dxl_id)
        
def set_punch_all():
    def print(*args, **kwargs):
        builtins.print("\033[42m", end="")   
        builtins.print(*args, **kwargs)
        builtins.print("\033[0m", end="")    # reset
    print("  ✔  servos : punch reglé pour les servos ")

def lecturepos():
    """ renvoie une liste contenant respectivement la position des servos d'id 1,2,3,4,5 et 6"""
    l = []
    return pm

def lecture_angles():
    """ renvoie une liste contenant respectivement la position en degrés des servos d'id 1,2,3,4,5 et 6"""
    la = pm[:]
    la[0] = (LIMITS[1][1]-(RATIO_MX64*18)-la[0])//(RATIO_MX64) +1
    la[1] = (LIMITS[2][1] - la[1] )//RATIO_MX64
    la[2]  = -(LIMITS[3][0] - la[2]) //RATIO_AX12
    la[3]  = (la[3]-512)//RATIO_AX12
    la[4] = (la[4]-((LIMITS[5][0]+LIMITS[5][1])//2) )    // RATIO_AX12
    la[5] = (la[5]-( (LIMITS[6][0]+LIMITS[6][1])//2 ) ) // RATIO_AX12
    print("  position des servos : ")
    #print("\033[34m\033[43mTexte bleu sur fond jaune\033[0m")
    print_table(la)
    return la

#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
def mmlecture():
    if tork_on:
        lecture()
    else:
        mlecture()
        
def verif_limite(la2):
    la3 = pm[:]


def lecture():
    """ renvoie une liste contenant respectivement la position en degrés des servos d'id 1,2,3,4,5 et 6"""
    la = pm[:]
    la[0] = (LIMITS[1][1]-(RATIO_MX64*18)-la[0])//(RATIO_MX64) +1
    la[1] = (LIMITS[2][1] - la[1] )//RATIO_MX64
    la[2]  = -(LIMITS[3][0] - la[2]) //RATIO_AX12
    la[3]  = (la[3]-512)//RATIO_AX12
    la[4] = (la[4]-((LIMITS[5][0]+LIMITS[5][1])//2) )    // RATIO_AX12 
    la[5] = (la[5]-( (LIMITS[6][0]+LIMITS[6][1])//2 ) ) // RATIO_AX12
    print("  position des servos : ")
    #print("\033[34m\033[43mTexte bleu sur fond jaune\033[0m")
    print_table(la)
    return la

import re # pour ne garder que les chiffres d'une chaine de caracteres

def mlecture():
    YELLOW = "\033[33m"
    RESET = "\033[0m"
    print()
    print(f"{YELLOW}----- SIMULATION DE MOUVEMENT MANUEL DU BRAS  -------{RESET}")
    print("On va entrer à la main les valeurs de position pour les servos:")
    print()
    la2 = []
    for i in range (6):
        st = "   Quelle position pour servo "+ str(i+1)+" ? : "
        s=int(input(st))
        limite_min = int(re.sub(r"[^0-9-]", "", data[i]["Angle min"]) )
        limite_max = int(re.sub(r"[^0-9-]", "", data[i]["Angle max"]) )
        if s < limite_min or s > limite_max :
            hors_limite()
            print("  ❌ La saisie des valeurs est annulée")
            print("  💡 Referez-vous au document guide des angles pour connaître les limites")
            print()
            return [0,0,0,0,0,0]             
        else:
            la2.append(s)
    
    #print ("vous avez saisi : ", la2)
    return la2
#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&       
       

################## PRINT TABLE #####################

def print_table(tab, color="green"):
    """
    Affiche un tableau avec :
    - Colonnes numériques encadrées avec traits colorés
    - Dernière colonne texte alignée à gauche, non encadrée
    - Tous les traits (| et +) colorés
    """
    def print(*args, **kwargs):
        builtins.print("\033[42m", end="")   
        builtins.print(*args, **kwargs)
        builtins.print("\033[0m", end="")    # reset
    # Codes ANSI pour les couleurs
    COLORS = {
        "black": "\033[30m",
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "white": "\033[37m",
    }
    RESET = "\033[0m"
    COLOR = COLORS.get(color.lower(), "\033[32m")

    n = len(tab)

    # Largeur des colonnes
    num_col_w = max(4, max(len(str(int(v))) for v in tab))
    last_col_w = max(len("id servo"), len("angle (degrés)")) + 2

    # Ligne horizontale pour colonnes numériques
    def line():
        print(
            COLOR
            + "+" + "+".join("-" * num_col_w for _ in range(n)) + "+"
            + RESET
        )

    # Affichage du tableau
    line()
    # Ligne des en-têtes
    print(
        COLOR + "|" + RESET
        + (COLOR + "|" + RESET).join(f"{i:^{num_col_w}}" for i in range(1, n + 1))
        + COLOR + "|" + RESET
        + f"{'id servo':<{last_col_w}}"  # aligné à gauche
    )
    line()
    # Ligne des valeurs
    print(
        COLOR + "|" + RESET
        + (COLOR + "|" + RESET).join(f"{int(v):^{num_col_w}}" for v in tab)
        + COLOR + "|" + RESET
        + f"{'angle (degrés)':<{last_col_w}}"  # aligné à gauche
    )
    line()   
    

data = [
    {"articulation":"Epaule", "Id servo":"1", "Angle min":"-18°", "Angle max":"+150°", "commentaire":"0° = le long du torse"},
    {"articulation":"Epaule", "Id servo":"2", "Angle min":"0°", "Angle max":"+145°", "commentaire":"0° = le long du torse"},
    {"articulation":"Coude", "Id servo":"3", "Angle min":"0°", "Angle max":"+132°", "commentaire":"0° = le long du torse"},
    {"articulation":"poignet", "Id servo":"4", "Angle min":"-145 (ccw)", "Angle max":"+145 (cw)", "commentaire":""},
    {"articulation":"Cou non", "Id servo":"5", "Angle min":"-88° (R)", "Angle max":"+88° (L)", "commentaire":"0° = tète droite"},
    {"articulation":"Cou oui", "Id servo":"6", "Angle min":"-40° (pied)", "Angle max":"40°(ciel)", "commentaire":"0° = tète droite"},
]

data2 = [
    {"articulation":"Epaule", "Id servo":"1", "Pos min":"1894 (-18°)", "Pos max":"0 (150°)", "commentaire":"0° = le long du torse"},
    {"articulation":"Epaule", "Id servo":"2", "Pos min":"1955 (0°)", "Pos max":"317 (145°)", "commentaire":"0° = le long du torse"},
    {"articulation":"Coude", "Id servo":"3", "Pos min":"511", "Pos max":"961", "commentaire":"0° = le long du torse"},
    {"articulation":"poignet", "Id servo":"4", "Pos min":"0", "Pos max":"1023", "commentaire":""},
    {"articulation":"Cou non", "Id servo":"5", "Pos min":"200 (R)", "Pos max":"800 (L)", "commentaire":"0° = tète droite"},
    {"articulation":"Cou oui", "Id servo":"6", "Pos min":"350 (pied)", "Pos max":"650 (ciel)", "commentaire":"0° = tète droite"},
]
def print_table2(data):
    """
    Affiche un tableau à partir d'une liste de dictionnaires.
    Compatible avec n'importe quelles colonnes.
    """
    if not data:
        print("Aucune donnée à afficher")
        return

    # Colonnes du tableau = toutes les clés du premier dictionnaire
    columns = list(data[0].keys())

    # Largeur de chaque colonne
    col_widths = {col: max(len(col), *(len(str(row[col])) for row in data)) for col in columns}

    # Ligne horizontale
    def line():
        print("+" + "+".join("-" * (col_widths[col]+2) for col in columns) + "+")

    # Affichage du tableau
    line()
    # En-têtes
    print("| " + " | ".join(f"{col:<{col_widths[col]}}" for col in columns) + " |")
    line()
    # Lignes de données
    for row in data:
        print("| " + " | ".join(f"{row[col]:<{col_widths[col]}}" for col in columns) + " |")
    line()

    #print(pm[id-1])
    return pm[id-1]

def affiche_pos(id):
    """affiche_pos(id) : affiche en pas la position du servo d’id id"""
    def print(*args, **kwargs):
        builtins.print("\033[42m", end="")   
        builtins.print(*args, **kwargs)
        builtins.print("\033[0m", end="")    # reset
    print( "position (en pas) du servo ",id, " : ", pm[id-1])
    
def init_servos_lecturepos():    
    """ renvoie une liste contenant respectivement la position des servos d'id 1,2,3 et 4"""
    #print(pm[0:4])
    return pm[0:4]

def posinit():
    """ positionne le bras le long du corps"""
    print("  🤖 le robot positionne son bras le long du corps et sa tête droite")
    time.sleep(1.5)
    pos=[1700,1950,512,512,500,500]
    for i in range(6):
        pm[i]=pos[i]
    #tete_posinit()
    #lecture_angles()

def tete_posinit():
    """ positionne la tête droite"""
    print("  🤖 le robot positionne sa tête droite")
    bouge5(0)
    bouge6(0)
    #lecture_angles()
    
## ======================================================================

def hors_limite(id=None):
    if not id:
        print("  ❗ \033[41m\033[97mServo hors limite \033[0m")
    else :
        print("  ❗ servo",id,": ","\033[41m\033[97mServo hors limite ! \033[0m")

import os

ANGLE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "angles.json")

def save_angles_to_json(filename=ANGLE_FILE):
    try:
        with open(filename, "w") as f:
            json.dump(current_angles, f, indent=2)
    except Exception as e:
        print(f"  ✘ Erreur sauvegarde JSON: {e}")

## bouge
def bouge(a,b=None,c=None,d=None,e=None,f=None):
    """ place les 6 servos à l'angle 
    bouge(servo1,servo2=None,servo3=None,servo4=None,servo5=None, servo6=None)"""
    bouge1(a)
    if b!=None:
        bouge2(b)
    if e!=None:
        bouge3(c)
    if e!=None:
        bouge4(d)
    if e!=None:
        bouge5(e)
    if f!=None:
        bouge6(f)
        
def bouge_tete(a,b):
    bouge5(a)
    bouge6(b)
    
def bouge2(a,b,c,d,e=None,f=None):
    """ place les 6 servos à l'angle 
    bouge(servo1,servo2,servo3,servo4,servo5=None, servo6=None)"""
    bouge1(a)
    bouge2(b)
    bouge3(c)
    bouge4(d)
    if e!=None:
        bouge5(e)
    if f!=None:
        bouge6(f)
        
def posangle(a,b,c,d,e=None,f=None):
    """ place les 6 servos à l'angle 
    bouge(servo1,servo2,servo3,servo4,servo5=None, servo6=None)"""
    bouge(a,b,c,d,e=None,f=None)      
    #lecture_angles()
        
def pos(a,b,c,d):
    """pos(a,b,c,d): Commande les 4 servos du bras en pos absolue"""
    if LIMITS[1][0]<=a<=LIMITS[1][1]:
        bougepos1(a)
    else :
        
        hors_limite(1)
    if LIMITS[2][0]<=b<=LIMITS[2][1]:
        bougepos2(b)
    else :
        hors_limite(2)
    if LIMITS[3][0]<=c<=LIMITS[3][1]:
        bougepos3(c)
    else :
        hors_limite(3)
    if LIMITS[4][0]<=d<=LIMITS[4][1]:
        bougepos4(d)
    else :
        hors_limite(4)
    time.sleep(0.2)
    lecturepos()
    lecture_angles()
    
def pos1():
    pos(724,1358,748,500)
    #lecture_angles()

### bougeposx(pos en pas):  ###############################################################################
def bougepos1(a):
    """place en pas (entre 0 et 4096) le servo d’id 1"""
    if LIMITS[1][0]<=a<=LIMITS[1][1]:
        pm[0]=a
    else :
        hors_limite(1)
    #lecture_angles()
def bougepos2(b):
    """place en pas (entre 0 et 4096) le servo d’id 2"""
    if LIMITS[2][0]<=b<=LIMITS[2][1]:
        pm[1]=b
    else :
        hors_limite(2)
    
def bougepos3(c):
    """place en pas (entre 0 et 1024) le servo d’id 3"""
    if LIMITS[3][0]<=c<=LIMITS[3][1]:
        pm[2]=c
    else :
        hors_limite(3)
    
def bougepos4(d):
    """place en pas (entre 0 et 1024) le servo d’id 4"""
    if LIMITS[4][0]<=d<=LIMITS[4][1]:
        pm[3]=d
    else :
        hors_limite(4)
    
def bougepos5(e):
    """place en pas (entre 0 et 1024) le servo d’id 5"""
    if LIMITS[5][0]<=e<=LIMITS[5][1]:
        pm[4]=e
    else :
        hors_limite(5)
    #lecture_angles()
def bougepos6(f):
    """place en pas (entre 0 et 1024) le servo d’id 6"""
    if LIMITS[6][0]<=f<=LIMITS[6][1]:
        pm[5]=f
    else :
        hors_limite(6)
    #lecture_angles()
        
### bougex(angle):  ###############################################################################
def bouge1(angle):
    print("  🦾 l'epaule (servo 1)) se place en angle ",angle)
    current_angles["servo_1"] = angle
    pos  = LIMITS[1][1]-int(RATIO_MX64*angle) - int(RATIO_MX64*18)
    bougepos1(pos)
    save_angles_to_json()  
def bouge2(angle):
    print("  🦾 l'epaule (servo 2) se place en angle ",angle)
    current_angles["servo_2"] = angle
    pos  = LIMITS[2][1]-int(RATIO_MX64*angle)
    bougepos2(pos)
    save_angles_to_json()
    
def bouge3(angle):
    print("  🦾 le coude (servo 3) se place en angle ",angle)
    current_angles["servo_3"] = angle
    pos  = LIMITS[3][0]+int(RATIO_AX12*angle)
    bougepos3(pos)
    save_angles_to_json()
      
def bouge4(angle):
    print("  🦾 le poignet (servo 4) se place en angle ",angle)
    current_angles["servo_4"] = angle
    pos  = 512+int(RATIO_AX12*angle)
    bougepos4(pos)
    save_angles_to_json()
    
def bouge5(angle):
    print("  👵 la tete (servo 5) se place en angle ",angle)
    current_angles["servo_5"] = angle
    pos  = (LIMITS[5][0]+LIMITS[5][1])//2 + int(RATIO_AX12*angle) 
    bougepos5(pos)
    save_angles_to_json()
     
def bouge6(angle):
    print("  👵 la tete (servo 6) se place en angle ",angle)
    current_angles["servo_6"] = angle
    pos  = (LIMITS[6][0]+LIMITS[6][1])//2 + int(RATIO_AX12*angle)
    bougepos6(pos)
    save_angles_to_json()
        
    
### decalposx(pos en pas):  ###############################################################################
def decalpos1(a):
    """décale en pas le servo d’id 1"""
    pos=lecturepos()[0]
    bougepos1(pos+a)
    #lecture_angles()
def decalpos2(a):
    """décale en pas le servo d’id 2"""
    pos=lecturepos()[1]
    bougepos2(pos+a)
    
def decalpos3(a):
    """décale en pas le servo d’id 3"""
    pos=lecturepos()[2]
    bougepos3(pos+a)
    
def decalpos4(a):
    """décale en pas le servo d’id 4"""
    pos=lecturepos()[3]
    bougepos4(pos+a)
    
def decalpos5(a):
    """décale en pas le servo d’id 5"""
    pos=lecturepos()[4]
    bougepos5(pos+a)
    
def decalpos6(a):
    """décale en pas le servo d’id 6"""
    pos=lecturepos()[5]
    bougepos6(pos+a)
    
### decalx(angle):  ###############################################################################   
def decal1(angle):
    """décale en degrés le servo d’id 1"""
    print("  🦾 l'epaule (servo 1) se deplace de ",angle)
    pos=lecturepos()[0]
    bougepos1(pos-int(RATIO_MX64*angle))   
    #lecture_angles()
def decal2(angle):
    """décale en degrés le servo d’id 2"""
    print("  🦾 l'epaule (servo 2) se deplace de ",angle)
    pos=lecturepos()[1]
    bougepos2(pos-int(RATIO_MX64*angle)) 
    
def decal3(angle):
    """décale en degrés le servo d’id 3"""
    print("  🦾 le coude (servo 3) se deplace de ",angle)
    pos=lecturepos()[2]
    bougepos3(pos+int(RATIO_AX12*angle))   
    
def decal4(angle):
    """décale en degrés le servo d’id 4"""
    print("  🦾 le poignet (servo 4) tourne de ",angle)
    pos=lecturepos()[3]
    bougepos4(pos+int(RATIO_AX12*angle))
    
def decal5(angle):
    """décale en degrés le servo d’id 5"""
    print("  👵 la tete (servo 5) se deplace de ",angle)
    pos=lecturepos()[4]
    bougepos5(pos+int(RATIO_AX12*angle))
    
def decal6(angle):
    """décale en degrés le servo d’id 6"""
    print("  👵 la tete (servo 6) se deplace de ",angle)
    pos=lecturepos()[5]
    bougepos6(pos+int(RATIO_AX12*angle))
    
#################### oui non  """""""""""""""""""""""""
def non(n=1):
    print(" 🤖 le robot fait NON de la tete")
    
def oui(n=1):
    print("🤖 le robot fait OUI de la tete")

def coucou():
    """ fait faire un geste de coucou """
    def print(*args, **kwargs):
        builtins.print("\033[42m", end="")   
        builtins.print(*args, **kwargs)
        builtins.print("\033[0m", end="")    # reset
    print("  🤖 le robot fait coucou")
    time.sleep(1)
    pos1()
    time.sleep(0.8)
    bouge5(40)
    for i in range(3):
        bougepos3(700)
        time.sleep(0.3)
        bougepos3(748)
        time.sleep(0.3)
    bouge5(-40)
    for i in range(3):
        bouge4(-90)
        time.sleep(0.3)
        bouge4(90)
        time.sleep(0.3)
        bouge4(0)
    bouge5(0)
  
def test():
    """ suite de mouvement pour verifier que tous les servos sont ok"""
    posinit()
    time.sleep(0.5)
    pos1()
    time.sleep(0.8)
    for i in range(3):
        bouge3(700)
        time.sleep(0.3)
        bouge3(748)
        time.sleep(0.3)
    oui()
    non()
    posinit()


##########################################################################       
# --- Variables globales ---
sliders = []
console_entry = None
console_output = None

# --- Console ---
def run_console_command(event=None):
    global console_entry, console_output
    code = console_entry.get()
    console_output.insert(tk.END, f">>> {code}\n")
    try:
        exec(code, globals())
    except Exception as e:
        console_output.insert(tk.END, f"Erreur : {e}\n")

# --- Mise à jour sliders depuis les angles ---
def update_sliders_from_angles():
    try:
        angles = lecture_angles()
        for i in range(min(6, len(sliders))):
            sliders[i].set(angles[i])
    except Exception as e:
        print(f"Erreur dans update_sliders_from_angles : {e}")

# --- Ajout fader vertical ---
def add_slider(parent, label, from_, to, command):
    frame = tk.Frame(parent, bg="#f0f0f0")
    frame.pack(side=tk.LEFT, padx=10)
    tk.Label(frame, text=label, font=("Arial", 10), bg="#f0f0f0").pack()
    scale = tk.Scale(frame, from_=from_, to=to, resolution=1, orient=tk.VERTICAL, command=lambda v: command(int(v)))
    scale.pack()
    sliders.append(scale)


# --- Interface principale ---
def graph_old():
    global console_entry, console_output

    root = tk.Tk()
    root.title("from maintenance_init_servos")
    root.configure(bg="#f0f0f0")

    tk.Label(root, text=" Contrôle Servos Bassem", font=("Arial", 10, "bold"), bg="#f0f0f0").pack(pady=5)

    # Première ligne : faders 1 à 4
    frame_faders1 = tk.Frame(root, bg="#f0f0f0")
    frame_faders1.pack()

    add_slider(frame_faders1, "epaule::servo 1", 150, -18, bouge1)
    add_slider(frame_faders1, "epaule::servo 2", 145, 0, bouge2)
    add_slider(frame_faders1, "coude::servo 3", 132, 0, bouge3)
    add_slider(frame_faders1, "poignet::servo 4", 88, -88, bouge4)

    # Deuxième ligne : fader 5 horizontal et fader 6 vertical
    frame_faders2 = tk.Frame(root, bg="#f0f0f0")
    frame_faders2.pack(pady=10)

    # Fader 5 : horizontal et plus petit
    frame5 = tk.Frame(frame_faders2, bg="#f0f0f0")
    frame5.pack(side=tk.LEFT, padx=10)
    tk.Label(frame5, text="tete::servo 5", font=("Arial", 10), bg="#f0f0f0").pack()
    scale5 = tk.Scale(frame5, from_=-88, to=88, orient=tk.HORIZONTAL, length=200, command=lambda v: bouge5(int(v)))
    scale5.pack()
    sliders.append(scale5)

    # Fader 6 : vertical
    add_slider(frame_faders2, "tete::servo 6", 40, -50, bouge6)

    # Boutons de contrôle
    frame_buttons = tk.Frame(root, bg="#f0f0f0")
    frame_buttons.pack(pady=10)

    btn_style = {"font": ("Arial", 10, "bold"), "width": 10, "bg": "#e0e0e0", "relief": tk.RAISED}
    tk.Button(frame_buttons, text="pon", command=pon, **btn_style).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_buttons, text="pof", command=pof, **btn_style).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_buttons, text="coucou", command=coucou, **btn_style).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_buttons, text="posinit", command=posinit, **btn_style).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_buttons, text="config", command=config, **btn_style).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_buttons, text="Sync. faders", command=update_sliders_from_angles, **btn_style).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_buttons, text="Quitter", command=root.destroy, bg="#0000ff", fg="white", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=10)

    root.mainloop()
    
    
def graph():
    global console_entry, console_output

    root = tk.Tk()
    root.title("from maintenance_init_servos")
    root.configure(bg="#f0f0f0")

    tk.Label(root, text=" Contrôle Servos Bassem", font=("Arial", 10, "bold"), bg="#f0f0f0").pack(pady=5)

    # Première ligne : faders 1 à 4
    frame_faders1 = tk.Frame(root, bg="#f0f0f0")
    frame_faders1.pack()

    add_slider(frame_faders1, "epaule::servo 1", 150, -18, bouge1)
    add_slider(frame_faders1, "epaule::servo 2", 145, 0, bouge2)
    add_slider(frame_faders1, "coude::servo 3", 132, 0, bouge3)
    add_slider(frame_faders1, "poignet::servo 4", 88, -88, bouge4)

    # Deuxième ligne : fader 5 horizontal et fader 6 vertical
    frame_faders2 = tk.Frame(root, bg="#f0f0f0")
    frame_faders2.pack(pady=10)

    # Fader 5 : horizontal et plus petit
    frame5 = tk.Frame(frame_faders2, bg="#f0f0f0")
    frame5.pack(side=tk.LEFT, padx=10)
    tk.Label(frame5, text="tete::servo 5", font=("Arial", 10), bg="#f0f0f0").pack()
    scale5 = tk.Scale(frame5, from_=-88, to=88, orient=tk.HORIZONTAL, length=200, command=lambda v: bouge5(int(v)))
    scale5.pack()
    sliders.append(scale5)

    # Fader 6 : vertical
    add_slider(frame_faders2, "tete::servo 6", 40, -50, bouge6)

    # Boutons de contrôle
    frame_buttons = tk.Frame(root, bg="#f0f0f0")
    frame_buttons.pack(pady=10)

    btn_style = {"font": ("Arial", 10, "bold"), "width": 10, "bg": "#e0e0e0", "relief": tk.RAISED}

    # --- Ligne 1 ---
    frame_btn_row1 = tk.Frame(frame_buttons, bg="#f0f0f0")
    frame_btn_row1.pack(pady=2)
    tk.Button(frame_btn_row1, text="pon", command=pon, **btn_style).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_btn_row1, text="pof", command=pof, **btn_style).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_btn_row1, text="coucou", command=coucou, **btn_style).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_btn_row1, text="posinit", command=posinit, **btn_style).pack(side=tk.LEFT, padx=5)

    # --- Ligne 2 ---
    frame_btn_row2 = tk.Frame(frame_buttons, bg="#f0f0f0")
    frame_btn_row2.pack(pady=2)
    tk.Button(frame_btn_row2, text="config", command=config, **btn_style).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_btn_row2, text="Sync. faders", command=update_sliders_from_angles, **btn_style).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_btn_row2, text="Quitter", command=root.destroy, bg="#0000ff", fg="white", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=10)

    root.mainloop()


    
""" console

import traceback

# Historique des commandes
command_history = []
history_index = -1


def run_console_command(event=None):
    global console_entry, console_output, command_history, history_index

    cmd = console_entry.get().strip()
    if not cmd:
        return

    # Ajout dans l'historique
    command_history.append(cmd)
    history_index = len(command_history)

    # Affiche la commande tapée
    console_output.insert(tk.END, f">>> {cmd}\n")
    console_entry.delete(0, tk.END)

    # Redirection stdout/stderr
    old_stdout, old_stderr = sys.stdout, sys.stderr
    sys.stdout, sys.stderr = io.StringIO(), io.StringIO()

    try:
        try:
            # Essayer d'évaluer une expression (2+2, son.parler(...), etc.)
            result = eval(cmd, globals())
            if result is not None:
                print(repr(result))
        except SyntaxError:
            # Sinon exécuter (utile pour def, import, for, etc.)
            exec(cmd, globals())
        except Exception:
            traceback.print_exc()
    finally:
        # Récupérer ce qui a été écrit
        output, errors = sys.stdout.getvalue(), sys.stderr.getvalue()
        if output:
            console_output.insert(tk.END, output)
        if errors:
            console_output.insert(tk.END, errors)

        # Restaurer stdout/stderr
        sys.stdout, sys.stderr = old_stdout, old_stderr

    console_output.see(tk.END)  # scroll auto


def navigate_history(event):
    global history_index
    if command_history:
        if event.keysym == "Up":
            history_index = max(0, history_index - 1)
        elif event.keysym == "Down":
            history_index = min(len(command_history), history_index + 1)
        if 0 <= history_index < len(command_history):
            console_entry.delete(0, tk.END)
            console_entry.insert(0, command_history[history_index])
        else:
            console_entry.delete(0, tk.END)


def console():
    global console_entry, console_output

    root = tk.Tk()
    root.title("from maintenance_init_servos")
    root.configure(bg="#f0f0f0")

    tk.Label(root, text="Contrôle Servos Bassem", font=("Arial", 10, "bold"), bg="#f0f0f0").pack(pady=5)

    # ... ton code sliders / boutons inchangé ...

    # Console Python
    tk.Label(root, text="Console Python", font=("Arial", 7, "bold"), bg="#f0f0f0").pack(pady=(5, 5))

    console_frame = tk.Frame(root, bg="#f0f0f0")
    console_frame.pack(padx=10, pady=5, fill=tk.X)

    console_entry = tk.Entry(console_frame, font=("Courier", 10), width=70)
    console_entry.pack(side=tk.LEFT, padx=5)
    console_entry.bind("<Return>", run_console_command)
    console_entry.bind("<Up>", navigate_history)
    console_entry.bind("<Down>", navigate_history)

    tk.Button(console_frame, text="Exécuter", command=run_console_command).pack(side=tk.LEFT)

    console_output = tk.Text(root, height=10, width=90, bg="#000", fg="#0f0", font=("Courier", 10))
    console_output.pack(padx=10, pady=5)

    root.mainloop()

"""
# ===== MODIFICATIONS AJOUTÉES =====
#
# Synchronisation des angles avec Unity via angles.json
#
# Ajouts :
#  - import json
#  - import os
#  - constante ANGLE_FILE pointant vers angles.json
#  - variable globale current_angles contenant les angles des 6 servos
#  - fonction save_angles_to_json() pour sauvegarder current_angles
#    dans angles.json
#
# Modifications dans les fonctions bouge1() à bouge6() :
#  - mise à jour de current_angles["servo_N"]
#  - appel de save_angles_to_json() après chaque mouvement
#
# Objectif :
#  - lorsqu'un servo est commandé depuis Python
#    (sliders, scénarios, console, etc.),
#    les angles sont enregistrés dans angles.json
#  - server.py surveille ce fichier et envoie automatiquement
#    les nouveaux angles à Unity via WebSocket
#
# Architecture :
#
# Python (bouge1..bouge6)
#          ↓
#   current_angles
#          ↓
#    angles.json
#          ↓
#      server.py
#          ↓
#      WebSocket
#          ↓
#        Unity
#
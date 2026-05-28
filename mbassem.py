"""
  ____           _____ _____ ______ __  __ 
 |  _ \   /\    / ____/ ____|  ____|  \/  |
 | |_) | /  \  | (___| (___ | |__  | \  / |
 |  _ < / /\ \  \___ \\___ \|  __| | |\/| |
 | |_) / ____ \ ____) |___) | |____| |  | |
 |____/_/    \_\_____/_____/|______|_|  |_|
 
mbassem

@author: TNSI

@description : importe toutes les librairies de maintenance de Bassem 
"""


#import bassem_son_seul as son

# lib si non connecté au robot :
from maintenance_init_servos import *
import maintenance_son as son
import maintenance_oeil as oeil
import bassem_credits as credit 
#import bassem_random as br
import time
import threading


credit.banner1()
print("  ")

# Codes ANSI
BLACK = "\033[30m"           # texte noir
YELLOW_BG = "\033[43m"       # fond jaune
RESET = "\033[0m"

print(f"  {YELLOW_BG}{BLACK}BASSEM EN MODE SIMULATION.  {RESET}")
#print("  Il faudra changer la premiere ligne du script pour tester sur le robot")
print(  "   ")

### pour le thread:
def th(func, *args, **kwargs):
    """Lance func(*args, **kwargs) dans un autre thread et retourne l'objet Thread
    exemple d'appel : t = th(fct1, 3, 4)  Lance fct1 dans un autre thread
    """
    t = threading.Thread(target=func, args=args, kwargs=kwargs)
    t.start()
    print(func," lancée dans un autre thread")
    return t  
###################################################################


import tkinter as tk
import sys, io, code, re

# Console interactive Python
py_console = code.InteractiveConsole(globals())

# Regex ANSI
ansi_re = re.compile(r'\033\[(\d+)m')

# Couleurs ANSI texte
ansi_fg = {
    "30": "black",
    "31": "red",
    "32": "green",
    "33": "yellow",
    "34": "blue",
    "35": "magenta",
    "36": "cyan",
    "37": "white",
}

# Couleurs ANSI fond
ansi_bg = {
    "40": "black",
    "41": "red",
    "42": "green",
    "43": "yellow",
    "44": "blue",
    "45": "magenta",
    "46": "cyan",
    "47": "white",
}


def insert_with_ansi(text_widget, text):
    """Insère du texte dans Tkinter en interprétant les couleurs ANSI."""
    pos = 0
    fg, bg = "white", "black"  # couleurs par défaut

    for match in ansi_re.finditer(text):
        start, end = match.span()
        if start > pos:
            tag_name = f"{fg}_{bg}"
            text_widget.insert(tk.END, text[pos:start], tag_name)

        code_val = match.group(1)

        if code_val == "0":  # reset
            fg, bg = "white", "black"
        elif code_val in ansi_fg:
            fg = ansi_fg[code_val]
        elif code_val in ansi_bg:
            bg = ansi_bg[code_val]

        pos = end

    if pos < len(text):
        tag_name = f"{fg}_{bg}"
        text_widget.insert(tk.END, text[pos:], tag_name)


def run_console_command(event=None):
    global console_entry, console_output, py_console

    cmd = console_entry.get().strip()
    if not cmd:
        return

    console_output.insert(tk.END, f">>> {cmd}\n", "white_black")
    console_entry.delete(0, tk.END)

    old_stdout, old_stderr = sys.stdout, sys.stderr
    sys.stdout, sys.stderr = io.StringIO(), io.StringIO()

    try:
        py_console.push(cmd)
    finally:
        output, errors = sys.stdout.getvalue(), sys.stderr.getvalue()
        if output:
            insert_with_ansi(console_output, output)
        if errors:
            insert_with_ansi(console_output, errors)

        sys.stdout, sys.stderr = old_stdout, old_stderr

    console_output.see(tk.END)


def console():
    global console_entry, console_output

    root = tk.Tk()
    root.title("Console Python from mbassem")
    root.configure(bg="#f0f0f0")

    tk.Label(root, text="Console Python", font=("Arial", 10, "bold"), bg="#f0f0f0").pack(pady=5)

    console_frame = tk.Frame(root, bg="#f0f0f0")
    console_frame.pack(padx=10, pady=5, fill=tk.X)

    console_entry = tk.Entry(console_frame, font=("Courier", 10), width=70)
    console_entry.pack(side=tk.LEFT, padx=5)
    console_entry.bind("<Return>", run_console_command)

    tk.Button(console_frame, text="Exécuter", command=run_console_command).pack(side=tk.LEFT)

    console_output = tk.Text(root, height=15, width=90, bg="#000", fg="white", font=("Courier", 10))
    console_output.pack(padx=10, pady=5)

    # Crée les tags (couleur texte + fond)
    for fg in ansi_fg.values():
        for bg in ansi_bg.values():
            tag_name = f"{fg}_{bg}"
            console_output.tag_config(tag_name, foreground=fg, background=bg)

    root.mainloop()
    
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
# --- Interface principale ---
def graph():
    global console_entry, console_output

    root = tk.Tk()
    root.title("Contrôle des Servos de Bassem")
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
    tk.Button(frame_buttons, text="poff", command=poff, **btn_style).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_buttons, text="coucou", command=coucou, **btn_style).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_buttons, text="posinit", command=posinit, **btn_style).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_buttons, text="config", command=config, **btn_style).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_buttons, text="Sync. faders", command=update_sliders_from_angles, **btn_style).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_buttons, text="Quitter", command=root.destroy, bg="#0000ff", fg="white", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=10)

    root.mainloop()


### pour faire choli #########
from rich import print as rprint

def print_rouge(msg):
    rprint(f"[red]{msg}[/red]")

def print_vert(msg):
    rprint(f"[green]{msg}[/green]")

def print_jaune(msg):
    rprint(f"[yellow]{msg}[/yellow]")

def print_bleu(msg):
    print(msg)
    #rprint(f"[blue]{msg}[/blue]")

def print_orange(msg):
    rprint(f"[dark_orange3]{msg}[/dark_orange3]")  # Simili-orange

def print_magenta(msg):
    rprint(f"[magenta]{msg}[/magenta]")

def print_cyan(msg):
    rprint(f"[cyan]{msg}[/cyan]")

def print_gris(msg):
    rprint(f"[grey50]{msg}[/grey50]")  # Gris moyen
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
# ajout perso pour conncter avec server.py 
def move_headLF(angle):
    try:
        bouge5(angle)   # servo tête gauche/droite
    except Exception as e:
        print("Erreur move_headLF :", e)

def move_headUD(angle):
    try:
        bouge6(angle)   # servo tête haut/bas
    except Exception as e:
        print("Erreur move_headUD :", e)


def move_rightArmSide(angle):
    try:
        bouge2(angle)
    except Exception as e:
        print("Erreur move_rightArmSide :", e)


def move_rightArm(angle):
    try:
        bouge1(angle)
    except Exception as e:
        print("Erreur move_rightArm :", e)


def move_rightLowerArm(angle):
    try:
        bouge3(angle)
    except Exception as e:
        print("Erreur move_rightLowerArm :", e)

# sur le simulateur il n'y a que servos 1 2 et 3 donc on ne peut bouger que 1 bras
#def move_leftArmSide(angle):
#def move_leftArm(angle):
#def move_leftLowerArm(angle):
 
# code que j'ai ajouté car sinon je n'avais pas les sliders    
if __name__ == "__main__":
    graph()
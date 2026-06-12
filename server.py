import asyncio
import websockets
import json
import os
import mbassem
import base64
#import bassem

import Robot_son

ANGLE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "angles.json")
active_websockets = set()  # Piste les websockets actifs pour envoyer les angles



def read_angles_json(filename=ANGLE_FILE):
    try:
        if not os.path.exists(filename):
            return None
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [
            data.get("servo_1", 0),
            data.get("servo_2", 0),
            data.get("servo_3", 0),
            data.get("servo_4", 0),
            data.get("servo_5", 0),
            data.get("servo_6", 0),
        ]
    except Exception as e:
        print("Erreur lecture angles.json :", e)
        return None



# envoi les angles a unity ------------------------------------------------------------------------
async def broadcast_angles_to_unity(angles):
    """Envoie les angles à tous les clients Unity connectés."""
    message = json.dumps({"type": "angles_update", "angles": angles, "source": "py"})
    # Créer une copie pour éviter les problèmes de modification pendant l'itération
    websockets_copy = list(active_websockets)
    for ws in websockets_copy:
        try:
            await ws.send(message)
        except Exception as e:
            print(f"Erreur envoi à Unity: {e}")
            # Retirer les websockets fermés
            active_websockets.discard(ws)
            
# reçois fichier WAV depuis Unity
def save_audio_from_unity(data):
    filename = data.get("filename", "unity_audio.wav")
    audio_base64 = data.get("audioBase64", "")

    if audio_base64 == "":
        print("Audio reçu vide")
        return None

    audio_bytes = base64.b64decode(audio_base64)

    audio_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)

    with open(audio_path, "wb") as f:
        f.write(audio_bytes)

    print("Fichier audio reçu et sauvegardé :", audio_path)

    return audio_path

# récupère un json avec les angles depuis unity pour bouger le simulateur -------------------------
async def handler(websocket):
    global active_websockets
    active_websockets.add(websocket)
    print("Unity connecté !")
    async for message in websocket:
        try:
            data = json.loads(message)  # récupère depuis Unity via websocket
            
            # recevoir le fichier wav envoyé par Unity
            if data.get("type") == "audio":
                audio_path = save_audio_from_unity(data)
                
                if audio_path:
                    Robot_son.reagir_au_wav(audio_path)
                    
                continue
        
            
            # éviter les boucles : ignorer les messages envoyés par Python
            if data.get("source") == "py":
                continue

            # récupère le json envoyé depuis unity
            headLF = data.get("headLF", 0)
            headUD = data.get("headUD", 0)
            rightArmSide = data.get("rightArmSide", 0)
            rightArm = data.get("rightArm", 0)
            rightLowerArm = data.get("rightLowerArm", 0)
            

            # exécution commande
            mbassem.bouge(rightArm, rightArmSide, rightLowerArm, 0, headLF, headUD)
            # pour bouger le vrai robot (en théorie)
          #  bassem.bouge(rightArm, rightArmSide, rightLowerArm, 0, headLF, headUD)
            print("------------------------------------------------------------------")
        except Exception as e:
            print("Erreur :", e)
        
    # Retirer le websocket fermé
    active_websockets.discard(websocket)
    print("Unity déconnecté !")


async def poll_angles_file():
    old_angles = read_angles_json()
    while True:
        await asyncio.sleep(0.1)
        new_angles = read_angles_json()
        if new_angles is None:
            continue
        if old_angles is None:
            old_angles = new_angles
            continue
        if new_angles != old_angles:
            old_angles = new_angles
            # Envoyer les nouveaux angles à Unity
            await broadcast_angles_to_unity(new_angles)

def handle_speech_command(text):
    """en fonction du texte reçu depuis Unity Bassem répond"""
    print("Commande vocale reçue :", text)
    Robot_son.reagir_au_texte(text)
    
    
    
#------------------------------------------------------------------------------
async def main():
    server = await websockets.serve(handler, "localhost", 8765)
    print("Serveur lancé")
    poll_task = asyncio.create_task(poll_angles_file())
    try:
        await server.wait_closed()
    finally:
        poll_task.cancel()


asyncio.run(main())
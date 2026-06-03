modifications 
=============================================

Objectif : détailler toutes les modifications apportées dans le workspace
pour `mbassem.py` et `maintenance_init_servos.py`, avec numéros de ligne, et
fournir une explication claire du rôle de `server.py`.

1) `maintenance_init_servos.py` 
--------------------------------------------------------
- `import json` ajouté : ligne 22
- `import os` ajouté : ligne 23
- `current_angles` (dict) ajouté : ligne 28
- `def save_angles_to_json(...)` ajouté : définition à la ligne 454

Modifs dans les fonctions `bougeN` :
- `def bouge1(...)` : ligne 574 — ajout de `global current_angles`, mise à jour
  `current_angles["servo_1"] = angle` et appel `save_angles_to_json()`
- `def bouge2(...)` : ligne 484 — ajout de `global current_angles`, mise à jour
  `current_angles["servo_2"] = angle` et appel `save_angles_to_json()`
- `def bouge3(...)` : ligne 589 — ajout de `global current_angles`, mise à jour
  `current_angles["servo_3"] = angle` et appel `save_angles_to_json()`
- `def bouge4(...)` : ligne 597 — ajout de `global current_angles`, mise à jour
  `current_angles["servo_4"] = angle` et appel `save_angles_to_json()`
- `def bouge5(...)` : ligne 605 — ajout de `global current_angles`, mise à jour
  `current_angles["servo_5"] = angle` et appel `save_angles_to_json()`
- `def bouge6(...)` : ligne 613 — ajout de `global current_angles`, mise à jour
  `current_angles["servo_6"] = angle` et appel `save_angles_to_json()`


2) `mbassem.py` — modification détectée
-------------------------------------
- Fonction ajoutée : `def move_all(a,b,c,d,e,f)` à la ligne 302.


3) `server.py` — rôle et fonctionnement
---------------------------------------
- Rôle général : serveur websocket qui reçoit des messages JSON depuis Unity
  et transmet les commandes d'angles au simulateur Python et/ou renvoie les
  angles à Unity.
- Points clés de l'implémentation actuelle :
  - Ecoute WebSocket sur `localhost:8765` (via `websockets.serve(handler, ...)`).
  - `handler(websocket)` : boucle asynchrone qui lit les messages JSON envoyés
    par Unity, ignore les messages où `source == 'py'` (éviter les boucles),
    extrait les champs d'angles (`rightArm`, `rightArmSide`, `rightLowerArm`,
    `headLF`, `headUD`) et appelle `mbassem.move_all(...)` pour appliquer les
    angles côté simulateur.
  - Surveillance du fichier `angles.json` via `poll_angles_file()` : si le
    fichier change, le serveur lit les nouvelles valeurs et les broadcast à
     Unity (avec `broadcast_angles_to_unity`).
  - `get_current_angles()` construit une liste à partir de `maintenance_init_servos.current_angles`.



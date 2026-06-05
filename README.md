# modifications

Objectif : détailler les modifications apportées pour permettre la synchronisation
des angles entre Python et Unity via WebSocket et le fichier `angles.json`.

---

1. `maintenance_init_servos.py`

---

Ajouts :

* `import json`
* `import os`
* constante `ANGLE_FILE` pointant vers le fichier `angles.json`
* variable globale :

```python
current_angles = {"servo_1": 0,"servo_2": 0,"servo_3": 0,"servo_4": 0,"servo_5": 0,"servo_6": 0}
```

* fonction :

```python
save_angles_to_json()
```

Cette fonction sauvegarde les angles contenus dans `current_angles`
dans le fichier `angles.json`.

Modifications dans les fonctions `bouge1()` à `bouge6()` :

* mise à jour de l'entrée correspondante dans `current_angles`
* appel de `save_angles_to_json()` après chaque mouvement

Exemple :

```python
current_angles["servo_5"] = angle
save_angles_to_json()
```

Objectif :

Lorsqu'un mouvement est exécuté depuis Python
(sliders, console, scénario, commande manuelle, etc.),
les angles actuels du robot sont automatiquement enregistrés
dans `angles.json` afin qu'ils puissent être récupérés et envoyés à Unity.

---

2. `mbassem.py`

---

Modification :

Ajout du bloc :

```python
if __name__ == "__main__":
    graph()
```

Permettre l'ouverture automatique de l'interface graphique

Lorsque `mbassem.py` est importé par un autre script
(comme `server.py`), l'interface graphique ne se lance pas.

---

3. `server.py`

---

Rôle général :

Serveur WebSocket chargé d'assurer la communication entre Unity
et les scripts Python du projet BASSEM.

Fonctionnement :

### Réception des commandes Unity

* Le serveur écoute sur :

```text
localhost:8765
```

* La fonction `handler(websocket)` reçoit les messages JSON envoyés par Unity.

* Les champs suivants sont récupérés :

```text
headLF
headUD
rightArm
rightArmSide
rightLowerArm
```

* Les messages dont :

```python
source == "py"
```

sont ignorés afin d'éviter les boucles de communication.

* Les angles reçus sont appliqués côté Python via :

```python
mbassem.bouge(...)
```

### Synchronisation Python → Unity

* La fonction `poll_angles_file()` surveille en permanence
  le fichier `angles.json`.

* Lorsqu'un changement est détecté :

  1. les nouveaux angles sont lus ;
  2. ils sont envoyés à Unity via `broadcast_angles_to_unity()`.

### Broadcast WebSocket

Les angles sont envoyés sous la forme :

```json
{
    "type": "angles_update",
    "angles": [...],
    "source": "py"
}
```

---

4. Architecture finale

---

Commande depuis Unity :

```text
Unity
   ↓
WebSocket
   ↓
server.py
   ↓
mbassem.bouge(...)
   ↓
maintenance_init_servos
   ↓
angles.json
```

Commande depuis Python :

```text
Sliders Python / Console / Scénario
                ↓
          bouge1..bouge6
                ↓
         current_angles
                ↓
          angles.json
                ↓
           server.py
                ↓
           WebSocket
                ↓
             Unity
```

Le fichier `angles.json` sert donc de point de synchronisation
entre les mouvements réalisés côté Python et leur représentation
dans Unity.

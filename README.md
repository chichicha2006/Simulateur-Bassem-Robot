# Simulateur-Bassem-Robot
Etapes à suivre et fichier nécessaires pour utiliser le simulateur robot bassem 

1. installer Anaconda (éditeur python) Spyder est inclu dedans 
2. télécharger et décompresser le fichier zip bassem install lib dans votre répertoire de travail (dans le même répertoire que le fichier python qui utilisera les lib).
3. ouvrir anaconda prompt 
4. se situer dans votre répertoire de travail (la ou vous avez téléchargé bassem install lib) (cd) puis tapez "bassem_install_lib.bat"
5. télécharger et décompresser le fichier zip lib bassem251014  dans le même répertoire

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Si vous êtes connecté au robot: 
- utiliser les lib bassem_x
- bassem.py : pour utiliser BASSEM pour de vrai.

Si vous n’y êtes pas connecté: 
- utiliser les lib maintenance_x
- mbassem.py : pour utiliser BASSEM en mode simulation console. 
 
Executer mbassem.py : dans le terminal se trouvent les position (angles ° des servos) et une autre fenêtre s’ouvre avec des sliders
si les sliders ne s’affichent pas, ajouter     if __name__ == "__main__":
                                                    graph() 
à la fin du code dans mbassem.py .

@echo off
setlocal EnableDelayedExpansion

echo.
echo TNSI R.DOISNEAU - CORBEIL
echo -------------------------------
echo INSTALLATION DES LIB DE BASSEM 
echo -------------------------------
:: Vérification de Python
python --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo Python n'est pas installé ou pas dans le PATH.

)


echo Version de Python detectee : !PYVERSION!

:: Vérifie si Python est 3.7
IF "!PYMAJOR!" NEQ "3" (
    echo Ce script requiert Python 3.7. Version detectee : !PYVERSION!

)
IF "!PYMINOR!" NEQ "7" (
    echo ATTENTION : Ce script est optimise pour Python 3.7.
    echo La version detectee est !PYVERSION!. Risques de probleme avec PyAudio.
)

:: Affichage de l'environnement virtuel
python -c "import sys; print('Env virtuel actif' if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix) else 'Pas d''environnement virtuel')" 

echo.
echo --------------------------------------
echo INSTALLATION DES BIBLIOTHEQUES PYTHON
echo --------------------------------------

:: Mise à jour pip
python -m pip install --upgrade pip

:: Installations
pip install pyserial
pip install pygame
pip install SpeechRecognition
python -m pip install opencv-python
pip install dynamixel-sdk
pip install wave
pip install pyttsx3==2.71
pip install cmake
echo pip install pybullet (on zappe le coup la)

:: PyAudio local
echo.
echo --------------------------------------
echo INSTALLATION DE PyAudio (fichier local)
echo --------------------------------------

IF EXIST PyAudio-0.2.11-cp37-cp37m-win_amd64.whl (
    pip install PyAudio-0.2.11-cp37-cp37m-win_amd64.whl
) ELSE (
    echo ERREUR : Le fichier PyAudio-0.2.11-cp37-cp37m-win_amd64.whl est introuvable.
    pause
    exit /b
)

echo.
echo --------------------------------------
echo INSTALLATION TERMINEE !
echo --------------------------------------
pause

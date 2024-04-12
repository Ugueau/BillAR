@echo off
echo Création de l'environnement virtuel
python -m venv .venv

echo Activation de l'environnement virtuel
call .venv\Scripts\activate

echo Installation des bibliothèques
pip install ultralytics opencv-python pygrabber PyDispatcher pyinstaller

echo start projet
python main.py

echo Désactivation de l'environnement virtuel
deactivate

@echo off
echo Création de l'environnement virtuel
python -m venv .venv

echo Activation de l'environnement virtuel
call .venv\Scripts\activate

echo Installation des bibliothèques
pip install ultralytics opencv-python pygrabber PyDispatcher pyinstaller

echo start projet
pyinstaller --noconfirm --onedir --console --name "BillAR" --icon="resources/logo_Billar2.ico" --add-data ".venv/Lib/site-packages/ultralytics;ultralytics/" --hidden-import=ultralytics main.py
xcopy ".\resources\" ".\dist\BillAR\resources\"
xcopy ".\YoloModel\" ".\dist\BillAR\YoloModel\"

echo Compilation réussi, vous pouvez accéder à l'application dans le dossier ./dist/BillAR/BillAR.exe
pause

echo Désactivation de l'environnement virtuel
deactivate

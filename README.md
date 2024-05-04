# BillA.R
Projet de 3ème année de BUT informatique 

## Les Objectifs du projet 
Le projet billA.R, est un système d'assistance pour le célèbre jeu du billard.
Il permet la détection des billes et des queues, afin de créer et d'afficher la trajectoire pour aider le joueur à réaliser son coup.

## Utilisation
Mettez en place le vidéo projecteur et la web cam au-dessus du billard.
Brancher le vidéo projecteur et la web cam à l'ordinateur qui exécutera le projet.
Pour utiliser le projet cloner le repo et exécuter le projet.
Lors du lancement de l'application, dans "Options" sélectionner la web cam utilisé pour filmer le billard.
Cliquer sur "Jouer" et réaliser le calibrage de la web cam et du vidéo projecteur.
Une fois la calibration effectuée le programme détectera les billes et les queues visibles sur le billard. 
Cette détection peut prendre 20 à 30 secs.
Vous n'avez plus qu'à vous amuser avec votre billard ! 

## Démonstration
[Video](https://youtu.be/guS1cG0wH1E)


## Les contributeurs
- Nikola Chevalliot
- Hugo Millot
- Maël Chalon
- Maxence Coeur

## Technologies
- Le projet de base était fait en langage Processing.
- Changement de langage pour utiliser Python v3.11 et faire de l'inteligence artificielle.

## Librairie
/!\ Majuscule importante
- opencv-python
- ultralytics
- pygrabber
- PyDispatcher
- pyinstaller

# Fonctionnement
La nouvelle version du projet repose sur l'intelligence artificielle, pour cela la migration vers un langage adapté était nécessaire à savoir Python. 
Le projet utilise la librairie OpenCV Python permet d'aider à la détection des queues de billard. 
Ultralytics [https://github.com/ultralytics](https://github.com/ultralytics), une librairie Python spécialisé dans l'intelligence artificielle permet la création du modèle YOLO.
Pour l'entrainement du modèle nous avons utilisé 400 images annotées grâce au site [https://app.cvat.ai/](https://app.cvat.ai/)
Pour l'entrainement du modèle nous avons utilisé la puissance de calcul de Google Colab.
La librairie native Tkinter de Python est utilisé pour réaliser l'interface graphique de l'application.

## Command
- Pour compiler le projet veuillez exécuter le script : **compilation_exe.bat** celui-ci génerera un une application en .exe

import json
from Model.Point import Point

class Profil:
    def __init__(self):
        self._nom = ""
        self._webcam_billard_coordonnees_top_left = Point(0, 0)
        self._webcam_billard_coordonnees_top_right = Point(0, 0)
        self._webcam_billard_coordonnees_bot_left = Point(0, 0)
        self._webcam_billard_coordonnees_bot_right = Point(0, 0)

        self._projecteur_billard_coordonnees_top_left = Point(0, 0)
        self._projecteur_billard_coordonnees_top_right = Point(0, 0)
        self._projecteur_billard_coordonnees_bot_left = Point(0, 0)
        self._projecteur_billard_coordonnees_bot_right = Point(0, 0)

    @classmethod
    def charger_profils(self):
        try:
            with open('profils.json', 'r') as json_file:
                data = json.load(json_file)
            return [Profil.from_json(profil) for profil in data]
        except FileNotFoundError:
            # Handle the case where the file does not exist
            return []

    @classmethod
    def delete_profils(self, index:int):
        profils = self.charger_profils()

        profils.remove(profils[index])

        with open('profils.json', 'w') as json_file:
            json.dump([profil.to_json() for profil in profils], json_file, indent=2)
        print("Profils supprimer dans profils.json.")
    @classmethod
    def sauvegarder_profils(self, new_profil):
        profils = self.charger_profils()

        profils.append(new_profil)

        with open('profils.json', 'w') as json_file:
            json.dump([profil.to_json() for profil in profils], json_file, indent=2)
        print("Profils sauvegardés dans profils.json.")

    @property
    def nom(self) -> str:
        return self._nom

    @nom.setter
    def nom(self, new_nom: str) -> None:
        if not isinstance(new_nom, str):
            raise ValueError("Le nom doit être une chaîne.")
        self._nom = new_nom

    @property
    def webcam_billard_coordonnees_top_left(self) -> Point:
        return self._webcam_billard_coordonnees_top_left

    @webcam_billard_coordonnees_top_left.setter
    def webcam_billard_coordonnees_top_left(self, webcam_billard_coordonnees_top_left: Point) -> None:
        if not isinstance(webcam_billard_coordonnees_top_left, Point):
            raise ValueError("La coordonnees_top_left doit être un Point.")
        self._webcam_billard_coordonnees_top_left = webcam_billard_coordonnees_top_left

    @property
    def webcam_billard_coordonnees_top_right(self) -> Point:
        return self._webcam_billard_coordonnees_top_right

    @webcam_billard_coordonnees_top_right.setter
    def webcam_billard_coordonnees_top_right(self, webcam_billard_coordonnees_top_right: Point) -> None:
        if not isinstance(webcam_billard_coordonnees_top_right, Point):
            raise ValueError("La coordonnees_top_right doit être un Point.")
        self._webcam_billard_coordonnees_top_right = webcam_billard_coordonnees_top_right

    @property
    def webcam_billard_coordonnees_bot_right(self) -> Point:
        return self._webcam_billard_coordonnees_bot_right

    @webcam_billard_coordonnees_bot_right.setter
    def webcam_billard_coordonnees_bot_right(self, webcam_billard_coordonnees_bot_right: Point) -> None:
        if not isinstance(webcam_billard_coordonnees_bot_right, Point):
            raise ValueError("La coordonnees_bot_right doit être un Point.")
        self._webcam_billard_coordonnees_bot_right = webcam_billard_coordonnees_bot_right

    @property
    def webcam_billard_coordonnees_bot_left(self) -> Point:
        return self._webcam_billard_coordonnees_bot_left

    @webcam_billard_coordonnees_bot_left.setter
    def webcam_billard_coordonnees_bot_left(self, webcam_billard_coordonnees_bot_left: Point) -> None:
        if not isinstance(webcam_billard_coordonnees_bot_left, Point):
            raise ValueError("La coordonnees_bot_right doit être un Point.")
        self._webcam_billard_coordonnees_bot_left = webcam_billard_coordonnees_bot_left

    @property
    def projecteur_billard_coordonnees_bot_left(self) -> Point:
        return self._projecteur_billard_coordonnees_bot_left

    @projecteur_billard_coordonnees_bot_left.setter
    def projecteur_billard_coordonnees_bot_left(self, projecteur_billard_coordonnees_bot_left: Point) -> None:
        if not isinstance(projecteur_billard_coordonnees_bot_left, Point):
            raise ValueError("La coordonnees_bot_left doit être un Point.")
        self._projecteur_billard_coordonnees_bot_left = projecteur_billard_coordonnees_bot_left

    @property
    def projecteur_billard_coordonnees_bot_right(self) -> Point:
        return self._projecteur_billard_coordonnees_bot_right

    @projecteur_billard_coordonnees_bot_right.setter
    def projecteur_billard_coordonnees_bot_right(self, projecteur_billard_coordonnees_bot_right: Point) -> None:
        if not isinstance(projecteur_billard_coordonnees_bot_right, Point):
            raise ValueError("La coordonnees_top_left doit être un Point.")
        self._projecteur_billard_coordonnees_bot_right = projecteur_billard_coordonnees_bot_right

    @property
    def projecteur_billard_coordonnees_top_left(self) -> Point:
        return self._projecteur_billard_coordonnees_top_left

    @projecteur_billard_coordonnees_top_left.setter
    def projecteur_billard_coordonnees_top_left(self, projecteur_billard_coordonnees_top_left: Point) -> None:
        if not isinstance(projecteur_billard_coordonnees_top_left, Point):
            raise ValueError("La coordonnees_top_left doit être un Point.")
        self._projecteur_billard_coordonnees_top_left = projecteur_billard_coordonnees_top_left

    @property
    def projecteur_billard_coordonnees_top_right(self) -> Point:
        return self._projecteur_billard_coordonnees_top_right

    @projecteur_billard_coordonnees_top_right.setter
    def projecteur_billard_coordonnees_top_right(self, projecteur_billard_coordonnees_top_right: Point) -> None:
        if not isinstance(projecteur_billard_coordonnees_top_right, Point):
            raise ValueError("La coordonnees_top_right doit être un Point.")
        self._projecteur_billard_coordonnees_top_right = projecteur_billard_coordonnees_top_right

    def to_json(self):
        return {
            'nom': self.nom,
            'webcam_billard_coordonnees_top_left': self.webcam_billard_coordonnees_top_left.to_json(),
            'webcam_billard_coordonnees_top_right': self.webcam_billard_coordonnees_top_right.to_json(),
            'webcam_billard_coordonnees_bot_left': self.webcam_billard_coordonnees_bot_left.to_json(),
            'webcam_billard_coordonnees_bot_right': self.webcam_billard_coordonnees_bot_right.to_json(),
            'projecteur_billard_coordonnees_top_left': self.projecteur_billard_coordonnees_top_left.to_json(),
            'projecteur_billard_coordonnees_top_right': self.projecteur_billard_coordonnees_top_right.to_json(),
            'projecteur_billard_coordonnees_bot_left': self.projecteur_billard_coordonnees_bot_left.to_json(),
            'projecteur_billard_coordonnees_bot_right': self.projecteur_billard_coordonnees_bot_right.to_json()
        }

    @classmethod
    def from_json(cls, data):
        profil = cls()
        profil.nom = data['nom']
        profil.webcam_billard_coordonnees_top_left = Point.from_json(data['webcam_billard_coordonnees_top_left'])
        profil.webcam_billard_coordonnees_top_right = Point.from_json(data['webcam_billard_coordonnees_top_right'])
        profil.webcam_billard_coordonnees_bot_left = Point.from_json(data['webcam_billard_coordonnees_bot_left'])
        profil.webcam_billard_coordonnees_bot_right = Point.from_json(data['webcam_billard_coordonnees_bot_right'])
        profil.projecteur_billard_coordonnees_top_left = (
            Point.from_json(data['projecteur_billard_coordonnees_top_left']))
        profil.projecteur_billard_coordonnees_top_right = (
            Point.from_json(data['projecteur_billard_coordonnees_top_right']))
        profil.projecteur_billard_coordonnees_bot_left = (
            Point.from_json(data['projecteur_billard_coordonnees_bot_left']))
        profil.projecteur_billard_coordonnees_bot_right = (
            Point.from_json(data['projecteur_billard_coordonnees_bot_right']))

        return profil

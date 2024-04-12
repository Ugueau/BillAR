import math
import tkinter as tk
import cv2
import numpy as np
from Model.Bille import Bille
from Model.Point import Point
from Model.Queue import Queue
from Singleton.SingletonCache import SingletonCache


class DrawBillard:
    TAGS_BILLE = "bille"
    TAGS_QUEUE = "queue"
    TAGS_TRAJECTOIR = "trajectoire"
    TAGS_BILLARD = "billard"

    @staticmethod
    def draw_bille_fill(canvas: tk.Canvas, bille: Bille, homographie, color: str):
        # on converti le radius en 2 points (center et un point du cercle) pour appliquer l'homographie sur
        # le radius du cercle
        tmp_point = Point(bille.center.x + bille.radius, bille.center.y)

        center = DrawBillard.appliquer_homographie(bille.center, homographie)
        point_radius = DrawBillard.appliquer_homographie(
            tmp_point,
            homographie
        )

        # à partir du centre et du point du cercle dans le plan du projecteur on calcul le nouveau radius
        radius = math.sqrt(
            abs((center.x - point_radius.x) ** 2 + (center.y - point_radius.y) ** 2)
        )

        # on affiche un cercle sur le canvas
        canvas.create_oval(center.x - radius,
                           center.y - radius,
                           center.x + radius,
                           center.y + radius, fill=color, tags=DrawBillard.TAGS_BILLE)

    @staticmethod
    def draw_bille_outline(canvas: tk.Canvas, bille: Bille, homographie, color: str):

        # même principe que pour la methode draw_bille_fill mais avec un affichage outlined dans le canvas
        tmp_point = Point(bille.center.x + bille.radius, bille.center.y)

        center = DrawBillard.appliquer_homographie(bille.center, homographie)
        point_radius = DrawBillard.appliquer_homographie(
            tmp_point,
            homographie
        )

        radius = math.sqrt(
            abs((center.x - point_radius.x) ** 2 + (center.y - point_radius.y) ** 2)
        )

        canvas.create_oval(center.x - radius,
                           center.y - radius,
                           center.x + radius,
                           center.y + radius, width=5, outline=color, tags=DrawBillard.TAGS_BILLE)

    @staticmethod
    def draw_bille_trajectoire(canvas: tk.Canvas, bille: Bille, homographie, color: str):
        # on parcour la liste des point qui forme la trajectoir de la bille passé en paramètre
        # (trajectoire est une paire de point)
        for trajectoire in bille.trajectoire:
            # pour chaque point on applique l'homographie
            p1, p2 = trajectoire
            p1_convert = DrawBillard.appliquer_homographie(p1, homographie)
            p2_convert = DrawBillard.appliquer_homographie(p2, homographie)
            # on affiche le segment sur le canvas
            canvas.create_line(p1_convert.x,
                               p1_convert.y,
                               p2_convert.x,
                               p2_convert.y,
                               fill=color, tags=DrawBillard.TAGS_TRAJECTOIR, width=10)

    @staticmethod
    def draw_queue(canvas: tk.Canvas, queue: Queue, homographie):
        # les queues sont représentée par 2 points, on applique l'homographie a ces deux point
        blue_point = DrawBillard.appliquer_homographie(queue.blue_point, homographie)
        direction_point = DrawBillard.appliquer_homographie(queue.origine_point, homographie)

        # on dessine ensuite un rectangle entre ces deux nouveaux points
        canvas.create_rectangle(blue_point.x,
                                blue_point.y,
                                direction_point.x,
                                direction_point.y, outline="pink", tags=DrawBillard.TAGS_QUEUE)

    @staticmethod
    def draw_queue_trajectoire(canvas: tk.Canvas, queue: Queue, homographie, color: str):
        # on récupère les 2 points de les deux points de la queue et on applique l'homographie
        blue_point = DrawBillard.appliquer_homographie(queue.blue_point, homographie)
        direction_point = DrawBillard.appliquer_homographie(queue.origine_point, homographie)

        # on trace la ligne entre ces deux points
        canvas.create_line(blue_point.x,
                           blue_point.y,
                           direction_point.x,
                           direction_point.y,
                           fill="red", tags=DrawBillard.TAGS_TRAJECTOIR, width=10)

        # on récupère la trajectoir calculé de la queue, on lui applique l'homographie et on l'affiche
        point_depart, point_arrivee = queue.trajectoire
        point_depart_convert = DrawBillard.appliquer_homographie(point_depart, homographie)
        point_arrivee_convert = DrawBillard.appliquer_homographie(point_arrivee, homographie)
        if point_arrivee_convert is not None:
            canvas.create_line(point_depart_convert.x,
                               point_depart_convert.y,
                               point_arrivee_convert.x,
                               point_arrivee_convert.y,
                               fill=color, tags=DrawBillard.TAGS_TRAJECTOIR, width=10)

    @staticmethod
    def draw_billard(canvas: tk.Canvas):
        # on converti les 4 coins du billard enregistré dans le singleton lors de la calibration, on leurs applique l'homographie
        canvas.delete("billard")
        top_left = SingletonCache().profil.projecteur_billard_coordonnees_top_left
        top_right = SingletonCache().profil.projecteur_billard_coordonnees_top_right
        bot_right = SingletonCache().profil.projecteur_billard_coordonnees_bot_right
        bot_left = SingletonCache().profil.projecteur_billard_coordonnees_bot_left

        # on affiche le polygone formé par les 4 coins
        canvas.create_polygon(top_left.x, top_left.y,
                              top_right.x, top_right.y,
                              bot_right.x, bot_right.y,
                              bot_left.x, bot_left.y,
                              outline="red", fill='', tags="rectangle", width=5)

    @staticmethod
    def trouver_homographie():
        # on créé une matrice à partir des 4 coins du billard dans le plan du projecteur
        matrice_projecteur = [
            (SingletonCache().profil.projecteur_billard_coordonnees_top_left.x,
             SingletonCache().profil.projecteur_billard_coordonnees_top_left.y),
            (SingletonCache().profil.projecteur_billard_coordonnees_top_right.x,
             SingletonCache().profil.projecteur_billard_coordonnees_top_right.y),
            (SingletonCache().profil.projecteur_billard_coordonnees_bot_right.x,
             SingletonCache().profil.projecteur_billard_coordonnees_bot_right.y),
            (SingletonCache().profil.projecteur_billard_coordonnees_bot_left.x,
             SingletonCache().profil.projecteur_billard_coordonnees_bot_left.y)
        ]

        # on créé une matrice à partir des 4 coins du billard dans le plan de la camera
        matrice_camera = [
            (SingletonCache().profil.webcam_billard_coordonnees_top_left.x,
             SingletonCache().profil.webcam_billard_coordonnees_top_left.y),
            (SingletonCache().profil.webcam_billard_coordonnees_top_right.x,
             SingletonCache().profil.webcam_billard_coordonnees_top_right.y),
            (SingletonCache().profil.webcam_billard_coordonnees_bot_right.x,
             SingletonCache().profil.webcam_billard_coordonnees_bot_right.y),
            (SingletonCache().profil.webcam_billard_coordonnees_bot_left.x,
             SingletonCache().profil.webcam_billard_coordonnees_bot_left.y)
        ]

        # on calcul l'homographie via cv2
        homographie, _ = cv2.findHomography(np.float32(matrice_camera), np.float32(matrice_projecteur), method=0)

        return homographie

    @staticmethod
    def appliquer_homographie(point_source: Point, homographie):
        # Convertir le point source en format numpy array
        pt_src = [point_source.x, point_source.y, 1]
        pt_src_array = np.asarray(pt_src)
        # calcul de l'homographie
        pt_transform = np.dot(homographie, pt_src_array)
        # normalisation de la matrice de sortie
        pt_transform = pt_transform / pt_transform[2]

        return Point(pt_transform[0], pt_transform[1])

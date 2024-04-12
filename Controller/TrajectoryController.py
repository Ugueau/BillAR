import math
from typing import List, Tuple
from Controller import BallsController
from Model.Bille import Bille
from Model.Point import Point
from Singleton.SingletonCache import SingletonCache


# retourne un point d'intersection soit une des bille de la liste si il existe une sur la trajectoir soit un point
# sur les bord du billard
def get_intersection_ball_or_billard(origine_point: Point, direction_point: Point, list_balls: List[Bille]) -> Point:
    list_impact_ball: List[Tuple[float, Bille]] = []
    intersection = None
    for ball in list_balls:
        distance = BallsController.distance_impact_with_cue(ball, origine_point, direction_point)
        if distance is not None:
            list_impact_ball.append((distance, ball))

    if len(list_impact_ball) > 0:
        list_impact_ball = sorted(list_impact_ball, key=lambda x: x[0])
        distance, shot_ball = list_impact_ball[0]
        intersection = BallsController.get_intersection_between_line_ball(shot_ball, origine_point, direction_point)
        shot_ball.impact = intersection

    else:
        intersection = find_intersection_with_billard(origine_point, direction_point)

    return intersection


# retoune un Point s'il trouve un point d'interserction entres 2 droites si elle existe sinon retourne None
def find_intersection(p1: Point, p2: Point, p_billard1: Point, p_billard2: Point) -> Point | None:
    # Calculate slopes
    m1 = (p2.y - p1.y) / (p2.x - p1.x) if (p2.x - p1.x) != 0 else float('inf')
    m2 = (p_billard2.y - p_billard1.y) / (p_billard2.x - p_billard1.x) if (p_billard2.x - p_billard1.x) != 0 else float(
        'inf')

    if m1 == m2:
        return None
    if m2 == float('inf'):
        return Point(p_billard1.x, p1.y)
    elif m1 == float('inf'):
        return Point(p1.x, p_billard1.y)
    else:

        # Calculate gaps
        b1 = p1.y - m1 * p1.x
        b2 = p_billard1.y - m2 * p_billard1.x

        # Calculate intersection point
        x_intersect = (b1 - b2) / (m2 - m1)
        y_intersect = m1 * x_intersect + b1

        return Point(x_intersect, y_intersect)


# reourne un point d'intersection entre une droite et le billard
def find_intersection_with_billard(point_origin: Point, point_direction: Point) -> Point:
    billard_top_left = SingletonCache().profil.webcam_billard_coordonnees_top_left
    billard_top_right = SingletonCache().profil.webcam_billard_coordonnees_top_right
    billard_bottom_left = SingletonCache().profil.webcam_billard_coordonnees_bot_left
    billard_bottom_right = SingletonCache().profil.webcam_billard_coordonnees_bot_right

    # Décomposer le rectangle en segments de bord
    top_segment = (billard_top_left, billard_top_right)
    bot_segment = (billard_bottom_left, billard_bottom_right)
    left_segment = (billard_top_left, billard_bottom_left)
    right_segment = (billard_top_right, billard_bottom_right)

    # Vérifier les intersections avec chaque segment de bord
    segments = [top_segment, bot_segment, left_segment, right_segment]
    intersections = []
    for segment in segments:
        intersection = find_intersection(point_origin, point_direction, segment[0], segment[1])
        if intersection is not None:
            intersections.append(intersection)

    best_point = point_in_direction(point_origin, point_direction, intersections)
    if best_point is None:
        return intersections[0]
    return best_point


def point_in_direction(point_origin: Point, point_direction: Point, intersections: List[Point]) -> Point | None:
    # Vecteur direction
    vx, vy = (point_direction.x - point_origin.x, point_direction.y - point_origin.y)

    # Liste pour stocker les points dans la même direction
    points_same_direction = []

    for point in intersections:
        px, py = (point.x - point_direction.x, point.y - point_direction.y)

        # Vérifie si le point est dans la même direction que le vecteur
        if vx * px >= 0 and vy * py > 0:
            points_same_direction.append(point)
        elif vx * px > 0 and vy * py >= 0:
            points_same_direction.append(point)
        elif vx == px == 0 and vy * py > 0:
            points_same_direction.append(point)
        elif vx * px > 0 and vy == py == 0:
            points_same_direction.append(point)

    if len(points_same_direction) != 0:
        # Trouver le point le plus proche parmi les points dans la même direction
        closest_point = min(points_same_direction, key=lambda p: get_distance(point_direction, p))
        return closest_point
    return None


def normalize_vector(x, y):
    norm = math.sqrt(x ** 2 + y ** 2)
    if norm == 0:
        return (0, 0)  # Pour éviter une division par zéro si le vecteur est nul
    else:
        return (x / norm, y / norm)


# Fonction pour calculer la distance euclidienne entre deux points
def get_distance(point1: Point, point2: Point) -> float:
    return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)

from Controller import TrajectoryController
from Model.Point import Point
from Model.Bille import Bille
from typing import List, Tuple
import math

def distance_impact_with_cue(ball: Bille,  origine_point:Point, direction_point:Point)-> float | None:
    discriminant = get_discriminant_intersection_between_line_ball(ball, origine_point,direction_point)

    if discriminant < 0:
        return None
    distance = TrajectoryController.get_distance(ball.center,direction_point)
    return distance
def get_trajectory_ball(ball: Bille, list_balls:List[Bille]) -> List[Tuple[Point, Point]]:
    intersection = ball.impact

    if intersection is None:
        return []

    opposite_intersation = get_opposite_intersation_ball(ball, intersection)

    interation_with_ball_or_billard = TrajectoryController.get_intersection_ball_or_billard(intersection, opposite_intersation, list_balls)

    if interation_with_ball_or_billard is None:
        return []

    return [(opposite_intersation, interation_with_ball_or_billard)]

def get_intersection_between_line_ball(ball: Bille, origine_point:Point, direction_point:Point) -> Point | None:

    ball_in_direction = TrajectoryController.point_in_direction(origine_point, direction_point, [ball.center])

    if ball_in_direction is None:
        return None

    discriminant = get_discriminant_intersection_between_line_ball(ball, origine_point, direction_point)
    if direction_point.x == origine_point.x:
        # La droite est verticale (m = infini)
        x_intersection = direction_point.x

        if discriminant < 0:
            return None
        elif discriminant == 0:
            y_intersection = ball.center.y
            return Point(x_intersection, y_intersection)
        else:
            y1 = ball.center.y + ball.radius
            y2 = ball.center.y - ball.radius
            intersection1 = Point(x_intersection, y1)
            intersection2 = Point(x_intersection, y2)

            distance1 = TrajectoryController.get_distance(direction_point, intersection1)
            distance2 = TrajectoryController.get_distance(direction_point, intersection2)

            if distance1 < distance2:
                return intersection1
            else:
                return intersection2

    else:
        # La droite n'est pas verticale
        m = (direction_point.y - origine_point.y) / (
                direction_point.x - origine_point.x)  # Pente de la droite
        b = origine_point.y - m * origine_point.x  # Ordonnée à l'origine

        # Calculer les coefficients du polynôme quadratique pour trouver les intersections
        A = m ** 2 + 1
        B = 2 * (m * b - m * ball.center.y - ball.center.x)

        # S'il n'y a pas d'intersection, retourner None
        if discriminant < 0:
            return None
        elif discriminant == 0:
            # Il y a une seule intersection
            x_intersection = -B / (2 * A)
            y_intersection = m * x_intersection + b

            intersection = Point(x_intersection, y_intersection)
            return intersection

        # Calculer les coordonnées x des intersections
        x1 = (-B + math.sqrt(discriminant)) / (2 * A)
        x2 = (-B - math.sqrt(discriminant)) / (2 * A)

        # Calculer les coordonnées y des intersections
        y1 = m * x1 + b
        y2 = m * x2 + b

        # Créer les points d'intersection
        intersection1 = Point(x1, y1)
        intersection2 = Point(x2, y2)

        distance1 = TrajectoryController.get_distance(direction_point, intersection1)
        distance2 = TrajectoryController.get_distance(direction_point, intersection2)

        if distance1 < distance2:
            return intersection1
        else:
            return intersection2




def get_opposite_intersation_ball(ball: Bille, intersection: Point) -> Point:
    x_oppose = 2 * ball.center.x - intersection.x
    y_oppose = 2 * ball.center.y - intersection.y
    return Point(x_oppose, y_oppose)

def get_discriminant_intersection_between_line_ball(ball: Bille, origine_point:Point, direction_point:Point) -> float:
    ball_in_direction = TrajectoryController.point_in_direction(origine_point, direction_point, [ball.center])

    if ball_in_direction is None:
        return -1

    if direction_point.x == origine_point.x:
        # La droite est verticale (m = infini)
        x_intersection = direction_point.x
        discriminant = ball.radius ** 2 - (x_intersection - ball.center.x) ** 2
        return discriminant
    else:
        # La droite n'est pas verticale
        m = (direction_point.y - origine_point.y) / (
                direction_point.x - origine_point.x)  # Pente de la droite
        b = origine_point.y - m * origine_point.x  # Ordonnée à l'origine

        # Calculer les coefficients du polynôme quadratique pour trouver les intersections
        A = m ** 2 + 1
        B = 2 * (m * b - m * ball.center.y - ball.center.x)
        C = ball.center.x ** 2 + (b - ball.center.y) ** 2 - ball.radius ** 2

        # Calculer le discriminant
        discriminant = B ** 2 - 4 * A * C
        return discriminant
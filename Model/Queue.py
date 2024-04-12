from enum import Enum
from typing import Tuple
from Model.Point import Point

class ImageCorner(Enum):
    TOP_LEFT = 0
    TOP = 1
    TOP_RIGHT = 2
    RIGHT = 3
    BOTTOM_RIGHT = 4
    BOTTOM = 5
    BOTTOM_LEFT = 6
    LEFT = 7

class Queue:
    def __init__(self, blue_point: Point, origine_point: Point, orientation: ImageCorner):
        self._blue_point = blue_point
        self._origine_point = origine_point
        self._orientation = orientation
        self._trajectoire = Tuple[Point, Point]

    @property
    def blue_point(self) -> Point:
        return self._blue_point

    @blue_point.setter
    def blue_point(self, blue_point: Point) -> None:
        if not isinstance(blue_point, Point):
            raise ValueError("Le blue_point doit être un Point.")
        self._blue_point = blue_point

    @property
    def origine_point(self) -> Point:
        return self._origine_point

    @origine_point.setter
    def origine_point(self, origine_point: Point) -> None:
        if not isinstance(origine_point, Point):
            raise ValueError("Le origine_point doit être un Point.")
        self._origine_point = origine_point

    @property
    def orientation(self) -> ImageCorner:
        return self._orientation

    @orientation.setter
    def orientation(self, orientation: ImageCorner):
        self._orientation = orientation

    @property
    def trajectoire(self) -> Tuple[Point,Point]:
        return self._trajectoire

    @trajectoire.setter
    def trajectoire(self, trajectoire: Tuple[Point, Point]) -> None:
        if not isinstance(trajectoire, Tuple):
            raise ValueError("La trajectoire doit être un tuple.")
        self._trajectoire = trajectoire

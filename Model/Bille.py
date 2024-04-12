from Model.Point import Point
from typing import List, Tuple

class Bille:
    def __init__(self,center:Point, radius:float):
        self._center = center
        self._radius = radius
        self._trajectoire = []
        self._impact = None

    @property
    def impact(self) -> Point | None:
        return self._impact

    @impact.setter
    def impact(self, impact: Point) -> None:
        if not isinstance(impact, Point):
            raise ValueError("Le center doit être un Point.")
        self._impact = impact
    @property
    def center(self) -> Point:
        return self._center

    @center.setter
    def center(self, center: Point) -> None:
        if not isinstance(center, Point):
            raise ValueError("Le center doit être un Point.")
        self._center = center
    @property
    def radius(self) -> float:
        return self._radius

    @radius.setter
    def radius(self, radius: float) -> None:
        if not isinstance(radius, float):
            raise ValueError("Le radius doit être un float.")
        self._radius = radius
    @property
    def trajectoire(self) -> List[Tuple[Point, Point]]:
        return self._trajectoire

    @trajectoire.setter
    def trajectoire(self, trajectoire: List[Tuple[Point, Point]]) -> None:
        if not isinstance(trajectoire, List):
            raise ValueError("Le trajectoire doit être un List[].")
        self._trajectoire = trajectoire
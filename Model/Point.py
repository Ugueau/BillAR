class Point:
    def __init__(self, x: float, y: float):
        self._x = x
        self._y = y
    def get_tuple(self):
        return (self._x, self._y)

    @property
    def x(self) -> float:
        return self._x

    @x.setter
    def x(self, x: float | int) -> None:
        if isinstance(x, int):
            x=float(x)
        if not isinstance(x, float):
            raise ValueError("Le x doit être un float.")
        self._x = x

    @property
    def y(self) -> float:
        return self._y

    @y.setter
    def y(self, y: float | int) -> None:
        if isinstance(y, int):
            y=float(y)
        if not isinstance(y, float):
            raise ValueError("Le y doit être un float.")
        self._y = y

    def afficher_profil(self):
        print(f"x : {self.x}")
        print(f"y : {self.y}")
    def to_json(self):
        return {'x': self.x, 'y': self.y}

    @classmethod
    def from_json(cls, data):
        return cls(float(data['x']), float(data['y']))
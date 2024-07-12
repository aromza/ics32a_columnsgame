# project5_model.py

class SpotsState:
    pass

class Jewel:
    def __init__ (self, point: (int, int), length: int):
        self._point_x, self._point_y = point
        self._length = length

    def point (self) -> (int, int):
        return (self._point_x, self._point_y)

    def length (self) -> int:
        return self._length

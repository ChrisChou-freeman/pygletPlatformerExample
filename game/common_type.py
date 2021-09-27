from typing import NamedTuple

class Point(NamedTuple):
    x: int
    y: int

class FPoint(NamedTuple):
    x: float
    y: float

class RGBAColor(NamedTuple):
    r: int
    g: int
    b: int
    a: int

class Rectangle(NamedTuple):
    x: int
    y: int
    width: int
    height: int


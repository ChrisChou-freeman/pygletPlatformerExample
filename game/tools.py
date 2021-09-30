from pyglet.shapes import Rectangle

from .common_type import Point


def rec_contain_poi(rec: Rectangle, poi: Point) -> bool:
    return poi.x >= rec.x \
            and poi.y >= rec.y\
            and poi.x <= rec.x + rec.width\
            and poi.y <= rec.y + rec.height

from typing import Callable

from pyglet.image import Texture
from pyglet.sprite import Sprite
from pyglet.graphics import Batch, OrderedGroup

from .common_type import Rectangle, Point
from .sprite import MySprite as Sprite

class Button(Sprite):
    def __init__(self,
                 img:Texture,
                 x:int,
                 y:int,
                 batch: Batch,
                 group: OrderedGroup):
        super().__init__(img=img, x=x, y=y, batch=batch, group=group)
        self.in_select = False

    def get_rec(self) -> Rectangle:
        return Rectangle(self.x, self.y, self.width, self.height)

    def _on_hover(self, point: Point) -> bool:
        rec = self.get_rec()
        return point.x >= rec.x \
                and point.x <= (rec.x + rec.width) \
                and point.y >= rec.y \
                and point.y <= (rec.y + rec.width)

    def on_click(self, point: Point, call_fuc: Callable) -> None:
        if not self._on_hover(point):
            return
        call_fuc()

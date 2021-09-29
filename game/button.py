from typing import Callable, List

from pyglet.image import Texture
from pyglet.sprite import Sprite
from pyglet.graphics import Batch, OrderedGroup
from pyglet.shapes import Line

from .common_type import Rectangle, Point
from .sprite import MySprite as Sprite
import settings

class Button(Sprite):
    def __init__(self,
                 img:Texture,
                 x:int,
                 y:int,
                 batch: Batch,
                 group: OrderedGroup):
        super().__init__(img=img, x=x, y=y, batch=batch, group=group)
        self.in_select = False
        self.order = group.order
        self.select_box: List[Line] = []

    def get_rec(self) -> Rectangle:
        return Rectangle(self.x, self.y, self.width, self.height)

    def _on_hover(self, point: Point) -> bool:
        rec = self.get_rec()
        return point.x >= rec.x \
                and point.x <= (rec.x + rec.width) \
                and point.y >= rec.y \
                and point.y <= (rec.y + rec.width)

    def _draw_select_box(self) -> None:
        line_width = 2
        self.select_box.append(Line(self.x, self.y, self.x + self.width, self.y, batch=self.batch, group=OrderedGroup(self.order+1), width=line_width, color=settings.COLOR_YELLOW[0:3]))
        self.select_box.append(Line(self.x, self.y, self.x, self.y + self.height, batch=self.batch, group=OrderedGroup(self.order+1), width=line_width, color=settings.COLOR_YELLOW[0:3]))
        self.select_box.append(Line(self.x + self.width, self.y, self.x + self.width, self.y + self.height, batch=self.batch, group=OrderedGroup(self.order+1), width=line_width, color=settings.COLOR_YELLOW[0:3]))
        self.select_box.append(Line(self.x, self.y + self.height, self.x + self.width, self.y + self.height, batch=self.batch, group=OrderedGroup(self.order+1), width=line_width, color=settings.COLOR_YELLOW[0:3]))

    def _clean_line(self):
        self.select_box = []

    def on_click(self, point: Point, call_fuc: Callable) -> bool:
        if not self._on_hover(point):
            return False
        call_fuc()
        return True

    def update(self) -> None:
        if self.in_select:
            self._draw_select_box()
        else:
            self._clean_line()

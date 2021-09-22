from pyglet import text, graphics
from pyglet.graphics import OrderedGroup

from .common_type import Point
import settings

class Menu(text.Label):
    def __init__(self, text: str, position: Point, font_size: float, batch: graphics.Batch, group: OrderedGroup):
        super().__init__(text=text, font_name=None, x=position.x, y=position.y, font_size=font_size, color=settings.COLOR_WHITE, batch=batch, group=group)
        self.in_select = False

    def on_hover(self, point: Point) -> bool:
        return point.x >= self.x and point.x <= (self.x + self.content_width) and point.y >= self.y and point.y <= (self.y + self.content_height)

    def update(self) -> None:
        if self.in_select:
            self.color = settings.COLOR_YELLOW
        else:
            self.color = settings.COLOR_WHITE

    def on_selected(self) -> None:
        if self.in_select:
            settings.game_model = self.text

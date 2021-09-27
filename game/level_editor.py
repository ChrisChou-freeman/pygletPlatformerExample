import os
from typing import List, Union

from pyglet.graphics import OrderedGroup
from pyglet import resource, shapes

from .game_manager import GameManager
from .key_map import key_left, key_right, key_back, mouse_left
from .button import Button
from .sprite import MySprite as Sprite
from .common_type import Point
import settings

class LevelEditor(GameManager):
    def __init__(self):
        self.current_level = 0
        self.layer_number = 4
        self.layer_repeat = 2
        self.contaner_height = 200
        self.scroll_speed = 2
        self.surface_layer_width = 0
        self.layer_list: List[Sprite] = []
        self.key_hold: List[int] = []
        self.tile_btn_list: List[Button] = []
        self.game_start_path = 'content/gamestart'
        self.btn_path = 'content/button'
        self.tiles_path = 'content/tiles'
        self.open_tile_btn: Union[Button, None] = None
        self.btn_container: Union[shapes.Rectangle, None] = None
        self.map_group = OrderedGroup(self.layer_number)
        self.ui_group = OrderedGroup(self.layer_number + 1)
        self.ui_group2 = OrderedGroup(self.layer_number + 2)
        super().__init__()

    def _load_layers(self) -> None:
        for i in range(self.layer_repeat):
            for j in range(self.layer_number):
                img = resource.image(f'layer{j}_{self.current_level}.png')
                self.layer_list.append(
                    Sprite(
                        img=img,
                        batch=self.batch,
                        x=i*img.width*settings.GLOBAL_SCALE,
                        group=OrderedGroup(j)))

                if j == self.layer_number -1:
                    self.surface_layer_width = img.width

    def _load_container(self) -> None:
        self.btn_container = shapes.Rectangle(
                x=0,
                y=settings.SCREEN_HEIGHT - self.contaner_height,
                width=settings.SCREEN_WIDTH,
                height=self.contaner_height,
                batch=self.batch,
                group=self.ui_group,
                color=settings.COLOR_GREY[0:3])
        self.btn_container.visible = False

    def _load_tile_menu(self) -> None:
        tils_name = os.listdir(self.tiles_path)

    def _load_button(self) -> None:
        open_tile_img = resource.image('tileMenu.png')
        self.open_tile_btn = Button(
            open_tile_img,
            x=20,
            y=settings.SCREEN_HEIGHT - 70,
            batch=self.batch,
            group=self.ui_group)

    def _open_tile_container(self):
        if self.btn_container == None or self.open_tile_btn == None:
            return
        self.btn_container.visible = True if not self.btn_container.visible else False
        if self.btn_container.visible:
            self.open_tile_btn.y -= self.contaner_height
        else:
            self.open_tile_btn.y += self.contaner_height

    def load_content(self) -> None:
        resource.path = [self.game_start_path, self.btn_path]
        resource.reindex()
        self._load_layers()
        self._load_button()
        self._load_container()
        self._load_tile_menu()

    def _handle_scroll(self, direction: str) -> None:
        border_left = self.layer_list[self.layer_number-1].x >= 0
        last_layer = self.layer_list[len(self.layer_list)-1]
        border_right = last_layer.x + last_layer.width <= settings.SCREEN_WIDTH
        if direction == 'left' and border_left:
            return
        elif direction == 'right' and border_right:
            return

        for i in range(self.layer_repeat):
            for j in range(self.layer_number):
                index = i * self.layer_number + j
                layer = self.layer_list[index]
                scroll_speed = int(self.scroll_speed * (j + 1))
                if direction == 'left':
                    layer.x += scroll_speed
                else:
                    layer.x -= scroll_speed

    def on_mouse_motion(self, x:int, y:int) -> None:
        pass

    def on_mouse_press(self, x: int, y: int, mouse_key: int) -> None:
        if mouse_left(mouse_key) and self.open_tile_btn != None:
            self.open_tile_btn.on_click(Point(x, y), self._open_tile_container)

    def on_key_press(self, key: int) -> None:
        if key_left(key) or key_right(key):
            self.key_hold.append(key)

        if key_back(key):
            settings.game_model = "main"

    def on_key_release(self, key: int) -> None:
        if key_left(key) or key_right(key):
            self.key_hold.remove(key)

    def update(self, _) -> None:
        for k in self.key_hold:
            if key_left(k):
                self._handle_scroll('left')

            elif key_right(k):
                self._handle_scroll('right')

    def dispose(self) -> None:
        if self.open_tile_btn != None:
            self.open_tile_btn.delete()
        for s in self.layer_list:
            s.delete()


from typing import List, Union

from pyglet.graphics import OrderedGroup
from pyglet import resource

from .game_manager import GameManager
from .key_map import key_left, key_right, key_back
from .button import Button
from .sprite import MySprite as Sprite
import settings

class LevelEditor(GameManager):
    def __init__(self):
        self.current_level = 0
        self.layer_number = 4
        self.layer_repeat = 2
        self.layer_list: List[Sprite] = []
        self.game_start_path = 'content/gamestart'
        self.btn_path = 'content/button'
        self.key_hold: List[int] = []
        self.scroll_speed = 2
        self.surface_layer_width = 0
        self.open_tile_btn: Union[Button, None] = None
        self.btn_contaner: int
        super().__init__()

    def load_layers(self) -> None:
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

    def load_button(self):
        open_tile_img = resource.image('tileMenu.png')
        self.open_tile_btn = Button(
            open_tile_img,
            x=20,
            y=settings.SCREEN_HEIGHT - 50,
            batch=self.batch,
            group=OrderedGroup(self.layer_number))

    def load_content(self) -> None:
        resource.path = [self.game_start_path, self.btn_path]
        resource.reindex()
        self.load_layers()
        self.load_button()

    def on_mouse_motion(self, x:int, y:int) -> None:
        pass

    def on_mouse_press(self, x: int, y: int, mouse_key: int) -> None:
        pass

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
                if self.layer_list[self.layer_number-1].x >= 0:
                    break
                for i in range(self.layer_repeat):
                    for j in range(self.layer_number):
                        index = i * self.layer_number + j
                        layer = self.layer_list[index]
                        layer.x += int(self.scroll_speed * (j+1))

            elif key_right(k):
                last_layer = self.layer_list[len(self.layer_list)-1]
                if last_layer.x + last_layer.width <= settings.SCREEN_WIDTH:
                    break
                for i in range(self.layer_repeat):
                    for j in range(self.layer_number):
                        index = i * self.layer_number + j
                        layer = self.layer_list[index]
                        layer.x -= int(self.scroll_speed * (j+1))

    def dispose(self) -> None:
        if self.open_tile_btn != None:
            self.open_tile_btn.delete()
        for s in self.layer_list:
            s.delete()

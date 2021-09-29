from typing import List

from pyglet.graphics import OrderedGroup
from pyglet.window import mouse
from pyglet import resource

from .key_map import key_up, key_down, key_enter
from .game_manager import GameManager
from .common_type import Point
from .menu import Menu
from .sprite import MySprite as Sprite
import settings

class GameMain(GameManager):
    def __init__(self):
        self.sprite_list: List[Sprite] = []
        self.menu_list: List[Menu] = []
        self.menu_texts = ['Exit', 'Development', 'Game Start']
        self.content_path = 'content/main'
        self.menu_start = int(settings.SCREEN_HEIGHT/4)
        self.menu_index = len(self.menu_texts) - 1
        self.menu_gap = 50
        self.cloud_speed = 5
        self.layer_number = 5
        self.clou_number = 3
        super().__init__()

    def load_layers(self) -> None:
        for i in range(self.layer_number):
            self.sprite_list.append(
                Sprite(
                    img=resource.image(f'layer{i}.png'),
                    batch=self.batch,
                    group=OrderedGroup(i)))

    def load_cloud(self) -> None:
        for i in range(self.clou_number):
            self.sprite_list.append(
                Sprite(
                    img=resource.image(f'cloudAnimation{i}.png'),
                    batch=self.batch,
                    group=OrderedGroup(self.layer_number)))

    def load_menu(self) -> None:
        for index, menu_name in enumerate(self.menu_texts):
            self.menu_list.append(
                Menu(
                    menu_name,
                    Point(20, self.menu_start + index * self.menu_gap),
                    25 * settings.GLOBAL_SCALE,
                    self.batch,
                    OrderedGroup(6)))

    def load_content(self) -> None:
        resource.path = [self.content_path]
        resource.reindex()
        self.load_layers()
        self.load_cloud()
        self.load_menu()

    def on_mouse_motion(self, x: int, y: int) -> None:
        for index, menu in enumerate(self.menu_list):
            if menu.on_hover(Point(x, y)):
                menu.in_select = True
                self.menu_index = index
            else:
                menu.in_select = False

    def on_mouse_press(self, x: int, y: int, button: int) -> None:
        mouse_left = True if button == mouse.LEFT else False
        for menu in self.menu_list:
            if menu.on_hover(Point(x, y)) and mouse_left:
                menu.on_selected()

    def on_mouse_release(self, *_) -> None:
        pass

    def on_key_press(self, key: int) -> None:
        if key_up(key):
            self.menu_index += 1
            if self.menu_index > len(self.menu_list) - 1:
                self.menu_index = 0

        elif key_down(key):
            self.menu_index -= 1
            if self.menu_index < 0:
                self.menu_index = len(self.menu_list) -1

        elif key_enter(key):
            for menu in self.menu_list:
                menu.on_selected()

    def on_key_release(self, _) -> None:
        pass

    def update(self, dt: float) -> None:
        speed = dt*self.cloud_speed
        for i in range(5, len(self.sprite_list)):
            s = self.sprite_list[i]
            s.x += speed
            speed += dt*self.cloud_speed
            if s.x >= settings.SCREEN_WIDTH:
                s.x = -settings.SCREEN_WIDTH

        for index, menu in enumerate(self.menu_list):
            if index == self.menu_index:
                menu.in_select = True
            else:
                menu.in_select = False
            menu.update()

    def dispose(self):
        for s in self.sprite_list:
            s.delete()


import os
from typing import List, Union

from pyglet.graphics import OrderedGroup
from pyglet.image import Texture
from pyglet import resource, shapes

from . import key_map
from .game_manager import GameManager
from .button import Button
from .sprite import MySprite as Sprite
from .common_type import Point
import settings

class LevelEditor(GameManager):
    def __init__(self):
        self.current_level = 0
        self.layer_number = 4
        self.layer_repeat = 2
        self.contaner_height = 150
        self.scroll_speed = 2
        self.surface_layer_width = 0
        self.layer_list: List[Sprite] = []
        self.tile_btn_list: List[Button] = []
        self.key_hold: List[int] = []
        self.mouse_key_hold: List[int] =[]
        self.grid_line_list: List[shapes.Line] = []
        self.game_start_path = 'content/gamestart'
        self.btn_path = 'content/button'
        self.tiles_path = 'content/tiles'
        self.open_tile_btn: Union[Button, None] = None
        self.btn_container: Union[shapes.Rectangle, None] = None
        self.map_group = OrderedGroup(self.layer_number)
        self.ui_group = OrderedGroup(self.layer_number + 1)
        self.ui_group2 = OrderedGroup(self.layer_number + 2)
        self.in_select_tile = 0
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
        tile_border = 15
        tiles_name = os.listdir(self.tiles_path)
        col_num = 0
        row_num = 0
        cols = settings.SCREEN_OR_WIDTH // (settings.TILE_WIDTH + tile_border)

        for tile in tiles_name:
            tile_image = resource.image(tile)
            tile_x = col_num * (settings.TILE_WIDTH + tile_border)
            tile_y = settings.SCREEN_OR_HEIGHT - (row_num * (tile_image.height + tile_border) + tile_image.height)
            tile_y *= settings.GLOBAL_SCALE
            tile_x *= settings.GLOBAL_SCALE
            btn_obj = Button(
                tile_image,
                x=int(tile_x),
                y=int(tile_y),
                batch=self.batch,
                group=self.ui_group2)
            btn_obj.visible = False
            self.tile_btn_list.append(btn_obj)
            col_num += 1
            if col_num == cols:
                row_num += 1
                col_num = 0

    def _load_button(self) -> None:
        open_tile_img: Texture = resource.image('tileMenu.png')
        self.open_tile_btn = Button(
            open_tile_img,
            x=20,
            y=settings.SCREEN_HEIGHT - 70,
            batch=self.batch,
            group=self.ui_group)

    def _show_tile_menu(self, show: bool) -> None:
        for tile in self.tile_btn_list:
            tile.visible = show

    def _open_tile_container(self):
        if self.btn_container == None or self.open_tile_btn == None:
            return
        self.btn_container.visible = True if not self.btn_container.visible else False
        if self.btn_container.visible:
            self.open_tile_btn.y -= self.contaner_height
        else:
            self.open_tile_btn.y += self.contaner_height
        self._show_tile_menu(self.btn_container.visible)

    def _load_grid(self) -> None:
        scroll_length = self.layer_list[-1].width * self.layer_repeat
        for ypos in range(0, settings.SCREEN_HEIGHT, settings.TILE_HEIGHT):
            new_line = shapes.Line(0, ypos, scroll_length, ypos, batch=self.batch, group=self.map_group)
            new_line.visible = False
            self.grid_line_list.append(new_line)

        for xpox in range(0, scroll_length, settings.TILE_WIDTH):
            new_line = shapes.Line(xpox, 0, xpox, settings.SCREEN_HEIGHT, batch=self.batch, group=self.map_group)
            new_line.visible = False
            self.grid_line_list.append(new_line)

    def load_content(self) -> None:
        resource.path = [self.game_start_path, self.btn_path, self.tiles_path]
        resource.reindex()
        self._load_layers()
        self._load_button()
        self._load_container()
        self._load_tile_menu()
        self._load_grid()

    def _handle_scroll(self, direction: str) -> None:
        border_left = self.layer_list[self.layer_number-1].x >= 0
        last_layer = self.layer_list[len(self.layer_list)-1]
        border_right = last_layer.x + last_layer.width <= settings.SCREEN_WIDTH
        if direction == 'left' and border_left:
            return
        elif direction == 'right' and border_right:
            return

        surface_layer_scroll_speed = 0
        for i in range(self.layer_repeat):
            for j in range(self.layer_number):
                index = i * self.layer_number + j
                layer = self.layer_list[index]
                scroll_speed = int(self.scroll_speed * (j + 1))
                if direction == 'left':
                    layer.x += scroll_speed
                else:
                    layer.x -= scroll_speed
                if j == self.layer_number -1:
                    surface_layer_scroll_speed = scroll_speed

        for l in self.grid_line_list:
            if direction == 'left':
                l.x += surface_layer_scroll_speed
                l.x2 += surface_layer_scroll_speed
            else:
                l.x -= surface_layer_scroll_speed
                l.x2 -= surface_layer_scroll_speed

    def _show_grid(self) -> None:
        for l in self.grid_line_list:
            l.visible = True if not l.visible else False

    def on_mouse_motion(self, *_) -> None:
        pass

    def on_mouse_press(self, x: int, y: int, mouse_key: int) -> None:
        if key_map.mouse_left(mouse_key):
            if self.open_tile_btn != None:
                ev = self.open_tile_btn.on_click(Point(x, y), self._open_tile_container)
                if ev:
                    return

            for index, button in enumerate(self.tile_btn_list):
                if button._on_hover(Point(x, y)):
                    self.in_select_tile = index

            self.mouse_key_hold.append(mouse_key)

    def on_mouse_release(self, *args) -> None:
        mouse_key = args[-1]
        if mouse_key in self.mouse_key_hold:
            self.mouse_key_hold.remove(mouse_key)

    def on_key_press(self, key: int) -> None:
        if key_map.key_left(key) or key_map.key_right(key):
            self.key_hold.append(key)

        if key_map.key_back(key):
            settings.game_model = "main"

        if key_map.key_grid(key):
            self._show_grid()

    def on_key_release(self, key: int) -> None:
        if key in self.key_hold:
            self.key_hold.remove(key)

    def update(self, _) -> None:
        for k in self.key_hold:
            if key_map.key_left(k):
                self._handle_scroll('left')

            elif key_map.key_right(k):
                self._handle_scroll('right')

        for index, button in enumerate(self.tile_btn_list):
            if index == self.in_select_tile \
                    and self.btn_container != None \
                    and self.btn_container.visible:
                button.in_select = True
            else:
                button.in_select = False
            button.update()

    def dispose(self) -> None:
        if self.open_tile_btn != None:
            self.open_tile_btn.delete()

        for s in self.layer_list:
            s.delete()

        for btn in self.tile_btn_list:
            btn.delete()


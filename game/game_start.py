import json
from typing import Dict, List

from pyglet import resource
from pyglet.graphics import OrderedGroup

from .sprite import MySprite as Sprite

from .game_manager import GameManager

class GameStart(GameManager):
    def __init__(self):
        self.level_data_path = 'content/leveldata'
        self.tiles_path = 'content/tiles'
        self.layer_path = 'content/gamestart'
        self.curren_level = 0
        self.layer_number = 4
        self.layer_repeat = 2
        self.layer_sprits: List[Sprite] = []
        self.tile_data: List[Dict[str, int]] = []
        self.collistion_data: Dict[str, List[int]] = {}
        self.level_info: Dict[str, int] = {}
        self.tile_sprits: List[Sprite] = []
        super().__init__()

    def load_layers(self) -> None:
        for i in range(self.layer_number):
            layer_image = resource.image(f'layer{i}_{self.curren_level}.png')
            self.layer_sprits.append(
                Sprite(
                    layer_image,
                    batch=self.batch,
                    group=OrderedGroup(i)))


    def load_tiles(self) -> None:
        for tile in self.tile_data:
            tile_num = tile['tile']
            if tile_num == -1:
                continue
            tile_image = resource.image(f'{tile_num}.png')
            self.tile_sprits.append(
                Sprite(
                    tile_image,
                    x=tile['X'],
                    y=480-tile['Y']-32,
                    batch=self.batch,
                    group=OrderedGroup(self.layer_number)))

    def load_level_data(self) -> None:
        level_json = resource.text(f'{self.curren_level}.json')
        json_obj = json.loads(level_json.text)
        self.tile_data = json_obj["TileData"]
        self.collistion_data = json_obj["CollisionData"]
        self.level_info = json_obj["LevelInfo"]


    def load_content(self) -> None:
        resource.path = [self.level_data_path, self.tiles_path, self.layer_path]
        resource.reindex()
        self.load_level_data()
        self.load_tiles()
        self.load_layers()

    def on_mouse_motion(self, *_) -> None:
        pass

    def on_mouse_press(self, x: int, y: int, button: int) -> None:
        pass

    def on_key_press(self, key: int) -> None:
        pass

    def on_key_release(self, key: int) -> None:
        pass

    def update(self, df: float) -> None:
        pass

    def dispose(self) -> None:
        pass

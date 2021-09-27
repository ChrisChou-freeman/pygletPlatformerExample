import sys

from pyglet import clock, app, gl
from pyglet.window import mouse, Window
from pyglet.image import Texture

from game import GameMain, LevelEditor
import settings

class Game(Window):
    def __init__(self, width: int, height: int, caption: str):
        super().__init__(width=width, height=height, caption=caption)
        self._set_graphics()
        self.game_manager = {
            'main': GameMain,
            'Development': LevelEditor,
            # 'Game Start': GameStart
        }
        self.game_model = self.game_manager[settings.game_model]()
        self.mouse = mouse

    def _set_graphics(self):
        Texture.default_mag_filter = gl.GL_NEAREST

    def on_mouse_motion(self, x: int, y: int, *_) -> None:
        self.game_model.on_mouse_motion(x, y)

    def on_mouse_press(self, x: int, y: int, button: int, _) -> None:
        self.game_model.on_mouse_press(x, y, button)

    def on_key_press(self, key: int, _) -> None:
        self.game_model.on_key_press(key)

    def on_key_release(self, key: int, _) -> None:
        self.game_model.on_key_release(key)

    def on_draw(self) -> None:
        self.clear()
        self.game_model.draw()

    def update(self, dt: float) -> None:
        if settings.game_model == 'Exit':
            sys.exit(1)
        if self.game_manager.get(settings.game_model) != None \
                and not isinstance(self.game_model, self.game_manager[settings.game_model]):
            self.game_model.dispose()
            self.game_model = self.game_manager[settings.game_model]()
        self.game_model.update(dt)

    def run(self) -> None:
        clock.schedule_interval(self.update, settings.FPS_LIMIT)
        app.run()

if __name__ == '__main__':
    game = Game(
            settings.SCREEN_WIDTH,
            settings.SCREEN_HEIGHT,
            settings.GAME_NAME)
    game.run()


from abc import ABC, abstractmethod

from pyglet import graphics

class GameManager(ABC):
    def __init__(self):
        self.batch = graphics.Batch()
        self.load_content()

    @abstractmethod
    def load_content(self) -> None:
        pass

    @abstractmethod
    def on_mouse_motion(self, x: int, y: int) -> None:
        pass

    @abstractmethod
    def on_mouse_press(self, x: int, y: int, button: int) -> None:
        pass

    @abstractmethod
    def on_key_press(self, key: int) -> None:
        pass

    @abstractmethod
    def on_key_release(self, key: int) -> None:
        pass

    @abstractmethod
    def update(self, dt: float) -> None:
        pass

    def draw(self) -> None:
        self.batch.draw()

    @abstractmethod
    def dispose(self) -> None:
        pass

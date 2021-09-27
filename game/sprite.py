from pyglet.sprite import Sprite
from pyglet.image import Texture
from pyglet.graphics import Batch, OrderedGroup

import settings

class MySprite(Sprite):
    def __init__(
            self,
            img: Texture,
            batch: Batch,
            group: OrderedGroup=OrderedGroup(0),
            x: int=0,
            y: int=0):
        super().__init__(img=img, x=x, y=y, batch=batch, group=group)
        self.scale = settings.GLOBAL_SCALE

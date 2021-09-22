from pyglet.window import key


def key_up(input_key: int) -> bool:
    return input_key == key.W or input_key == key.UP

def key_down(input_key: int) -> bool:
    return input_key == key.S or input_key == key.DOWN

def key_left(input_key: int) -> bool:
    return input_key == key.A or input_key == key.LEFT

def key_right(input_key: int) -> bool:
    return input_key == key.D or input_key == key.RIGHT

def key_enter(input_key: int) -> bool:
    return input_key == key.ENTER

def key_back(input_key: int) -> bool:
    return input_key == key.ESCAPE

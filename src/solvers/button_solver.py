from enum import Enum
from debug import log
from features.button import get_button_features, get_strip_color

def solve(img, features, model):
    """
    Extracts features about a button from an image of it,
    and returns whether to hold down, or press the button.
    """
    text, color = get_button_features(img, model)
    log(f"Button text: {text}, color: {color}")

    Color = Enum("Colors", {"White":0, "Yellow":1, "Blue":2, "Red":3})
    if color == Color.Blue.value and text == "Abort":
        return True
    if features["batteries"] > 1 and text == "Detonate":
        return False
    if color == Color.White.value and "lit_car" in features["indicators"]:
        return True
    if features["batteries"] > 2 and "lit_frk" in features["indicators"]:
        return False
    if color == Color.Yellow.value:
        return True
    if color == Color.Red.value and text == "Hold":
        return False
    return True

def get_release_time(img, pixel):
    strip_color = get_strip_color(img, pixel)
    Color = Enum("Colors", {"White":0, "Yellow":1, "Blue":2, "Red":3})
    if strip_color == Color.Blue.value:
        return 4
    if strip_color == Color.White.value:
        return 1
    if strip_color == Color.Yellow.value:
        return 5
    return 1
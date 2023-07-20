import pyautogui
import subprocess

def copy(text: str):
    process = subprocess.Popen('clip', stdin=subprocess.PIPE, text=True)
    process.communicate(input=text)

class Picker:
    def __init__(self, save_to_clipboard:bool=True) -> None:
        self.save_to_clipboard=save_to_clipboard

    def pick(self, x, y) -> None:
        color = pyautogui.pixel(x, y)
        color_hex = '#%02x%02x%02x' % color[:3]
        if self.save_to_clipboard:
            copy(color_hex.strip())

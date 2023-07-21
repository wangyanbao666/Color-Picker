import pyautogui
import subprocess

def copy(text: str):
    process = subprocess.Popen('clip', stdin=subprocess.PIPE, text=True)
    process.communicate(input=text)

class Picker:
    def __init__(self, save_to_clipboard:bool=True, show_popup:bool=True) -> None:
        self.save_to_clipboard=save_to_clipboard
        self.show_popup=show_popup

    def pick(self, x, y) -> str:
        color = pyautogui.pixel(x, y)
        color_hex = '#%02x%02x%02x' % color[:3]
        if self.save_to_clipboard:
            copy(color_hex.strip())
        return color_hex

import ctypes
from ctypes import *
import ctypes.wintypes
import win32con
import win32api
import asyncio
import threading
from popup import show_color_popup
from picker import Picker
import time

# Constants
WH_KEYBOARD_LL = 13
WH_MOUSE_LL = 14
WM_KEYDOWN = 0x0100
WM_KEYUP = 0x0101
WM_MOUSEMOVE = 0x0200
WM_LBUTTONDOWN = 0x0201
WM_LBUTTONUP = 0x0202
VK_CONTROL = 0x11
VK_MENU = 0x12
VK_S = 0x53

# Global variables
user32 = ctypes.windll.user32
is_color_picker_active = False

# Instantiate the picker class
picker = Picker()


class KBDLLHOOKSTRUCT(ctypes.Structure):
    _fields_ = [
        ('vkCode', ctypes.c_int),
        ('scanCode', ctypes.c_int),
        ('flags', ctypes.c_int),
        ('time', ctypes.c_int),
        ('dwExtraInfo', ctypes.POINTER(ctypes.c_ulonglong)),
    ]

def show_color_popup_after_delay(color):
    show_color_popup(color)

# Define the callback function for keyboard events
def keyboard_event_handler(nCode, wParam, lParam):
    global is_color_picker_active
    if nCode == win32con.HC_ACTION:
        event = wParam

        # Access the KBDLLHOOKSTRUCT structure using contents
        kbd_struct = ctypes.cast(lParam, ctypes.POINTER(KBDLLHOOKSTRUCT)).contents

        # Extract the virtual-key code and key state from the structure
        vk_code = kbd_struct.vkCode
        last_8_bits = vk_code & 0xFF
        
        ctrl_pressed = win32api.GetAsyncKeyState(VK_CONTROL)<0
        alt_pressed = win32api.GetAsyncKeyState(VK_MENU)<0
        if alt_pressed and ctrl_pressed:
            if event == WM_KEYDOWN and last_8_bits == VK_S:
                is_color_picker_active = True
                return -1  # Block the 's' key press event
        else:
            is_color_picker_active = False


        # Check for key release to exit the color picker state
        if event == WM_KEYUP:
            if vk_code == VK_S:
                is_color_picker_active = False


    # Pass the event to the next hook
    return user32.CallNextHookEx(None, nCode, wParam, lParam)

# Define the callback function for mouse events
def mouse_event_handler(nCode, wParam, lParam):
    global is_color_picker_active

    if nCode == win32con.HC_ACTION:
        event = wParam

        # Block mouse events while the color picker is active
        if is_color_picker_active and (event == WM_LBUTTONDOWN):
            # call color picker function
            x, y = win32api.GetCursorPos()
            color = picker.pick(x, y)
            if picker.show_popup:
                threading.Thread(target=show_color_popup_after_delay, args=(color,)).start()
            return -1
    
    # Pass the event to the next hook
    return user32.CallNextHookEx(None, nCode, wParam, lParam)

# Convert the keyboard callback function to a C function
keyboard_callback = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_void_p))(keyboard_event_handler)

# Convert the mouse callback function to a C function
mouse_callback = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_void_p))(mouse_event_handler)

def main():
    # Set the low-level keyboard hook
    keyboard_callback = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_void_p))(keyboard_event_handler)
    keyboard_hook = user32.SetWindowsHookExA(WH_KEYBOARD_LL, keyboard_callback, None, 0)

    # Set the low-level mouse hook
    mouse_callback = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_void_p))(mouse_event_handler)
    mouse_hook = user32.SetWindowsHookExA(WH_MOUSE_LL, mouse_callback, None, 0)

    # Start the message loop
    user32.BlockInput(True)
    msg = ctypes.wintypes.MSG()
    while user32.GetMessageA(ctypes.byref(msg), None, 0, 0) != 0:
        user32.TranslateMessage(ctypes.byref(msg))
        user32.DispatchMessageA(ctypes.byref(msg))

    # Remove the keyboard hook
    user32.BlockInput(False)
    user32.UnhookWindowsHookEx(keyboard_hook)

    # Remove the mouse hook
    user32.UnhookWindowsHookEx(mouse_hook)

if __name__ == "__main__":
    main()
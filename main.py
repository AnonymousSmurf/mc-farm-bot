import ctypes
import time
import pyautogui
from pynput.keyboard import *

SendInput = ctypes.windll.user32.SendInput

#  ======== settings ========
delay = 0.1
resume_key = Key.f4
pause_key = Key.f6
exit_key = Key.f7

pause = True
running = True

def on_press(key):
    global running, pause

    if key == resume_key:
        pause = False 
        print("[Resumed]")
    elif key == pause_key:
        pause = True
        print("[Paused]")
    elif key == exit_key:
        running = False
        print("[Exit]")

def display_controls():
    print("// - Controls:")
    print("\t F4 = Resume")
    print("\t F6 = Pause")
    print("\t F7 = Exit")
    print("-----------------------------------------------------")
    print('Press F4 to start ...')

PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def main():
    lis = Listener(on_press=on_press)
    lis.start()

    display_controls()
    while running:
        if not pause:
         pyautogui.click(pyautogui.position().x, pyautogui.position().y, 1, 0, 'LEFT')
         PressKey(0x02)
         ReleaseKey(0x02)
         pyautogui.click(pyautogui.position().x, pyautogui.position().y, 1, 0, 'RIGHT')
         PressKey(0x03)
         ReleaseKey(0x03)
         pyautogui.click(pyautogui.position().x, pyautogui.position().y, 5, 0, 'RIGHT')
         time.sleep(delay)
    lis.stop()


if __name__ == "__main__":
    main()
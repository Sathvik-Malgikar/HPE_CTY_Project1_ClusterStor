import pyautogui
from time import sleep

def type_into_dialogue_box(FILE_TO_UPLOAD):
    # types into dialogue box
    pyautogui.typewrite(FILE_TO_UPLOAD)
    sleep(1)
    pyautogui.press("enter")
    sleep(3)
    
def zoom_out():
    pyautogui.keyDown("ctrl")
    pyautogui.press("-")
    pyautogui.press("-")
    pyautogui.keyUp("ctrl")
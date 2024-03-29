import pyautogui
from time import sleep

"""
Utility function to type text into a dialogue box in the GUI.

This function types the specified text into the dialogue box and presses 'Enter'.

Parameters:
    FILE_TO_UPLOAD (str): The text to be typed into the dialogue box.

Returns:
    None

Raises:
    None

Usage:
    type_into_dialogue_box(FILE_TO_UPLOAD)
"""

def type_into_dialogue_box(FILE_TO_UPLOAD):
    # types into dialogue box
    pyautogui.typewrite(FILE_TO_UPLOAD)
    sleep(1)
    pyautogui.press("enter")
    sleep(3)

def go_back_esc():
    # types into dialogue box
    pyautogui.press("esc")
    sleep(4)

def press_tab():
    # types into dialogue box
    pyautogui.press("tab")
    sleep(1)
  
def n_tabs_shift_focus(n):
    for i in range(n):
        press_tab()
        sleep(0.4)
            
def press_enter():
    # types into dialogue box
    pyautogui.press("enter")
    sleep(2)
    
def view_shortcut():
    # types into dialogue box
    pyautogui.typewrite("gd")
    sleep(2)

    
    
    
def zoom_out():
    pyautogui.keyDown("ctrl")
    pyautogui.press("-")
    pyautogui.press("-")
    pyautogui.keyUp("ctrl")
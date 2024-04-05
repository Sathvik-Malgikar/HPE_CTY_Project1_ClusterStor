import pyautogui
from time import sleep
import configparser
import time
import os

parser = configparser.ConfigParser()
parser.read("config.ini")
very_small_delay = float(parser.get("Delay Parameters", "very_small_delay"))
small_delay = int(parser.get("Delay Parameters", "small_delay"))
medium_delay = float(parser.get("Delay Parameters", "medium_delay"))
large_delay = int(parser.get("Delay Parameters", "large_delay"))

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

def type_into_dialogue_box(stringvalue):
    # types into dialogue box
    pyautogui.typewrite(stringvalue)
    sleep(small_delay)
    pyautogui.press("enter")
    sleep(medium_delay)

def go_back_esc():
    # types into dialogue box
    pyautogui.press("esc")
    sleep(medium_delay)

def press_tab():
    # types into dialogue box
    pyautogui.press("tab")
    sleep(small_delay)
  
def n_tabs_shift_focus(n):
    sleep(medium_delay)
    for i in range(n):
        press_tab()
        sleep(very_small_delay)
            
def press_enter():
    # types into dialogue box
    pyautogui.press("enter")
    sleep(small_delay)
    
def view_shortcut():
    # types into dialogue box
    pyautogui.typewrite("gd")
    sleep(small_delay)
    
    
def zoom_out():
    pyautogui.keyDown("ctrl")
    pyautogui.press("-")
    pyautogui.press("-")
    pyautogui.keyUp("ctrl")
    
def wait_for_file(path, timeout=None, poll_interval=2):
    start_time = time.time()
    while True:
        if os.path.exists(path):
            return True
        if timeout is not None and time.time() - start_time >= timeout:
            return False
        time.sleep(poll_interval)
import pyautogui
from time import sleep
import configparser
import time
import os

parser = configparser.ConfigParser()
parser.read("infrastructure/config.ini")
very_small_delay = float(parser.get("Delay Parameters", "very_small_delay"))
small_delay = float(parser.get("Delay Parameters", "small_delay"))
medium_delay = float(parser.get("Delay Parameters", "medium_delay"))
large_delay = float(parser.get("Delay Parameters", "large_delay"))


def type_into_dialogue_box(stringvalue: str) -> None:
  """
  Types the specified text into a dialogue box in the GUI and presses 'Enter'.

  Args:
      stringvalue (str): The text to be typed into the dialogue box.

  Returns:
      None
  """
  sleep(small_delay)
  pyautogui.typewrite(stringvalue)
  pyautogui.press("enter")
  sleep(small_delay)


def go_back_esc() -> None:
  """
  Simulates pressing the Escape (Esc) key. Useful for going back in dialogs or menus.
  """
  pyautogui.press("esc")
  sleep(medium_delay)


def press_tab() -> None:
  """
  Simulates pressing the Tab key to move focus between elements in a GUI.
  """
  pyautogui.press("tab")
  sleep(very_small_delay)


def n_tabs_shift_focus(n: int) -> None:
  """
  Simulates pressing the Tab key n times to shift focus between elements in a GUI.

  Args:
      n (int): The number of times to press the Tab key.
  """
  for _ in range(n):
    press_tab()
    sleep(very_small_delay)


def press_space() -> None:
  """
  Simulates pressing the Space bar.
  """
  pyautogui.press("space")
  sleep(small_delay)


def press_enter() -> None:
  """
  Simulates pressing the Enter key.
  """
  pyautogui.press("enter")
  sleep(small_delay)


def view_shortcut() -> None:
  """
  Simulates typing "gd" to potentially view a shortcut menu (specific behavior depends on the application).
  """
  pyautogui.typewrite("gd")
  sleep(small_delay)


def press_down_arrow() -> None:
  """
  Simulates pressing the Down arrow key.
  """
  pyautogui.press("down")
  sleep(small_delay)


def zoom_out() -> None:
  """
  Simulates zooming out by pressing Ctrl + '-' twice.
  """
  pyautogui.keyDown("ctrl")
  pyautogui.press("-")
  pyautogui.press("-")
  pyautogui.keyUp("ctrl")
  sleep(very_small_delay)


def select_all() -> None:
  """
  Simulates pressing Ctrl + A to select all text in the currently focused text area.

  **Assumption:** The cursor is already focused on the text area where you want to select all.
  """
  pyautogui.hotkey("ctrl", "a")  # Presses Ctrl + A to select all text
  sleep(very_small_delay)


def cut_selection() -> None:
  """
  Simulates pressing Ctrl + X to cut the selected text in the currently focused text area.

  **Assumption:** The cursor is already focused on the text area where you want to cut text.
  """
  pyautogui.hotkey("ctrl", "x")  # Presses Ctrl + X to cut selected text
  sleep(very_small_delay)


def copy_selection() -> None:
  """
  Simulates pressing Ctrl + C to copy the selected text in the currently focused text area.

  **Assumption:** The cursor is already focused on the text area where you want to copy text.
  """
  pyautogui.hotkey("ctrl", "c")  # Presses Ctrl + C to copy selected text
  sleep(very_small_delay)


def paste_clipboard() -> None:
  """
  Simulates pressing Ctrl + V to paste the clipboard content in the currently focused text area.

  **Assumption:** The cursor is already focused on the text area where you want to paste text.
  """
  pyautogui.hotkey("ctrl", "v")  # Presses Ctrl


def press_delete() -> None:
  """
  Simulates pressing the Delete key.
  """
  pyautogui.press("delete")  # Presses the "Delete" key
  sleep(small_delay)


def wait_for_file(path: str, timeout: float = None, poll_interval: float = 2) -> bool:
  """
  Waits for a file to exist at the specified path.

  Args:
      path (str): The path to the file.
      timeout (float, optional): The maximum time to wait in seconds. Defaults to None (wait indefinitely).
      poll_interval (float, optional): The time interval between checks in seconds. Defaults to 2.

  Returns:
      bool: True if the file exists within the timeout period, False otherwise.
  """
  start_time = time.time()
  while True:
    if os.path.exists(path):
      return True
    if timeout is not None and time.time() - start_time >= timeout:
      return False
    time.sleep(poll_interval)

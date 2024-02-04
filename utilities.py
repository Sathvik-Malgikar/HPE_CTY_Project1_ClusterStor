import configparser
from time import sleep

import pyautogui
import pytest
from selenium.webdriver import Chrome
from selenium.webdriver.common.action_chains import ActionChains
import selenium.common.exceptions as EXC 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import locators

"""
Utility function to select a file/folder in Google Drive GUI

Parameters:
- driver (WebDriver): The Selenium WebDriver instance.
- action_chain (ActionChains): The Selenium ActionChains instance for performing user actions.
- web_driver_wait (WebDriverWait): The Selenium WebDriverWait instance for waiting on elements.
-file_name: Name of file/folder to be selected

Returns:
None

Raises:
FileNotFoundError: If the file/folder does not exist on Google Drive.

Usage:
select_file(driver, action_chain, web_driver_wait, file_name)
"""

def select_file(driver, action_chain, web_driver_wait,file_name,show_more_needed=True): # show_more_needed is to ensure backwards compatibility

    if(show_more_needed): # old testcases do not have show_more param, so by default True, 
       # newer testcases can explicitly mention if show more button is to be clicked or not before looking for file
            

        web_driver_wait.until(
            EC.presence_of_element_located(
                locators.show_more_files
            ),
        )

        
        show_more_button = driver.find_element(
        *locators.show_more_files
        )
        show_more_button.click()
    
    sleep(5)
        # Find file
    try:
        file_selector = locators.file_selector(file_name)
        web_driver_wait.until(
            EC.presence_of_element_located(
                file_selector
            ),
        )
    except:
        raise FileNotFoundError("File Not found")
    else:
        file_element = driver.find_element(
            *file_selector
        )
        action_chain.move_to_element(file_element).click()
        action_chain.perform()


"""
Utility function to click delete button on a selected file/folder in the Google Drive web GUI.

Parameters:
- driver (WebDriver): The Selenium WebDriver instance.
- action_chain (ActionChains): The Selenium ActionChains instance for performing user actions.
- web_driver_wait (WebDriverWait): The Selenium WebDriverWait instance for waiting on elements.

Returns:
None

Raises:
-

Usage:
delete_file(driver, action_chain, web_driver_wait)
"""

def delete_file(driver,action_chain,web_driver_wait):
    # click on delete button
    web_driver_wait.until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//div[@role='button' and @aria-label='Move to trash' and @aria-hidden='false' and @aria-disabled='false']",
            )
        ),
    )
    delete_button = driver.find_element(
        By.XPATH,
        "//div[@role='button' and @aria-label='Move to trash' and @aria-hidden='false' and @aria-disabled='false']",
    )
    delete_button.click()
    sleep(3)

"""
Utility function to perform delete action on the file/folder in the Google Drive web GUI.

Parameters:
- driver (WebDriver): The Selenium WebDriver instance.
- action_chain (ActionChains): The Selenium ActionChains instance for performing user actions.
- web_driver_wait (WebDriverWait): The Selenium WebDriverWait instance for waiting on elements.
- file_name: Name of file/folder to be deleted.

Returns:
None

Raises:
-

Usage:
remove_file(driver, action_chain, web_driver_wait,file_name)
"""
def remove_file(driver, action_chain, web_driver_wait,file_name):
    try:
        select_file(driver, action_chain, web_driver_wait,file_name)
    except FileNotFoundError as e:
        raise e
    else:
        delete_file(driver, action_chain, web_driver_wait)




def is_file_found(driver, web_driver_wait, file_name):

    
    try:
        # Use a CSS selector to find the file by its name
        file_locator = (By.CSS_SELECTOR, f'div.uXB7xe[aria-label*="{file_name}"]')
        condition = EC.presence_of_element_located(file_locator)
        web_driver_wait.until(condition)
        return True
    except EXC.TimeoutException as e:
        print(f"TimeoutException: {e}")
        return False
    
def clear_action_chain(chain):
    chain.reset_actions()
    for device in chain.w3c_actions.devices:
        device.clear_actions()
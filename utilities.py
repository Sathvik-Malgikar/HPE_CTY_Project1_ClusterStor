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
from selenium.common.exceptions import NoSuchElementException
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

def select_file(driver, action_chain, web_driver_wait,file_name):

    web_driver_wait.until(
        EC.presence_of_element_located(
            locators.show_more_files
        ),
    )

    
    show_more_button = driver.find_element(
    *locators.show_more_files
    )
    show_more_button.click()
    sleep(3)
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









# FUNCTION TO RENAME A FILE. THIS IS CALLED LATER IN THE MAIN FILE.
def rename_file(driver, action_chain, web_driver_wait, old_file_name, new_file_name):
    try:
        select_file(driver, action_chain, web_driver_wait, old_file_name)
    except FileNotFoundError as e:
        raise e
    else:
        file_element = driver.find_element(*locators.file_name_selector)
        action_chain.move_to_element(file_element).perform()
        sleep(3)

        action_chain.reset_actions()
        for device in action_chain.w3c_actions.devices:
            device.clear_actions()

        sleep(1)
        action_chain.move_to_element(file_element).send_keys("n").perform()
        action_chain.reset_actions()
        for device in action_chain.w3c_actions.devices:
            device.clear_actions()

        sleep(3)

        action_chain.send_keys(new_file_name).perform()

        # Locate and click the OK button
        ok_button = web_driver_wait.until(EC.element_to_be_clickable(locators.ok_button_locator))
        ok_button.click()
        sleep(10)

        try:
            file_element = driver.find_element(*locators.file_name_selector)
            assert False, f"Original File '{old_file_name}' Found after Rename"
        except NoSuchElementException:
            pass  # Original file not found, continue

        try:
            renamed_file_element = driver.find_element(*locators.renamed_file_name_selector)
        except NoSuchElementException:
            assert False, f"New File '{new_file_name}' Not Found after Rename"



# FUNCTION TO UNDO DELETE ACTION. THIS IS CALLED LATER IN THE MAIN FILE.
def undo_delete_action(driver, action_chain, web_driver_wait, file_to_be_retrieved):
    trash_button = web_driver_wait.until(EC.element_to_be_clickable(locators.trash_button_locator))
    trash_button.click()

    try:
        web_driver_wait.until(EC.presence_of_element_located(locators.trashed_file_locator))
    except:
        assert False, "File Not Found in Trash"
    else:
        # Click on the trashed file
        trashed_file_element = driver.find_element(*locators.trashed_file_locator)
        action_chain.move_to_element(trashed_file_element).click().perform()
        sleep(1)

        # Press 'a' and then press Enter
        restore_from_trash_button = web_driver_wait.until(EC.element_to_be_clickable(locators.restore_from_trash_button_locator))
        restore_from_trash_button.click()
        sleep(3)

    # Check whether the file has actually been restored or not
    try:
        home_button = web_driver_wait.until(EC.element_to_be_clickable(locators.home_button_locator))
        home_button.click()
        sleep(3)
        web_driver_wait.until(EC.presence_of_element_located(locators.restored_file_locator))
    except:
        assert False, f"File '{file_to_be_retrieved}' Not Restored"
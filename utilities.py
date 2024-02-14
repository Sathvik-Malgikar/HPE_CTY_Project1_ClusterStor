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
from selenium.common.exceptions import TimeoutException
import locators
import files


web_driver_wait : WebDriverWait
action_chain: ActionChains
driver: Chrome

def initialize_driver(drv ):
    global driver

    driver  = drv
def initialize_web_driver_wait(wdw ):
    global web_driver_wait

    web_driver_wait  = wdw
def initialize_action_chain(ac ):
    global action_chain

    action_chain  = ac

    

"""
Utility function to select a file in Google Drive GUI
"""

def select_file(file_name,show_more_needed=True): # show_more_needed is to ensure backwards compatibility

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
Utility function to select a folder in Google Drive GUI
"""
def select_folder(folder_name,show_more_needed=True):
    if(show_more_needed):
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
    # Find folder
    try:
        web_driver_wait.until(EC.presence_of_element_located(locators.folder_locator))
    except:
        assert False, f"Folder '{files.folder_name}' Not Found"
    else:
        folder_element = driver.find_element(*locators.folder_locator)
        action_chain.move_to_element(folder_element).click().perform()
        sleep(3)

        action_chain.reset_actions()
        for device in action_chain.w3c_actions.devices:
            device.clear_actions()
        sleep(1)


"""
Utility function to click delete button on a selected file/folder in the Google Drive web GUI.
"""
def delete_file( ):
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
"""
def remove_file(file_name):
    try:
        select_file( file_name)
    except FileNotFoundError as e:
        raise e
    else:
        delete_file( )


"""
Utility function to rename a folder in the Google Drive web GUI.
"""
def rename_folder( old_folder_name, new_folder_name):
    try:
        select_folder(old_folder_name)
    except FileNotFoundError as e:
        raise e
    else:
        folder_element = driver.find_element(*locators.folder_locator)
        action_chain.move_to_element(folder_element).perform()
        sleep(3)
        action_chain.reset_actions()
        for device in action_chain.w3c_actions.devices:
            device.clear_actions()
        sleep(1)
        action_chain.move_to_element(folder_element).send_keys("n").perform()
        action_chain.reset_actions()
        for device in action_chain.w3c_actions.devices:
            device.clear_actions()

        sleep(3)

        action_chain.send_keys(new_folder_name).perform()

        # Locate and click the OK button
        ok_button = web_driver_wait.until(EC.element_to_be_clickable(locators.ok_button_locator))
        ok_button.click()
        sleep(10)

# def select_file(file_name):
#     try:
#         file_selector = locators.file_selector(file_name)
#         web_driver_wait.until(EC.presence_of_element_located(file_selector),)
#     except:
#         raise FileNotFoundError("File Not found")
#     else:
#         file_element = driver.find_element(*file_selector)
#         action_chain.move_to_element(file_element).click()
#         action_chain.perform()


def rename_action(new_file_name):
    rename_button = web_driver_wait.until(EC.element_to_be_clickable(locators.rename_button_locator))
    rename_button.click()
    sleep(1)
    # Send keys for the new file name
    pyautogui.write(new_file_name)


def click_on_ok_button():
    ok_button = web_driver_wait.until(EC.element_to_be_clickable(locators.ok_button_locator))
    ok_button.click()
    sleep(10)

    
def rename_verification( old_file_name, new_file_name):
    try:
        file_element = driver.find_element(*locators.file_name_selector)
        assert False, f"Original File '{old_file_name}' Found after Rename"
    except NoSuchElementException:
        pass  # Original file not found, continue
    try:
        renamed_file_element = driver.find_element(*locators.renamed_file_name_selector)
    except NoSuchElementException:
        assert False, f"New File '{new_file_name}' Not Found after Rename"
    
    


def click_trash_button() : 
    trash_button = web_driver_wait.until(EC.element_to_be_clickable(locators.trash_button_locator))
    trash_button.click()
    sleep(5)

def select_file_from_trash():
    try:
        web_driver_wait.until(EC.presence_of_element_located(locators.trashed_file_locator))
    except:
        assert False, "File Not Found in Trash"
    else:
        # Click on the trashed file
        trashed_file_element = driver.find_element(*locators.trashed_file_locator)
        action_chain.move_to_element(trashed_file_element).click().perform()
        sleep(6)


def click_on_restore_from_trash_button():
    restore_from_trash_button = web_driver_wait.until(EC.element_to_be_clickable(locators.restore_from_trash_button_locator))
    restore_from_trash_button.click()
    sleep(3)

def click_on_home_button():
    home_button = web_driver_wait.until(EC.element_to_be_clickable(locators.home_button_locator))
    home_button.click()
    sleep(3)


def verify_restoration( file_name):
    click_on_home_button()
    if(verify_folder_presence(file_name)):
        return True
    else:
        assert False, f"File '{file_name}' Not Restored"

    


"""
Utility function to undo delete action in the Google Drive web GUI.
"""
# def undo_delete_action(driver, action_chain, web_driver_wait, file_to_be_retrieved):
#     trash_button = web_driver_wait.until(EC.element_to_be_clickable(locators.trash_button_locator))
#     trash_button.click()
#     sleep(5)

#     try:
#         web_driver_wait.until(EC.presence_of_element_located(locators.trashed_file_locator))
#     except:
#         assert False, "File Not Found in Trash"
#     else:
#         # Click on the trashed file
#         trashed_file_element = driver.find_element(*locators.trashed_file_locator)
#         action_chain.move_to_element(trashed_file_element).click().perform()
#         sleep(6)
#         restore_from_trash_button = web_driver_wait.until(EC.element_to_be_clickable(locators.restore_from_trash_button_locator))
#         restore_from_trash_button.click()
#         sleep(3)

#     # Check whether the file has actually been restored or not
#     try:
#         home_button = web_driver_wait.until(EC.element_to_be_clickable(locators.home_button_locator))
#         home_button.click()
#         sleep(3)
#         web_driver_wait.until(EC.presence_of_element_located(locators.restored_file_locator))
#     except:
#         assert False, f"File '{file_to_be_retrieved}' Not Restored"


def open_folder(open_folder):

    
    try:
        # Use a CSS selector to find the file by its name
        file_locator = (By.CSS_SELECTOR, f'div.uXB7xe[aria-label*="{open_folder}"]')
        folder_element = driver.find_element(*file_locator)
        double_click_element(folder_element)
        
        return True
    except EXC.TimeoutException as e:
        print(f"TimeoutException: {e}")
        return False


def send_keys_to_element(element_locator, text):
    try:
        element = driver.find_element(*element_locator)
        element.send_keys(text)
    except Exception as e:
        print(f"Error sending keys to element: {e}")

def find_element( locator):
    try:
        element = driver.find_element(*locator)
        return element
    except NoSuchElementException:
        print(f"Element not found with locator {locator}")
        return None

def verify_folder_presence( folder_name, timeout=10):
    folder_locator = (By.XPATH, f'//div[@class="uXB7xe" and contains(@aria-label,"{folder_name}" )]')
    try:
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located(folder_locator))
        return True
    except TimeoutException:
        print(f"Folder element with name '{folder_name}' not found within {timeout} seconds.")
        return False
    
def clear_action_chain():
    action_chain.reset_actions()
    for device in action_chain.w3c_actions.devices:
        device.clear_actions()

def wait_for_element(locator):
    try:
        element = web_driver_wait.until(EC.presence_of_element_located(locator))
        return element
    except TimeoutException:
        print(f"Timeout waiting for element with locator {locator}")
        return None
    
def wait_to_click(locator):
    try:
        element = web_driver_wait.until(EC.element_to_be_clickable(locator))
        return element
    except TimeoutException:
        print(f"Timeout waiting for element with locator {locator}")
        return None

def click_element( element):
    try:
        action_chain.click(element).perform()
    except Exception as e:
        print(f"Error clicking on element: {e}")


def double_click_element( element):
    try:
        action_chain.double_click(element).perform()
    except Exception as e:
        print(f"Error double clicking on element: {e}")


def drag_and_drop_element( source_element, destination_element):
    try:
        action_chain.drag_and_drop(source_element, destination_element).perform()
    except Exception as e:
        print(f"Error dragging and dropping element: {e}")
        
def click_on_new_button():
    # clicks on new button
    web_driver_wait.until(EC.element_to_be_clickable(locators.new_button_selector))
    new_button = driver.find_element(*locators.new_button_selector)
    new_button.click()
    sleep(2)
    
    # clicks on new file
    web_driver_wait.until(EC.element_to_be_clickable(locators.file_upload_button_selector))
    upload_button = driver.find_element(*locators.file_upload_button_selector)
    upload_button.click()
    sleep(3)
    
def type_into_dialogue_box(FILE_TO_UPLOAD):
    # types into dialogue box
    pyautogui.typewrite(FILE_TO_UPLOAD)
    sleep(1)
    pyautogui.press("enter")
    sleep(5)
    
def wait_till_upload():
    # try block to deal with situation of file being there already
    try:
        # to see if the warning of file being alreay present shows up
        driver.find_element(*locators.file_already_present_text)
    except EXC.NoSuchElementException:
        
        print("file not already in google drive, uploading as new file")
    else:
        # to deal with file already exisiting
        pyautogui.press("tab")
        pyautogui.press("tab")
        
        sleep(0.5)
        pyautogui.press("space")
        sleep(1)
    finally:
        # wait till upload completes, max 10 seconds for now 
        web_driver_wait.until(EC.presence_of_element_located(locators.upload_complete_text))
        sleep(2)
        
def navigateTo(path):
    for foldername in path.split("/"): #A/B/eruier.mp3
        if verify_folder_presence(foldername):
            open_folder(foldername)
            sleep(3)
        else:
            print(f"navigateTo {path} failed, {foldername} not found!")
            return -1
        
        
        
    
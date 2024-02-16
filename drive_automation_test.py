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
from selenium.common.exceptions import StaleElementReferenceException

import locators
import files
from selenium.common.exceptions import StaleElementReferenceException
import utilities


class DriveUtils:
    def __init__(self, driver: Chrome, action_chain: ActionChains, web_driver_wait: WebDriverWait):
        self.driver = driver
        self.action_chain = action_chain
        self.web_driver_wait = web_driver_wait

    def remove_file(self, file_name):
        utilities.remove_file(file_name)# TODO shift code here

    def rename_folder(self, old_folder_name, new_folder_name):
        utilities.rename_folder(old_folder_name, new_folder_name)

    def click_trash_button(self):
        utilities.click_trash_button()

    def select_file(self, file_name, mode):
        utilities.select_file(file_name, show_more_needed=mode)

    def click_on_restore_from_trash_button(self):
        utilities.click_on_restore_from_trash_button()

    def click_on_home_button(self):
        utilities.click_on_home_button()

    def verify_restoration(self, file_name):
        utilities.verify_restoration(file_name)

    def rename_action(self, new_file_name):
        utilities.rename_action(new_file_name)

    def click_on_ok_button(self):
        utilities.click_on_ok_button()

    def rename_verification(self, old_file_name, new_file_name):
        utilities.rename_verification(old_file_name, new_file_name)

    def select_file_from_trash(self):
        utilities.select_file_from_trash()


"""
    Pytest fixture for providing a Selenium WebDriver instance with Chrome.
"""


@pytest.fixture(scope="session", autouse=True)
def driver():
    # svc = Service(executable_path="./chromedriver.exe")
    webdriver = Chrome(executable_path="./chromedriver.exe")
    utilities.initialize_driver(webdriver)
    yield webdriver
    webdriver.quit()


"""
    Pytest fixture for providing an ActionChains instance for Selenium WebDriver.
"""


@pytest.fixture(scope="session", autouse=True)
def action_chain(driver):
    chain = ActionChains(driver)
    utilities.initialize_action_chain(chain)
    yield chain
    utilities.clear_action_chain()


"""
    Pytest fixture for providing a WebDriverWait instance for Selenium WebDriver.
"""


@pytest.fixture(scope="session", autouse=True)
def web_driver_wait(driver):
    w_wait = WebDriverWait(driver, 10)
    utilities.initialize_web_driver_wait(w_wait)
    yield w_wait


@pytest.fixture(scope="session", autouse=True)
def drive_utils(driver, action_chain, web_driver_wait):
    return DriveUtils(driver, action_chain, web_driver_wait)


"""
    Test function for signing into Google Drive using Selenium WebDriver.
"""


def test_signin(drive_utils):
    drive_utils.driver.get("https://www.google.com/intl/en-US/drive/")
    drive_utils.driver.maximize_window()
    sleep(0.8)

    drive_utils.web_driver_wait.until(
        EC.presence_of_element_located((By.LINK_TEXT, "Sign in")))

    signin_ele = drive_utils.driver.find_element(By.LINK_TEXT, "Sign in")
    signin_ele.click()
    sleep(1.3)
    # opened by clicking sign-in anchor tag
    sign_in_tab = drive_utils.driver.window_handles[-1]
    drive_utils.driver.switch_to.window(sign_in_tab)
    sleep(1.3)
    parser = configparser.ConfigParser()
    parser.read("config.ini")
    account_email_id = parser.get("Account Credentials", "email")
    print("Sending email")
    drive_utils.action_chain.send_keys(account_email_id)
    drive_utils.action_chain.send_keys(Keys.ENTER)
    drive_utils.action_chain.perform()
    drive_utils.web_driver_wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//span[contains(text(), 'Welcome')]")
        ),
    )
    sleep(1.5)  # to deal with input animation
    drive_utils.action_chain.reset_actions()
    for device in drive_utils.action_chain.w3c_actions.devices:
        device.clear_actions()
    account_pwd = parser.get("Account Credentials", "password")
    drive_utils.action_chain.send_keys(account_pwd)
    drive_utils.action_chain.send_keys(Keys.ENTER)
    drive_utils.action_chain.perform()
    sleep(5)

    try:
        drive_utils.web_driver_wait.until(EC.title_is("Home - Google Drive"))
        assert True

    except TimeoutError:
        assert False
    else:
        pyautogui.keyDown("ctrl")
        pyautogui.press("-")
        pyautogui.press("-")
        pyautogui.keyUp("ctrl")

    sleep(5)


def test_dummy_test_prerequisite(driver):
    file_list_to_upload = ["test.txt", "cty_ppt.pdf", "test2.txt"]

    for file in file_list_to_upload:

        utilities.click_on_new_button()

        utilities.type_into_dialogue_box(file)

        utilities.wait_till_upload()
        driver.refresh()
        sleep(5)


"""
    Test function to retrieve filenames from the Google Drive web GUI.
"""


def test_get_filenames(drive_utils):
    file_name_divs = drive_utils.driver.find_elements_by_css_selector(
        "div.KL4NAf")
    sleep(4)
    assert len(file_name_divs) > 0


"""
Test function to remove a file from the Google Drive web GUI.
"""


def test_remove_file(drive_utils):
    file_name = files.trashed_file_name
    drive_utils.remove_file(file_name)
    drive_utils.driver.refresh()


"""
Test function to rename a file in the Google Drive web GUI.
"""


def test_rename_file(drive_utils):
    old_file_name = files.file_name
    new_file_name = files.renamed_file_name
    drive_utils.select_file(old_file_name, False)
    drive_utils.rename_action(new_file_name)
    drive_utils.click_on_ok_button()
    drive_utils.rename_verification(old_file_name, new_file_name)


"""
Test function to undo delete action in the Google Drive web GUI.
"""


def test_undo_delete_action(drive_utils):
    file_name_to_retrieve = files.file_to_be_restored
    drive_utils.click_trash_button()
    drive_utils.select_file_from_trash()
    drive_utils.click_on_restore_from_trash_button()
    drive_utils.verify_restoration(file_name_to_retrieve)


"""
Test function to rename a folder in the Google Drive web GUI.
"""


def test_rename_folder():
    old_folder_name = files.folder_name
    new_folder_name = files.renamed_folder_name
    drive_utils.select_file_from_trash(old_folder_name)
    drive_utils.rename(new_folder_name)
    drive_utils.click_on_ok_button()


"""
## Test function to create a new folder in the Google Drive web GUI.
"""


@pytest.fixture
def folder_name():
    return files.create_folder_name


def test_create_folder(driver, folder_name):
    new_btn_element = utilities.wait_for_element(locators.new_btn_locator)
    utilities.click_element(new_btn_element)
    utilities.click_element(new_btn_element)

    input_field = utilities.wait_for_element(locators.input_field_locator)

    input_field.clear()
    utilities.send_keys_to_element(locators.input_field_locator, folder_name)
    utilities.send_keys_to_element(locators.input_field_locator, Keys.ENTER)
    assert utilities.verify_folder_presence(folder_name)
    sleep(3)


"""
## Test function to upload new file in the Google Drive web GUI.
"""


def test_upload_file(driver):
    # this file is present in User folder
    FILE_TO_UPLOAD = "Screenshot (177).png"

    utilities.click_on_new_button()

    utilities.type_into_dialogue_box(FILE_TO_UPLOAD)

    # this is utility solely because prerequisites aso reuses this function
    utilities.wait_till_upload()

    assert utilities.verify_file_presence(driver, FILE_TO_UPLOAD, 10)


"""
## Test function to download a file in the Google Drive web GUI.
"""


def test_download_file(driver, web_driver_wait):
    web_driver_wait.until(EC.element_to_be_clickable(
        locators.file_selector(files.renamed_file_name)))
    sleep(2)
    file_div = driver.find_element(
        *locators.file_selector(files.renamed_file_name))
    file_div.click()
    web_driver_wait.until(EC.element_to_be_clickable(
        locators.download_file_selector))
    sleep(2)
    download_button = driver.find_element(*locators.download_file_selector)
    download_button.click()
    sleep(3)


"""
## Test function to remove multiple files in the Google Drive web GUI.
"""


def test_remove_multiple_files():
    files = ['test.txt', 'test1.txt']
    for file in files:
        try:
            utilities.remove_file( file)
        except FileNotFoundError as e:
            assert False, repr(e)
        finally:
            utilities.clear_action_chain()
            driver.refresh()





def test_copy_file(drive_utils):
    utilities.select_file( files.file_name_for_copy,show_more_needed=True)
    drive_utils.action_chain.context_click().perform()
    sleep(5)

    make_a_copy_element = web_driver_wait.until(EC.element_to_be_clickable(locators.make_a_copy_element_locator))
    make_a_copy_element.click()

    sleep(5)
    drive_utils.driver.refresh()
    sleep(7)
    copied_file_element = utilities.find_element(locators.copied_file_locator)
    assert copied_file_element is not None


@pytest.fixture
def move_file():
    return files.file_move_name


def test_move_file(move_file):

    utilities.select_file(move_file, show_more_needed=True)
    utilities.clear_action_chain()
    sleep(2)
    file_element = utilities.find_element(locators.file_move_locator)
    destination_folder_element = utilities.find_element(
        locators.destination_folder_element_locator)
    utilities.drag_and_drop_element(file_element, destination_folder_element)
    sleep(5)

    try:
        destination_folder_element = utilities.find_element(
            locators.destination_folder_element_locator)
        utilities.double_click_element(destination_folder_element)
        sleep(4)
    except StaleElementReferenceException:
        print("StaleElementReferenceException occurred. Retrying...")

    file_in_destination = utilities.find_element(locators.file_move_locator)
    assert file_in_destination is not None, "File has not been moved successfully to the destination folder"
    my_drive_button = utilities.find_element(locators.my_drive_button_locator)
    my_drive_button.click()
    sleep(3)
    moved_file_element = utilities.find_element(locators.file_move_locator)
    assert not moved_file_element, "File is still present in the old folder"   


def test_view_file_info():    
    utilities.select_file( files.view_info_file_name)
    action_chain.send_keys("gd").perform()   
    try:        
        web_driver_wait.until(EC.presence_of_element_located(locators.file_info_dialog_locator))
    except:
        assert False, f"File info dialog for {files.view_info_file_name} is not visible"


def test_delete_file_permanently(drive_utils):
    drive_utils.driver.refresh()
    sleep(5)    
    utilities.remove_file( files.delete_forever_file_name)    
    trash_btn_element=utilities.wait_for_element(locators.trash_button_locator)
    utilities.click_element(trash_btn_element)    
    deleted_file_locator = locators.file_selector(files.delete_forever_file_name)
    web_driver_wait.until(EC.presence_of_element_located(deleted_file_locator))    
    utilities.clear_action_chain()    
    utilities.select_file( files.delete_forever_file_name, show_more_needed=False)    
    delete_forever_btn_element=utilities.wait_for_element(locators.delete_forever_button_locator) 
    utilities.click_element(delete_forever_btn_element)      
    sleep(2)    
    try:
        delete_confirm_btn_element = utilities.wait_for_element(locators.delete_confirm_button_locator) 
        utilities.click_element(delete_confirm_btn_element) 
        sleep(3)
    except:
        assert False, "Error occured"
    else:
        assert True, f"{files.delete_forever_file_name} is permanently deleted"

"""
## Test function to logout from the Google Drive web GUI.
"""
def test_logout(drive_utils):     
    user_profile_button_element = drive_utils.driver.find_element(*locators.user_profile_button_locator)
    utilities.click_element(user_profile_button_element)
    sleep(2)
    try:
        sign_out_button_element = drive_utils.driver.find_element(*locators.sign_out_button_locator)
        utilities.click_element(sign_out_button_element)
    except Exception as e:
        print("error occured ",e)
        
    # Assert that the login screen is visible after logging out
    assert driver.title == "Home - Google Drive"
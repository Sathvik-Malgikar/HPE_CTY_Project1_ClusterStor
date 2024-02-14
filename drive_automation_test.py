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
import utilities

"""
    Pytest fixture for providing a Selenium WebDriver instance with Chrome.
"""
@pytest.fixture(scope="session")
def driver():
    # svc = Service(executable_path="./chromedriver.exe")
    webdriver = Chrome(executable_path="./chromedriver.exe")
    yield webdriver
    webdriver.quit()


"""
    Pytest fixture for providing an ActionChains instance for Selenium WebDriver.
"""
@pytest.fixture
def action_chain(driver):
    chain = ActionChains(driver)
    yield chain
    chain.reset_actions()
    for device in chain.w3c_actions.devices:
        device.clear_actions()


"""
    Pytest fixture for providing a WebDriverWait instance for Selenium WebDriver.
"""
@pytest.fixture
def web_driver_wait(driver):
    w_wait = WebDriverWait(driver, 10)
    yield w_wait


"""
    Test function for signing into Google Drive using Selenium WebDriver.
"""
def test_signin(driver,web_driver_wait,action_chain):
    driver.get("https://www.google.com/intl/en-US/drive/")
    driver.maximize_window()
    sleep(0.8)

    web_driver_wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Sign in")))

    signin_ele = driver.find_element(By.LINK_TEXT, "Sign in")
    signin_ele.click()
    sleep(1.3)
    # opened by clicking sign-in anchor tag
    sign_in_tab = driver.window_handles[-1]
    driver.switch_to.window(sign_in_tab)
    sleep(1.3)
    parser = configparser.ConfigParser()
    parser.read("config.ini")
    account_email_id = parser.get("Account Credentials", "email")
    print("Sending email")
    action_chain.send_keys(account_email_id)
    action_chain.send_keys(Keys.ENTER)
    action_chain.perform()
    web_driver_wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//span[contains(text(), 'Welcome')]")
        ),
    )
    sleep(1.5)  # to deal with input animation
    utilities.clear_action_chain(action_chain)
    account_pwd = parser.get("Account Credentials", "password")
    action_chain.send_keys(account_pwd)
    action_chain.send_keys(Keys.ENTER)
    action_chain.perform()
    sleep(5)
  
    try:
        web_driver_wait.until(EC.title_is("Home - Google Drive"))
        assert True
       
    except TimeoutError:
        assert False
    else:
        pyautogui.keyDown("ctrl")
        pyautogui.press("-")
        pyautogui.press("-")
        pyautogui.keyUp("ctrl")
        


"""
    Test function to retrieve filenames from the Google Drive web GUI.
"""
def test_get_filenames(driver, action_chain, web_driver_wait):
    file_name_divs = driver.find_elements_by_css_selector("div.KL4NAf")

    sleep(4)
    assert len(file_name_divs) > 0


"""
Test function to remove a file from the Google Drive web GUI.
"""
def test_remove_file(driver, action_chain, web_driver_wait):
    file_name = files.trashed_file_name
    utilities.remove_file(driver, action_chain, web_driver_wait,file_name)
    driver.refresh()


"""
Test function to rename a file in the Google Drive web GUI.
"""
def test_rename_file(driver, action_chain, web_driver_wait):
    old_file_name = files.file_name
    new_file_name = files.renamed_file_name
    utilities.rename_file(driver, action_chain, web_driver_wait, old_file_name, new_file_name)
    driver.refresh()


"""
Test function to rename a folder in the Google Drive web GUI.
"""
def test_rename_folder(driver, action_chain, web_driver_wait):
    old_folder_name = files.folder_name
    new_folder_name = files.renamed_folder_name
    utilities.rename_folder(driver, action_chain, web_driver_wait, old_folder_name, new_folder_name)
    driver.refresh()
    assert True

"""
Test function to undo delete action in the Google Drive web GUI.
"""
def test_undo_delete_action(driver, action_chain, web_driver_wait):
    file_name_to_retrieve = files.trashed_file_name
    utilities.undo_delete_action(driver, action_chain, web_driver_wait, file_name_to_retrieve)
    driver.refresh()


"""
## Test function to create a new folder in the Google Drive web GUI.
"""
# def test_create_folder(driver, action_chain, web_driver_wait):
   
#     new_btn = web_driver_wait.until(EC.element_to_be_clickable(locators.new_btn_locator))
#     new_btn.click()
#     sleep(4)

    
#     new_folder_option = web_driver_wait.until(
#         EC.element_to_be_clickable(locators.new_folder_option_locator))

    
#     action_chain.move_to_element(new_folder_option).click().perform()

   

#     web_driver_wait.until(EC.presence_of_element_located(locators.input_field_locator))

   
#     input_field = driver.find_element(*locators.input_field_locator)
#     input_field.clear()
#     # sleep(5)

#     input_field.send_keys(files.create_folder_name)
#     input_field.send_keys(Keys.ENTER)

#     sleep(10)
#     xpath_expression = f"//*[text()='{files.create_folder_name}']"
   
#     folder_element = web_driver_wait.until(
#         EC.presence_of_element_located((By.XPATH,xpath_expression))
#     )
#     assert folder_element.is_displayed(), "Folder element is not visible"

@pytest.fixture
def folder_name():
    return files.create_folder_name


def test_create_folder(driver,action_chain,web_driver_wait,folder_name):
    new_btn_element=utilities.wait_for_element(web_driver_wait,locators.new_btn_locator)
    utilities.click_element(action_chain,new_btn_element)
    utilities.click_element(action_chain,new_btn_element)

    input_field=utilities.wait_for_element(web_driver_wait,locators.input_field_locator)
    
    input_field.clear()
    utilities.send_keys_to_element(driver,locators.input_field_locator, folder_name)
    utilities.send_keys_to_element(driver,locators.input_field_locator, Keys.ENTER)
    assert utilities.verify_folder_presence(driver,folder_name)
    sleep(3)

"""
## Test function to upload new file in the Google Drive web GUI.
"""
def test_upload_file(driver,web_driver_wait,action_chain):
    FILE_TO_UPLOAD = "Screenshot (177).png" # this file is present in User folder
    
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
    
    # types into dialogue box
    pyautogui.typewrite(FILE_TO_UPLOAD)
    sleep(1)
    pyautogui.press("enter")
    sleep(5)
    
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
        # a refresh to make sure file shows up
        driver.refresh()
        
        # a small wait to ensure page is stable after refresh
        web_driver_wait.until(EC.presence_of_element_located(locators.file_name_containerdiv))
        sleep(5)
        
        # looks for the uploade file in drive 
        file_name_divs = driver.find_elements(*locators.file_name_containerdiv)
        file_names= list(map(lambda a:a.text, file_name_divs))
        assert FILE_TO_UPLOAD in file_names
    
"""
## Test function to download a file in the Google Drive web GUI.
"""  
def test_download_file(driver,web_driver_wait,action_chain):
    web_driver_wait.until(EC.element_to_be_clickable(locators.file_selector(files.renamed_file_name)))
    sleep(2)
    file_div = driver.find_element(*locators.file_selector(files.renamed_file_name))
    file_div.click()
    web_driver_wait.until(EC.element_to_be_clickable(locators.download_file_selector))
    sleep(2)
    download_button = driver.find_element(*locators.download_file_selector)
    download_button.click()
    sleep(3)

"""
## Test function to remove multiple files in the Google Drive web GUI.
"""
def test_remove_multiple_files(driver, action_chain, web_driver_wait):
    files = ['test.txt','test1.txt']
    for file in files:
        try:
            utilities.remove_file(driver, action_chain, web_driver_wait,file)
        except FileNotFoundError as e:
            assert False,repr(e)
        finally:
            action_chain.reset_actions()
            for device in action_chain.w3c_actions.devices:
                device.clear_actions()
            driver.refresh()



"""
## Test function to logout from the Google Drive web GUI.
"""
def test_logout(driver, action_chain, web_driver_wait):     
    user_profile_button_element = driver.find_element(*locators.user_profile_button_locator)
    utilities.click_element(action_chain,user_profile_button_element)
    sleep(2)
    try:
        sign_out_button_element = driver.find_element(*locators.sign_out_button_locator)
        utilities.click_element(action_chain,sign_out_button_element)
    except Exception as e:
        print("error occured ",e)
        
    # Assert that the login screen is visible after logging out
    assert driver.title == "Home - Google Drive"

def test_copy_file(driver, action_chain, web_driver_wait,file_name_to_copy="test.txt"):
    utilities.select_file(driver, action_chain, web_driver_wait, files.file_name_for_copy,show_more_needed=True)
    action_chain.context_click().perform()
    sleep(5)
    #make_copy_button=driver.find_element(*locators.make_a_copy_elemenent_locator)
    make_a_copy_element = web_driver_wait.until(EC.element_to_be_clickable(locators.make_a_copy_element_locator))
    make_a_copy_element.click()

    sleep(5)
    
    driver.refresh()
    sleep(7)
    copied_file_element = driver.find_element(*locators.copied_file_locator)
    assert copied_file_element is not None

 

# def test_move_file(driver, action_chain, web_driver_wait):
#     utilities.select_file(driver,action_chain,web_driver_wait,files.file_move_name)
#     utilities.clear_action_chain(action_chain)
#     sleep(2)
    
#     file_element = driver.find_element(*locators.file_move_locator)
#     destination_folder_element = driver.find_element(*locators.destination_folder_element_locator)

#     action_chain.drag_and_drop(file_element, destination_folder_element).perform()
#     sleep(5)
    
#     try:
        
#         destination_folder_element = driver.find_element(*locators.destination_folder_element_locator)

#         # Double click on the destination_folder_element
#         action_chain.double_click(destination_folder_element).perform()
#         sleep(4)
#     except StaleElementReferenceException:
#         print("StaleElementReferenceException occurred. Retrying...")

#     sleep(2)

#     try:
#         file_in_destination = driver.find_element(*locators.file_move_locator)
#     except NoSuchElementException:
#     # Set moved_file_element to None if the element is not found
#         file_in_destination = None

#     assert file_in_destination is not None, "File has not been moved successfully to the destination folder"


#     my_drive_button = driver.find_element(*locators.my_drive_button_locator)
#     my_drive_button.click()
#     sleep(3)
    
#     try:
#         moved_file_element = driver.find_element(*locators.file_move_locator)
#     except NoSuchElementException:
#     # Set moved_file_element to None if the element is not found
#         moved_file_element = None
   
#     assert not moved_file_element, "File is still present in the old folder"

    
@pytest.fixture
def move_file():
    return files.file_move_name

def test_move_file(driver, action_chain, web_driver_wait,move_file):

    utilities.select_file(driver,action_chain,web_driver_wait,move_file,show_more_needed=True)
    utilities.clear_action_chain(action_chain)
    sleep(2)
    file_element =utilities.find_element(driver,locators.file_move_locator)
    destination_folder_element = utilities.find_element(driver,locators.destination_folder_element_locator)
    utilities.drag_and_drop_element(action_chain, file_element, destination_folder_element)
    sleep(5)
    
    try: 
        destination_folder_element = utilities.find_element(driver,locators.destination_folder_element_locator)
        utilities.double_click_element(action_chain,destination_folder_element)
        sleep(4)
    except StaleElementReferenceException:
        print("StaleElementReferenceException occurred. Retrying...")

    file_in_destination = utilities.find_element(driver,locators.file_move_locator)
    assert file_in_destination is not None, "File has not been moved successfully to the destination folder"
    my_drive_button = utilities.find_element(driver,locators.my_drive_button_locator)
    my_drive_button.click()
    sleep(3)
    moved_file_element = utilities.find_element(driver,locators.file_move_locator)
    assert not moved_file_element, "File is still present in the old folder"   


def test_view_file_info(driver, action_chain, web_driver_wait):    
    utilities.select_file(driver, action_chain, web_driver_wait, files.view_info_file_name)
    action_chain.send_keys("gd").perform()   
    try:        
        web_driver_wait.until(EC.presence_of_element_located(locators.file_info_dialog_locator))
    except:
        assert False, f"File info dialog for {files.view_info_file_name} is not visible"

        
def test_delete_file_permanently(driver, action_chain, web_driver_wait):
    driver.refresh()
    sleep(5)    
    utilities.remove_file(driver, action_chain, web_driver_wait, files.delete_forever_file_name)    
    trash_btn_element=utilities.wait_for_element(web_driver_wait,locators.trash_button_locator)
    utilities.click_element(action_chain,trash_btn_element)    
    deleted_file_locator = locators.file_selector(files.delete_forever_file_name)
    web_driver_wait.until(EC.presence_of_element_located(deleted_file_locator))    
    utilities.clear_action_chain(action_chain)    
    utilities.select_file(driver, action_chain, web_driver_wait, files.delete_forever_file_name, show_more_needed=False)    
    delete_forever_btn_element=utilities.wait_for_element(web_driver_wait,locators.delete_forever_button_locator) 
    utilities.click_element(action_chain,delete_forever_btn_element)      
    sleep(2)    
    try:
        delete_confirm_btn_element = utilities.wait_for_element(web_driver_wait,locators.delete_confirm_button_locator) 
        utilities.click_element(action_chain,delete_confirm_btn_element) 
        sleep(3)
    except:
        assert False, "Error occured"
    else:
        assert True, f"{files.delete_forever_file_name} is permanently deleted"

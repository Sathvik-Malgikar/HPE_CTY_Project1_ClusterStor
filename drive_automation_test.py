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
import files
from utilities import CommonActions
from utilities import ButtonClicker
import autoGUIutils
import os

@pytest.fixture( scope="session" ,autouse=True)
def utilityInstance():
    instance = CommonActions()
    instance.setup()
    yield instance
    instance.teardown()


@pytest.fixture(scope="function", autouse=True)
def button_clicker(utilityInstance):
    instance = ButtonClicker(utilityInstance.driver, utilityInstance.web_driver_wait)
    yield instance

"""
    Test function for signing into Google Drive using Selenium WebDriver.
"""


def test_signin(utilityInstance):
    utilityInstance.driver.get("https://www.google.com/intl/en-US/drive/")
    utilityInstance.driver.maximize_window()
    sleep(0.8)

    signin_ele = utilityInstance.wait_to_click(locators.sign_in_link)
    signin_ele.click()
    sleep(1.3)
    # opened by clicking sign-in anchor tag
    sign_in_tab = utilityInstance.driver.window_handles[-1]
    utilityInstance.driver.switch_to.window(sign_in_tab)
    sleep(1.3)
    parser = configparser.ConfigParser()
    parser.read("config.ini")
    account_email_id = parser.get("Account Credentials", "email")
    print("Sending email")
    utilityInstance.send_keys_to_focused(account_email_id)
    utilityInstance.send_keys_to_focused(Keys.ENTER)
    
    utilityInstance.wait_for_element( locators.welcome_span)
    sleep(3)  # to deal with input animation
   
    account_pwd = parser.get("Account Credentials", "password")
    print(account_pwd)
    utilityInstance.send_keys_to_focused(account_pwd)
    utilityInstance.send_keys_to_focused(Keys.ENTER)
    
    sleep(5)

    try:
        utilityInstance.web_driver_wait.until(EC.title_is("Home - Google Drive"))
        assert True

    except TimeoutError:
        assert False
    else:
        autoGUIutils.zoom_out()

    sleep(5)


def test_prerequisites(utilityInstance):
    rawfilenames= [files.file_name_for_copy, files.file_name, files.file_move_name,files.view_info_file_name, *files.fileCollection ,files.share_file,files.delete_forever_file_name]
    file_list_to_upload = " ".join(list(map(lambda a:f'"{a}"',rawfilenames)))
    
    utilityInstance.click_on_new_button()
        
    upload_button = utilityInstance.wait_to_click(locators.new_menu_button_locator("File upload"))
    upload_button.click()
    sleep(2)

    autoGUIutils.type_into_dialogue_box(file_list_to_upload)

    utilityInstance.deal_duplicate_and_await_upload()
    utilityInstance.driver.refresh()
    sleep(5)
    
    # to create SVM folder
    utilityInstance.click_on_new_button()
        
    action_button = utilityInstance.wait_to_click(locators.new_menu_button_locator("New folder"))
    action_button.click()
    sleep(2)

    autoGUIutils.type_into_dialogue_box(files.folder_name_to_be_removed)
    
    utilityInstance.driver.refresh()
    assert True



"""
    Test function to retrieve filenames from the Google Drive web GUI.
"""


def test_get_filenames(utilityInstance):
    file_name_divs = utilityInstance.driver.find_elements(By.CSS_SELECTOR , 
        "div.KL4NAf")
    sleep(4)
    assert len(file_name_divs) > 0

def test_search_for_file_by_name(utilityInstance):
  
    
    utilityInstance.click_on_search_in_drive()
    autoGUIutils.type_into_dialogue_box(files.file_to_be_searched)
    file_element = utilityInstance.wait_to_click(locators.file_selector(files.file_to_be_searched))
    utilityInstance.double_click_element(file_element)
    sleep(3)
    autoGUIutils.go_back_esc()


def test_search_file_by_type(utilityInstance):
    
    
    utilityInstance.click_on_my_drive_button()
    utilityInstance.click_on_type_button()
    utilityInstance.click_on_the_required_type()
    file_element = utilityInstance.wait_to_click(locators.file_selector(files.file_to_be_searched_by_type))
    utilityInstance.double_click_element(file_element)
    sleep(3)
    autoGUIutils.go_back_esc()
    
"""
Test function to remove a file from the Google Drive web GUI.
"""


def test_remove_file(utilityInstance):
    utilityInstance.click_on_home_button()
    sleep(2)
    file_name = files.file_to_be_deleted
    utilityInstance.select_item(file_name,True)
    utilityInstance.delete_file()
    assert True


"""
Test function to rename a file in the Google Drive web GUI.
"""


def test_rename_file(utilityInstance):
    old_file_name = files.file_name
    new_file_name = files.renamed_file_name
    utilityInstance.select_item(old_file_name, False)
    utilityInstance.rename_selected_item(new_file_name)
    button_clicker.click_button(locators.ok_button_locator)
    utilityInstance.rename_verification(old_file_name, new_file_name)


"""
Test function to undo delete action in the Google Drive web GUI.
"""


def test_undo_delete_action(utilityInstance, button_clicker):
    file_name_to_retrieve = files.file_to_be_restored
    button_clicker.click_left_menu_page_buttons("Trash")
    sleep(4)
    utilityInstance.select_file_from_trash()
    button_clicker.click_action_bar_button("Restore from trash")
    restoration_successful = utilityInstance.verify_restoration(file_name_to_retrieve)
    assert restoration_successful == True, f"Failed to restore file '{file_name_to_retrieve}'"
    



"""
Test function to rename a folder in the Google Drive web GUI.
"""


def test_rename_folder(utilityInstance):
    utilityInstance.click_on_home_button()
    sleep(2)
    old_folder_name = files.folder_name
    new_folder_name = files.renamed_folder_name
    utilityInstance.select_item(old_folder_name,True)
    utilityInstance.rename_selected_item(new_folder_name)
    utilityInstance.click_on_ok_button()


"""
## Test function to create a new folder in the Google Drive web GUI.
"""


@pytest.fixture
def folder_name():
    return files.create_folder_name


def test_create_folder(utilityInstance, folder_name):
    utilityInstance.click_on_new_button()
        
    action_button = utilityInstance.wait_to_click(locators.new_menu_button_locator("New folder"))
    action_button.click()
    sleep(2)

    autoGUIutils.type_into_dialogue_box(folder_name)
    
    utilityInstance.driver.refresh()
 
    assert utilityInstance.wait_for_element(locators.file_selector(folder_name))!=None
    sleep(3)


"""
## Test function to upload new file in the Google Drive web GUI.
"""


def test_upload_file(utilityInstance):
    # this file is present in User folder
    

    utilityInstance.click_on_new_button()
    
    upload_button = utilityInstance.wait_for_element(locators.new_menu_button_locator("File upload"))
    upload_button.click()
    sleep(2)

    autoGUIutils.type_into_dialogue_box(files.FILE_TO_UPLOAD)

    # this is utility solely because prerequisites aso reuses this function
    utilityInstance.deal_duplicate_and_await_upload()

    assert utilityInstance.verify_file_presence(files.FILE_TO_UPLOAD, 10)


"""
## Test function to download a file in the Google Drive web GUI.
"""


def test_download_file(utilityInstance):
    utilityInstance.select_item(files.renamed_file_name,True)
    download_button = utilityInstance.wait_for_element(locators.action_bar_button_selector("Download"))
 
    download_button.click()
    
    sleep(6)
    assert files.renamed_file_name+".pdf" in os.listdir(r"C:\Users\Sathvik Malgikar\Downloads")


"""
## Test function to remove multiple files in the Google Drive web GUI.
"""


def test_remove_multiple_files(utilityInstance):
    utilityInstance.click_on_home_button()
    sleep(2)
    for file in files.fileCollection:
        try:
            utilityInstance.select_item( file , True)
            utilityInstance.delete_file( )
        except FileNotFoundError as e:
            assert False, repr(e)
            
        finally:
            utilityInstance.driver.refresh()
    




def test_copy_file(utilityInstance):
    utilityInstance.select_item( files.file_name_for_copy,show_more_needed=True)
    utilityInstance.context_click()
    sleep(5)

    make_a_copy_element = utilityInstance.wait_to_click(locators.make_a_copy_element_locator)
    make_a_copy_element.click()

    sleep(5)
    utilityInstance.driver.refresh()
    sleep(7)
    copied_file_element = utilityInstance.wait_for_element(locators.copied_file_locator)
    assert copied_file_element is not None

def test_move_file(utilityInstance):

    utilityInstance.select_item(files.file_move_name, show_more_needed=True)
    
    file_element = utilityInstance.wait_for_element(locators.file_move_locator)
    destination_folder_element = utilityInstance.wait_for_element(locators.file_selector(files.destination_folder_name))
    utilityInstance.drag_and_drop_element(file_element, destination_folder_element)
    
    sleep(5)

    try:
        destination_folder_element = utilityInstance.wait_to_click(
          locators.file_selector(files.destination_folder_name))
        utilityInstance.double_click_element(destination_folder_element)
        sleep(4)
    except EXC.StaleElementReferenceException:
        print("StaleElementReferenceException occurred. Retrying...")

    file_in_destination = utilityInstance.wait_for_element(locators.file_move_locator)
    assert file_in_destination is not None, "File has not been moved successfully to the destination folder"
    my_drive_button = utilityInstance.wait_to_click(locators.my_drive_button_locator)
    my_drive_button.click()
    sleep(3)
    moved_file_element = utilityInstance.wait_for_element(locators.file_move_locator)
    assert not moved_file_element, "File is still present in the old folder"   

def test_move_multiple_files(utilityInstance, button_clicker):
    file_destination_pairs = [
        ("test.txt", "After_rename"),
        ("test2.txt", "After_rename"),
        ("test3.txt", "F1"),
    ]
    show_more_needed=True
    for idx, (filename, destination_folder) in enumerate(file_destination_pairs):
        try:
            utilityInstance.move_action(filename, destination_folder,show_more_needed)
            utilityInstance.verify_file_in_destination(filename, destination_folder)
            button_clicker.click_left_menu_page_buttons("My Drive")
            assert not utilityInstance.wait_for_element(locators.file_selector(filename))

            if idx==0:
                    show_more_needed=False
        except Exception as e:
            print(f"Move operation failed for file '{filename}' to folder '{destination_folder}': {e}")
            # Continue to next move even if current move fails
            continue


def test_view_file_info(utilityInstance):  
    utilityInstance.select_item(files.view_info_file_name,True)  
    autoGUIutils.view_shortcut()
    
    sleep(2)
         
    element = utilityInstance.wait_to_click(locators.file_info_dialog_locator)
    if not element:
        
        assert False, f"File info dialog for {files.view_info_file_name} is not visible"
    else:
        utilityInstance.click_element(element)


def test_delete_file_permanently(utilityInstance):
    utilityInstance.driver.refresh()
    sleep(5)    
    utilityInstance.select_item( files.delete_forever_file_name,True)
    utilityInstance.delete_file( )    
    utilityInstance.click_trash_button()
    
    deleted_file_locator = locators.file_selector(files.delete_forever_file_name)
    utilityInstance.wait_for_element(deleted_file_locator)
      
    utilityInstance.select_item( files.delete_forever_file_name, show_more_needed=False)    
    delete_forever_btn_element=utilityInstance.wait_for_element(locators.action_bar_button_selector("Delete forever")) 
    delete_forever_btn_element.click()  
    sleep(2)    
    try:
        delete_confirm_btn_element = utilityInstance.wait_for_element(locators.delete_confirm_button_locator) 
        utilityInstance.click_element(delete_confirm_btn_element) 
        sleep(3)
    except:
        assert False, "Error occured"
    else:
        assert True, f"{files.delete_forever_file_name} is permanently deleted"


def test_share_via_link(utilityInstance):
    utilityInstance.click_on_home_button()
    sleep(2)
    utilityInstance.select_item(files.share_file,True)
    sleep(3)
    share_button = utilityInstance.wait_for_element(locators.action_bar_button_selector("Share"))
    share_button.click()
    
    sleep(5)
    
    autoGUIutils.press_tab()
    sleep(0.4)
    autoGUIutils.press_tab()
    sleep(0.4)
    autoGUIutils.press_tab()
    sleep(0.4)
    autoGUIutils.press_enter()
    sleep(0.4)
    autoGUIutils.go_back_esc()
    
    sleep(6)
    assert True
    
    
 
def test_search_for_file_by_name(utilityInstance, button_clicker):
    button_clicker.click_on_search_in_drive()
    autoGUIutils.type_into_dialogue_box(files.file_to_be_searched)
    file_element = utilityInstance.wait_to_click(locators.file_selector(files.file_to_be_searched))
    # Extract file names from file elements
    file_names = [element.text for element in files.file_elements]
    sleep(4)
    # Write file names to a text file
    with open("file_names.txt", "w") as file:
        for name in file_names:
            file.write(name + "\n")
    assert len(file_names) > 0




def test_search_file_by_type(utilityInstance, button_clicker):
    button_clicker.click_on_left_menu_page_buttons("My Drive")
    button_clicker.click_on_type_button()
    button_clicker.click_on_the_required_type()
    file_element = utilityInstance.wait_to_click(locators.file_selector(files.file_to_be_searched_by_type))
    # Extract file names from file elements
    file_names = [element.text for element in files.file_elements]
    sleep(4)
    # Write file names to a text file
    with open("file_names.txt", "w") as file:
        for name in file_names:
            file.write(name + "\n")
    assert len(file_names) > 0

def test_remove_folder(utilityInstance, button_clicker):
    button_clicker.click_left_menu_page_buttons("Home")
    button_clicker.click_on_folders_button()
    utilityInstance.select_item(files.folder_name_to_be_removed, False)
    button_clicker.click_action_bar_button("Move to trash")   
    sleep(4)

     


"""
## Test function to logout from the Google Drive web GUI.
"""
def test_logout(utilityInstance):     
    user_profile_button_element = utilityInstance.wait_for_element(locators.user_profile_button_locator)
    utilityInstance.click_element(user_profile_button_element)
    sleep(2)
    try:
        sign_out_button_element = utilityInstance.wait_for_element(locators.sign_out_button_locator)
        sign_out_button_element.click()
    except Exception as e:
        print("error occured ",e)
        
    # Assert that the login screen is visible after logging out
    assert utilityInstance.driver.title == "Home - Google Drive"
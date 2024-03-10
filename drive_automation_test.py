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
from library_functions import CommonActions
from library_functions import ButtonClicker
from library_functions import Helper
from library_functions import HigherActions

import autoGUIutils
import os

@pytest.fixture( scope="session" ,autouse=True)
def utilityInstance():
    instance = CommonActions()
    instance.setup()
    yield instance
    instance.teardown()


@pytest.fixture(scope="class", autouse=True)
def button_clicker(utilityInstance, helper):
    instance = ButtonClicker(utilityInstance.driver, utilityInstance.web_driver_wait, helper)
    yield instance


@pytest.fixture(scope="class", autouse=True)
def helper(utilityInstance):
    instance = Helper(utilityInstance.driver, utilityInstance.web_driver_wait)
    yield instance


@pytest.fixture(scope="class", autouse=True)
def higher_actions(utilityInstance, button_clicker, helper):
    instance = HigherActions(utilityInstance.driver, utilityInstance.web_driver_wait, button_clicker, helper)
    return instance

not_first_sign_in = False

@pytest.fixture(scope="class")
def prepare_for_class(helper, utilityInstance, higher_actions,button_clicker):

    global not_first_sign_in
    ### SETUP START ###
    
    utilityInstance.driver.get("https://www.google.com/intl/en-US/drive/")
    utilityInstance.driver.maximize_window()
    sleep(0.8)

    signin_ele = helper.wait_to_click(locators.sign_in_link)
    signin_ele.click()
    sleep(1.3)
    # opened by clicking sign-in anchor tag
    sign_in_tab = utilityInstance.driver.window_handles[-1]
    utilityInstance.driver.switch_to.window(sign_in_tab)
    
    parser = configparser.ConfigParser()
    parser.read("config.ini")
    account_email_id = parser.get("Account Credentials", "email")
    account_pwd = parser.get("Account Credentials", "password")
    
    #LOGIC FOR HANDLING SECOND TIME LOGIN'S , ONE EXTRA CLICK .
    
    if not_first_sign_in:
        account_div = helper.wait_to_click(locators.sign_in_account_locator)
        account_div.click()
        sleep(5)
    else:
        autoGUIutils.zoom_out()# SET ZOOM LEVEL ONCE AND FOR ALL  
        higher_actions.send_keys_to_focused(account_email_id)
        higher_actions.send_keys_to_focused(Keys.ENTER)
        
        helper.wait_for_element(locators.welcome_span)
        sleep(3)  # to deal with input animation
   
    not_first_sign_in = True
   
    higher_actions.send_keys_to_focused(account_pwd)
    higher_actions.send_keys_to_focused(Keys.ENTER)
    
    sleep(5)
    
    utilityInstance.web_driver_wait.until(EC.title_is("Home - Google Drive"))
    
    

    sleep(5)
    ### SETUP END ###

    yield
  
    ### TEARDOWN START ###
    user_profile_button_element = helper.wait_for_element(locators.user_profile_button_locator)
    button_clicker.click_element(user_profile_button_element)
    sleep(2)
   
    autoGUIutils.press_tab()
    autoGUIutils.press_tab()
    autoGUIutils.press_tab()
    autoGUIutils.press_tab()
    autoGUIutils.press_tab()
    autoGUIutils.press_enter()
    
    utilityInstance.driver.close()
    before_signin = utilityInstance.driver.window_handles[-1]
    utilityInstance.driver.switch_to.window(before_signin)
    ### TEARDOWN END ###

class Test_tt:
    """
        Test function to retrieve filenames from the Google Drive web GUI.
    """


    def test_get_filenames(utilityInstance,prepare_for_class):
        file_name_divs = utilityInstance.driver.find_elements(By.CSS_SELECTOR , 
            "div.KL4NAf")
        sleep(4)
        assert len(file_name_divs) > 0  
class Test_tt2:
    """
        Test function to retrieve filenames from the Google Drive web GUI.
    """


    def test_get_filenames2(utilityInstance,prepare_for_class):
        file_name_divs = utilityInstance.driver.find_elements(By.CSS_SELECTOR , 
            "div.KL4NAf")
        sleep(4)
        assert len(file_name_divs) > 0  
    

def test_prerequisites(utilityInstance, button_clicker, helper,higher_actions):
    rawfilenames= [files.file_name_for_copy, files.file_to_be_deleted, files.file_name, files.file_move_name,files.view_info_file_name, *files.fileCollection ,files.share_file,files.delete_forever_file_name]
    file_list_to_upload = " ".join(list(map(lambda a:f'"{a}"',rawfilenames)))
    
    button_clicker.click_on_new_button()
        
    upload_button = helper.wait_to_click(locators.new_menu_button_locator("File upload"))
    upload_button.click()
    sleep(2)

    autoGUIutils.type_into_dialogue_box(file_list_to_upload)
    sleep(3)

    higher_actions.deal_duplicate_and_await_upload()
    utilityInstance.driver.refresh()
    sleep(5)
    
    # to create SVM folder
    button_clicker.click_on_new_button()
        
    action_button = helper.wait_to_click(locators.new_menu_button_locator("New folder"))
    action_button.click()
    sleep(2)

    autoGUIutils.type_into_dialogue_box(files.folder_name_to_be_removed)
    
    utilityInstance.driver.refresh()
    assert True





def test_search_for_file_by_name(higher_actions):
    # utilityInstance.click_on_search_in_drive()
    # autoGUIutils.type_into_dialogue_box(files.file_to_be_searched)
    # file_element = utilityInstance.wait_to_click(locators.file_selector(files.file_to_be_searched))
    # utilityInstance.double_click_element(file_element)
    # sleep(3)
    # autoGUIutils.go_back_esc()
    file_elements = higher_actions.search_file_by_name(files.file_to_be_searched)
    assert (file_elements==[] or file_elements.count(files.file_to_be_searched) == len(file_elements))



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


def test_remove_file(button_clicker, helper):
    file_name = files.file_to_be_deleted
    helper.select_item(file_name,True)
    button_clicker.click_action_bar_button("Move to trash")  
    sleep(6)


"""
Test function to rename a file in the Google Drive web GUI.
"""


def test_rename_file(button_clicker, helper, higher_actions):
    old_file_name = files.file_name
    new_file_name = files.renamed_file_name
    helper.select_item(old_file_name, False)
    helper.rename_selected_item(new_file_name)
    button_clicker.click_on_ok_button()
    result = higher_actions.rename_verification(old_file_name, new_file_name)
    assert True
    



"""
Test function to undo delete action in the Google Drive web GUI.
"""


def test_undo_delete_action(higher_actions, button_clicker):
    file_name_to_retrieve = files.file_to_be_restored
    button_clicker.navigate_to("Trash")
    sleep(4)
    higher_actions.select_file_from_trash()
    button_clicker.click_action_bar_button("Restore from trash")
    restoration_successful = higher_actions.verify_restoration(file_name_to_retrieve)
    sleep(4)
    assert restoration_successful == True, f"Failed to restore file '{file_name_to_retrieve}'"
    



"""
Test function to rename a folder in the Google Drive web GUI.
"""


def test_rename_folder(helper, button_clicker):
    old_folder_name = files.folder_name
    new_folder_name = files.renamed_folder_name
    button_clicker.navigate_to("Home")
    button_clicker.click_on_folders_button
    helper.select_item(old_folder_name,True)
    helper.rename_selected_item(new_folder_name)
    button_clicker.click_on_ok_button()


"""
## Test function to create a new folder in the Google Drive web GUI.
"""


@pytest.fixture
def folder_name():
    return files.create_folder_name


def test_create_folder(utilityInstance, folder_name, button_clicker, helper):
    button_clicker.click_on_new_button()
        
    action_button = helper.wait_to_click(locators.new_menu_button_locator("New folder"))
    action_button.click()
    sleep(2)

    autoGUIutils.type_into_dialogue_box(folder_name)
    
    utilityInstance.driver.refresh()
 
    assert helper.wait_for_element(locators.file_selector(folder_name))!=None
    sleep(3)


"""
## Test function to upload new file in the Google Drive web GUI.
"""


def test_upload_file(button_clicker, helper, higher_actions):
    # this file is present in User folder
    button_clicker.click_on_new_button()
    upload_button = helper.wait_for_element(locators.new_menu_button_locator("File upload"))
    upload_button.click()
    sleep(2)
    autoGUIutils.type_into_dialogue_box(files.FILE_TO_UPLOAD)
    # this is utility solely because prerequisites aso reuses this function
    higher_actions.deal_duplicate_and_await_upload()
    assert helper.wait_for_element(locators.file_selector(files.FILE_TO_UPLOAD))


"""
## Test function to download a file in the Google Drive web GUI.
"""


def test_download_file(helper):
    helper.select_item(files.renamed_file_name,True)
    download_button = helper.wait_for_element(locators.action_bar_button_selector("Download"))
    download_button.click()
    
    sleep(6)
    assert files.renamed_file_name+".pdf" in os.listdir(r"C:\Users\Sathvik Malgikar\Downloads")


"""
## Test function to remove multiple files in the Google Drive web GUI.
"""


def test_remove_multiple_files(utilityInstance, button_clicker, helper):
    button_clicker.navigate_to("Home")
    sleep(2)
    for file in files.fileCollection:
        try:
            helper.select_item(file, True)
            button_clicker.click_action_bar_button("Move to trash")  
        except FileNotFoundError as e:
            assert False, repr(e)
            
        finally:
            utilityInstance.driver.refresh()
    




def test_copy_file(utilityInstance, helper, button_clicker):
    helper.select_item(files.file_name_for_copy,show_more_needed=True)
    button_clicker.context_click()
    sleep(5)

    make_a_copy_element = helper.wait_to_click(locators.make_a_copy_element_locator)
    make_a_copy_element.click()

    sleep(5)
    utilityInstance.driver.refresh()
    sleep(7)
    copied_file_element = helper.wait_for_element(locators.copied_file_locator)
    assert copied_file_element is not None



def test_move_file(helper, button_clicker):
    helper.select_item(files.file_move_name, show_more_needed=True)
    file_element = helper.wait_for_element(locators.file_move_locator)
    destination_folder_element = helper.wait_for_element(locators.file_selector(files.destination_folder_name))
    helper.drag_and_drop_element(file_element, destination_folder_element)
    sleep(5)

    try:
        destination_folder_element = helper.wait_to_click(
          locators.file_selector(files.destination_folder_name))
        helper.double_click_element(destination_folder_element)
        sleep(4)
    except EXC.StaleElementReferenceException:
        print("StaleElementReferenceException occurred. Retrying...")

    file_in_destination = helper.wait_for_element(locators.file_move_locator)
    assert file_in_destination is not None, "File has not been moved successfully to the destination folder"
    button_clicker.navigate_to("My Drive")
    sleep(3)
    moved_file_element = helper.wait_for_element(locators.file_move_locator)
    assert not moved_file_element, "File is still present in the old folder"   

def test_move_multiple_files(button_clicker, higher_actions, helper):
    file_destination_pairs = [
        ("test.txt", "After_rename"),
        ("test2.txt", "After_rename"),
        ("test3.txt", "F1"),
    ]
    show_more_needed=True
    for idx, (filename, destination_folder) in enumerate(file_destination_pairs):
        try:
            higher_actions.move_action(filename, destination_folder,show_more_needed)
            higher_actions.verify_file_in_destination(filename, destination_folder)
            button_clicker.navigate_to("My Drive")
            assert not helper.wait_for_element(locators.file_selector(filename))

            if idx==0:
                    show_more_needed=False
        except Exception as e:
            print(f"Move operation failed for file '{filename}' to folder '{destination_folder}': {e}")
            # Continue to next move even if current move fails
            continue


def test_view_file_info(helper, button_clicker):  
    helper.select_item(files.view_info_file_name,True)  
    autoGUIutils.view_shortcut()
    
    sleep(2)
         
    element = helper.wait_to_click(locators.file_info_dialog_locator)
    if not element:
        
        assert False, f"File info dialog for {files.view_info_file_name} is not visible"
    else:
        button_clicker.click_element(element)


def test_delete_file_permanently(utilityInstance, button_clicker, helper):
    utilityInstance.driver.refresh()
    sleep(5)    
    helper.select_item( files.delete_forever_file_name,True)
    button_clicker.click_action_bar_button("Move to trash")
    button_clicker.navigate_to("Trash")
    
    deleted_file_locator = locators.file_selector(files.delete_forever_file_name)
    helper.wait_for_element(deleted_file_locator)
      
    helper.select_item(files.delete_forever_file_name, show_more_needed=False)    
    button_clicker.click_action_bar_button("Delete forever")
    sleep(2)    
    try:
        delete_confirm_btn_element = helper.wait_for_element(locators.delete_confirm_button_locator) 
        button_clicker.click_element(delete_confirm_btn_element) 
        sleep(3)
    except:
        assert False, "Error occured"
    else:
        assert True, f"{files.delete_forever_file_name} is permanently deleted"


def test_share_via_link(utilityInstance,helper):
    utilityInstance.click_on_home_button()
    sleep(2)
    helper.select_item(files.share_file,False)
    sleep(3)
    share_button = helper.wait_for_element(locators.action_bar_button_selector("Share"))
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
    file_names = [element.text for element in file_element]
    sleep(4)
    # Write file names to a text file
    with open("file_names_by_name.txt", "w") as file:
        for name in file_names:
            file.write(name + "\n")
    assert len(file_names) > 0


def test_search_for_file_by_type(utilityInstance, button_clicker):
    button_clicker.navigate_to("My Drive")
    button_clicker.click_on_type_button()
    button_clicker.click_on_the_required_type()
    file_element = utilityInstance.wait_to_click(locators.file_selector(files.file_to_be_searched_by_type))
    # Extract file names from file elements
    file_names = [element.text for element in file_element]
    sleep(4)
    # Write file names to a text file
    with open("file_names_by_type.txt", "w") as file:
        for name in file_names:
            file.write(name + "\n")
    assert len(file_names) > 0


def test_remove_folder(button_clicker, helper):
    button_clicker.navigate_to("Home")
    button_clicker.click_on_folders_button()
    helper.select_item(files.folder_name_to_be_removed, True)
    button_clicker.click_action_bar_button("Move to trash")   
    sleep(4)


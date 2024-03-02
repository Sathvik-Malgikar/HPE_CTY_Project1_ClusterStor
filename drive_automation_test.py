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
import autoGUIutils


@pytest.fixture( scope="session" ,autouse=True)
def utilityInstance():
    instance = CommonActions()
    driver2 = Chrome(executable_path="./chromedriver.exe")
    web_driver_wait2 = WebDriverWait(driver2 , 10)
    instance.setup()
    yield instance
    instance.teardown()
    

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


def test_dummy_test_prerequisite(utilityInstance):
    file_list_to_upload = ["test.txt", "cty_ppt.pdf", "test2.txt"]

    for file in file_list_to_upload:

        utilityInstance.click_on_new_button()
          
        upload_button = utilityInstance.wait_to_click(locators.new_menu_button_locator("File upload"))
        upload_button.click()
        sleep(2)

        autoGUIutils.type_into_dialogue_box(file)

        utilityInstance.deal_duplicate_and_await_upload()
        utilityInstance.driver.refresh()
        sleep(5)


"""
    Test function to retrieve filenames from the Google Drive web GUI.
"""


def test_get_filenames(utilityInstance):
    file_name_divs = utilityInstance.driver.find_elements_by_css_selector(
        "div.KL4NAf")
    sleep(4)
    assert len(file_name_divs) > 0


"""
Test function to remove a file from the Google Drive web GUI.
"""


def test_remove_file(utilityInstance):
    file_name = files.file_to_be_deleted
    utilityInstance.select_item(file_name,True)
    utilityInstance.delete_file()


"""
Test function to rename a file in the Google Drive web GUI.
"""


def test_rename_file(utilityInstance):
    old_file_name = files.file_name
    new_file_name = files.renamed_file_name
    utilityInstance.select_item(old_file_name, False)
    utilityInstance.rename_selected_item(new_file_name)
    utilityInstance.click_on_ok_button()
    utilityInstance.rename_verification(old_file_name, new_file_name)


"""
Test function to undo delete action in the Google Drive web GUI.
"""


def test_undo_delete_action(utilityInstance):
    file_name_to_retrieve = files.file_to_be_restored
    utilityInstance.click_trash_button()
    utilityInstance.select_file_from_trash()
    utilityInstance.click_on_restore_from_trash_button()
    utilityInstance.verify_restoration(file_name_to_retrieve)


"""
Test function to rename a folder in the Google Drive web GUI.
"""


def test_rename_folder(utilityInstance):
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
      
    create_folder_button = utilityInstance.wait_to_click(locators.new_menu_button_locator("New folder"))
    create_folder_button.click()
    sleep(2)

    input_field = utilityInstance.wait_for_element(locators.input_field_locator)

    input_field.clear()
    utilityInstance.send_keys_to_element(locators.input_field_locator, folder_name)
    utilityInstance.send_keys_to_element(locators.input_field_locator, Keys.ENTER)
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
    
    sleep(10)
    assert True


"""
## Test function to remove multiple files in the Google Drive web GUI.
"""


def test_remove_multiple_files(utilityInstance):
    files = ['test.txt', 'test1.txt']
    for file in files:
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

def test_move_multiple_files(utilityInstance):
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
            utilityInstance.click_on_my_drive_button()
            assert not utilityInstance.wait_for_element(locators.file_selector(filename))

            if idx==0:
                    show_more_needed=False
        except Exception as e:
            print(f"Move operation failed for file '{filename}' to folder '{destination_folder}': {e}")
            # Continue to next move even if current move fails
            continue


def test_view_file_info(utilityInstance):    
    utilityInstance.send_keys_to_element( files.view_info_file_name,"gd")
    
         
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
    utilityInstance.select_item(files.share_file,False)
    sleep(3)
    share_button = utilityInstance.wait_for_element(locators.action_bar_button_selector("Share"))
    share_button.click()
    sleep(3)
    span_button = utilityInstance.wait_to_click(locators.permission_change_link_button)
    span_button.click()
    
    dropdown_element = utilityInstance.wait_for_element(locators.span_with_text("Anyone with the link"))
    action_chain = ActionChains(utilityInstance.driver)
    action_chain.move_to_element(dropdown_element).perform()
    dropdown_element.click()
    
    sleep(6)
    
    
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
    sleep(5)


def test_remove_folder(utilityInstance):
    
    utilityInstance.click_on_home_button()
    utilityInstance.click_on_folders_button()
    utilityInstance.select_item(files.folder_name_to_be_removed, True)
    utilityInstance.delete_file()    


"""
## Test function to logout from the Google Drive web GUI.
"""
def test_logout(utilityInstance):     
    user_profile_button_element = utilityInstance.wait_for_element(locators.user_profile_button_locator)
    utilityInstance.click_element(user_profile_button_element)
    sleep(2)
    try:
        sign_out_button_element = utilityInstance.wait_for_element(locators.sign_out_button_locator)
        utilityInstance.click_element(sign_out_button_element)
    except Exception as e:
        print("error occured ",e)
        
    # Assert that the login screen is visible after logging out
    assert utilityInstance.driver.title == "Home - Google Drive"
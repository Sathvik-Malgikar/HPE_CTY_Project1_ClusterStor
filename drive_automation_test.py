import configparser
from time import sleep
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import locators
import files

from library_functions import ButtonClicker
from library_functions import Helper
from library_functions import HigherActions

from utilities import CommonActions
from utilities import ButtonClicker
import autoGUIutils
import os

# @pytest.fixture( scope="session" ,autouse=True)
# def utilityInstance():
#     instance = CommonActions()
#     instance.setup()
#     yield instance
#     instance.teardown()


@pytest.fixture(scope="class", autouse=True)
def button_clicker(utilityInstance, helper):
    instance = ButtonClicker(utilityInstance.driver, utilityInstance.web_driver_wait, helper)
    yield instance


@pytest.fixture(scope="class", autouse=True)
def helper(utilityInstance):
    instance = Helper(utilityInstance.driver, utilityInstance.web_driver_wait)
@pytest.fixture(scope="function", autouse=True)
def button_clicker(utilityInstance):
    instance = ButtonClicker(utilityInstance.driver, utilityInstance.web_driver_wait)
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
    print("Sending email")
    utilityInstance.send_keys_to_focused(account_email_id)
    utilityInstance.send_keys_to_focused(Keys.ENTER)
    
    utilityInstance.wait_for_element( locators.welcome_span)
    sleep(3)  # to deal with input animation
   
    not_first_sign_in = True
   
    higher_actions.send_keys_to_focused(account_pwd)
    higher_actions.send_keys_to_focused(Keys.ENTER)
    account_pwd = parser.get("Account Credentials", "password")
    print(account_pwd)
    utilityInstance.send_keys_to_focused(account_pwd)
    utilityInstance.send_keys_to_focused(Keys.ENTER)
    
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


def test_prerequisites(utilityInstance, button_clicker, helper,higher_actions):
    rawfilenames= [files.file_name_for_copy, files.file_to_be_deleted, files.file_name, files.file_move_name,files.view_info_file_name, *files.fileCollection ,files.share_file,files.delete_forever_file_name]
    file_list_to_upload = " ".join(list(map(lambda a:f'"{a}"',rawfilenames)))


def test_dummy_test_prerequisite(utilityInstance):
    file_list_to_upload = [files.file_name_for_copy, "cty_ppt.pdf", files.file_move_name,files.view_info_file_name]
    

    for file in file_list_to_upload:

        utilityInstance.click_on_new_button()
          
        upload_button = utilityInstance.wait_to_click(locators.new_menu_button_locator("File upload"))
        upload_button.click()
        sleep(2)

    autoGUIutils.type_into_dialogue_box(file_list_to_upload)
    sleep(3)
        autoGUIutils.type_into_dialogue_box(file)

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


@pytest.fixture
def file_actions(helper, button_clicker,higher_actions,utilityInstance,prepare_for_class):
    """
    Fixture to provide an instance of the TestFolderActions class.
    """
    instance = TestfolderActions()  # Create the instance
    instance.helper = helper
    instance.button_clicker = button_clicker
    instance.higher_actions=higher_actions
    instance.utilityInstance=utilityInstance
    instance.prepare_for_class = prepare_for_class
    return instance



"""
    Test function to retrieve filenames from the Google Drive web GUI.
"""
class TestfileActions:
   
    def test_get_filenames(self,file_actions):
        file_name_divs = file_actions.utilityInstance.driver.find_elements(By.CSS_SELECTOR , 
            "div.KL4NAf")
        sleep(4)
        assert len(file_name_divs) > 0

    def test_search_for_file_by_name(self,file_actions):

        file_elements = file_actions.higher_actions.search_file_by_name(files.file_to_be_searched)
        assert (file_elements==[] or file_elements.count(self.files.file_to_be_searched) == len(file_elements))

        
    def test_search_for_file_by_type(self,file_actions):
        file_actions.button_clicker.navigate_to("My Drive")
        file_actions.button_clicker.click_on_type_button()
        file_actions.button_clicker.click_on_the_required_type()
        file_elements = file_actions.utilityInstance.driver.find_elements_by_css_selector("div.KL4NAf") 
        # Extract file names from file elements
        file_names = [element.text for element in file_elements]
        sleep(4)
        # Write file names to a text file
        with open("file_names_by_type.txt", "w") as file:
            for name in file_names:
                file.write(name + "\n")
        assert len(file_names) > 0

    """
    Test function to remove a file from the Google Drive web GUI.
    """


    def test_remove_file(self,file_actions):
        file_name = files.file_to_be_deleted
        file_actions.helper.select_item(file_name,True)
        file_actions.button_clicker.click_action_bar_button("Move to trash")  
        sleep(6)
        assert not file_actions.helper.wait_for_element(locators.file_selector(file_name)) 



    """
    ## Test function to remove multiple files in the Google Drive web GUI.
    """


    def test_remove_multiple_files(self,file_actions):
        file_actions.button_clicker.navigate_to("Home")
        sleep(2)
        for file in files.fileCollection:
            try:
                file_actions.helper.select_item(file, True)
                file_actions.button_clicker.click_action_bar_button("Move to trash")
                #assert not file_actions.helper.wait_for_element(locators.file_selector(file))  
            except FileNotFoundError as e:
                assert False, repr(e)
                
            finally:
                file_actions.utilityInstance.driver.refresh()
        

    
    def test_move_file(self,file_actions):

        filename=files.file_move_name
        destination_folder=files.destination_folder_name
        file_actions.higher_actions.move_action(filename,destination_folder,show_more=True)
        file_actions.higher_actions.verify_file_in_destination(filename,destination_folder)  
        file_actions.button_clicker.navigate_to("My Drive")
        assert not file_actions.helper.wait_for_element(locators.file_selector(filename)) 

    def test_move_multiple_files(self,file_actions):
        file_destination_pairs = [
            ("test.txt", "After_rename"),
            ("test2.txt", "After_rename"),
            ("test3.txt", "F1"),
        ]
        show_more_needed=True
        for idx, (filename, destination_folder) in enumerate(file_destination_pairs):
            try:
                file_actions.higher_actions.move_action(filename, destination_folder,show_more_needed)
                file_actions.higher_actions.verify_file_in_destination(filename, destination_folder)
                file_actions.button_clicker.navigate_to("My Drive")
                assert not file_actions.helper.wait_for_element(locators.file_selector(filename))

                if idx==0:
                        show_more_needed=False
            except Exception as e:
                print(f"Move operation failed for file '{filename}' to folder '{destination_folder}': {e}")
                # Continue to next move even if current move fails
                continue
def test_remove_file(utilityInstance):
    file_name = files.file_to_be_deleted
    utilityInstance.select_item(file_name,True)
    utilityInstance.delete_file()


    """
    Test function to rename a file in the Google Drive web GUI.
    """


    def test_rename_file(self,file_actions):
        old_file_name = files.file_name
        new_file_name = files.renamed_file_name
        file_actions.helper.select_item(old_file_name, True)
        file_actions.helper.rename_selected_item(new_file_name)
        file_actions.button_clicker.click_on_ok_button()
        result = file_actions.higher_actions.rename_verification(old_file_name, new_file_name)
        assert result, "Rename failed"
    

def test_rename_file(utilityInstance, button_clicker):
    old_file_name = files.file_name
    new_file_name = files.renamed_file_name
    utilityInstance.select_item(old_file_name, False)
    utilityInstance.rename_selected_item(new_file_name)
    button_clicker.click_button(locators.ok_button_locator)
    utilityInstance.rename_verification(old_file_name, new_file_name)


    """
    Test function to undo delete action in the Google Drive web GUI.
    """


    def test_undo_delete_action(self,file_actions):
        file_name_to_retrieve = files.file_to_be_restored
        file_actions.button_clicker.navigate_to("Trash")
        sleep(4)
        file_actions.higher_actions.select_item(file_name_to_retrieve,True)
        file_actions.button_clicker.click_action_bar_button("Restore from trash")
        restoration_successful = file_actions.higher_actions.verify_restoration(file_name_to_retrieve)
        sleep(4)
        assert restoration_successful == True, f"Failed to restore file '{file_name_to_retrieve}'"
        
def test_undo_delete_action(utilityInstance, button_clicker):
    file_name_to_retrieve = files.file_to_be_restored
    button_clicker.click_left_menu_page_buttons("Trash")
    sleep(4)
    utilityInstance.select_file_from_trash()
    button_clicker.click_action_bar_button("Restore from trash")
    restoration_successful = utilityInstance.verify_restoration(file_name_to_retrieve)
    assert restoration_successful == True, f"Failed to restore file '{file_name_to_retrieve}'"
    

    

    def test_upload_file(self,file_actions):
        # this file is present in User folder
        file_actions.button_clicker.click_on_new_button()
        upload_button = file_actions.helper.wait_for_element(locators.new_menu_button_locator("File upload"))
        upload_button.click()
        sleep(2)
        autoGUIutils.type_into_dialogue_box(files.FILE_TO_UPLOAD)
        # this is utility solely because prerequisites aso reuses this function
        file_actions.higher_actions.deal_duplicate_and_await_upload()
        assert file_actions.helper.wait_for_element(locators.file_selector(files.FILE_TO_UPLOAD))
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


    def test_download_file(self,file_actions):
        file_actions.helper.select_item(files.renamed_file_name,True)
        download_button = file_actions.helper.wait_for_element(locators.action_bar_button_selector("Download"))
        download_button.click()
        
        sleep(6)
        assert files.renamed_file_name+".pdf" in os.listdir(r"C:\Users\Sathvik Malgikar\Downloads")


    



    def test_copy_file(self,file_actions):
        file_actions.helper.select_item(files.file_name_for_copy,show_more_needed=True)
        file_actions.button_clicker.context_click()
        sleep(5)
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

        make_a_copy_element = file_actions.helper.wait_to_click(locators.make_a_copy_element_locator)
        make_a_copy_element.click()
    make_a_copy_element = utilityInstance.wait_to_click(locators.make_a_copy_element_locator)
    make_a_copy_element.click()

        sleep(5)
        file_actions.utilityInstance.driver.refresh()
        sleep(7)
        copied_file_element = file_actions.helper.wait_for_element(locators.copied_file_locator)
        assert copied_file_element is not None
    sleep(5)
    utilityInstance.driver.refresh()
    sleep(7)
    copied_file_element = utilityInstance.wait_for_element(locators.copied_file_locator)
    assert copied_file_element is not None




    def test_view_file_info(self,file_actions):  
        file_actions.helper.select_item(files.view_info_file_name,False)  
        autoGUIutils.view_shortcut()
        
        sleep(2)
            
        element = file_actions.helper.wait_to_click(locators.file_info_dialog_locator)
        if not element:
            
            assert False, f"File info dialog for {files.view_info_file_name} is not visible"
        else:
            file_actions.button_clicker.click_element(element)
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


    def test_delete_file_permanently(self,file_actions):
        file_actions.utilityInstance.driver.refresh()
        sleep(5)    
        file_actions.helper.select_item( files.delete_forever_file_name,False)
        file_actions.button_clicker.click_action_bar_button("Move to trash")
        file_actions.button_clicker.navigate_to("Trash")
        
        deleted_file_locator = locators.file_selector(files.delete_forever_file_name)
        file_actions.helper.wait_for_element(deleted_file_locator)
        
        file_actions.helper.select_item(files.delete_forever_file_name, show_more_needed=False)    
        file_actions.button_clicker.click_action_bar_button("Delete forever")
        sleep(2)    
        try:
            delete_confirm_btn_element = file_actions.helper.wait_for_element(locators.delete_confirm_button_locator) 
            file_actions.button_clicker.click_element(delete_confirm_btn_element) 
            sleep(3)
        except:
            assert False, "Error occured"
        else:
            assert True, f"{files.delete_forever_file_name} is permanently deleted"
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

@pytest.fixture
def folder_actions(helper, button_clicker,prepare_for_class):
    """
    Fixture to provide an instance of the TestFolderActions class.
    """
    instance = TestfolderActions()  # Create the instance
    instance.helper = helper
    instance.button_clicker = button_clicker
    instance.prepare_for_class = prepare_for_class
    return instance


class TestfolderActions:

    """
    Test function to rename a folder in the Google Drive web GUI.
    """

    def test_rename_folder(self,folder_actions,higher_actions):
        old_folder_name = files.folder_name
        new_folder_name = files.renamed_folder_name
        folder_actions.button_clicker.navigate_to("Home")
        folder_actions.button_clicker.click_on_folders_button
        folder_actions.helper.select_item(old_folder_name,True)
        folder_actions.helper.rename_selected_item(new_folder_name)
        folder_actions.button_clicker.click_on_ok_button()

        result = higher_actions.rename_verification(old_folder_name, new_folder_name)
        assert result, "Rename failed"
        

    """
    ## Test function to create a new folder in the Google Drive web GUI.
    """


    

    def test_create_folder(self,folder_actions,utilityInstance):
        folder_name=files.create_folder_name
        folder_actions.button_clicker.click_on_new_button()
            
        action_button = folder_actions.helper.wait_to_click(locators.new_menu_button_locator("New folder"))
        action_button.click()
        sleep(2)

        autoGUIutils.type_into_dialogue_box(folder_name)
        
        utilityInstance.driver.refresh()
    
        assert folder_actions.helper.wait_for_element(locators.file_selector(folder_name))!=None
        sleep(3)
    """
    ## Test function to upload new file in the Google Drive web GUI.
    """

    def test_remove_folder(self,folder_actions):
        folder_to_be_removed=files.folder_name_to_be_removed
        folder_actions.button_clicker.navigate_to("Home")
        folder_actions.button_clicker.click_on_folders_button()
        folder_actions.helper.select_item(folder_to_be_removed, True)
        folder_actions.button_clicker.click_action_bar_button("Move to trash")   
        sleep(4)
        assert not folder_actions.helper.wait_for_element(locators.file_selector(folder_to_be_removed)) 



def test_share_via_link(utilityInstance,helper,button_clicker):
    button_clicker.navigate_to("Home")
    sleep(2)
    helper.select_item(files.share_file,False)

def test_share_via_link(utilityInstance):
    utilityInstance.select_item(files.share_file,False)
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
    file_elements = utilityInstance.driver.find_elements_by_css_selector("div.KL4NAf") 
    # Extract file names from file elements
    file_names = [element.text for element in file_elements]
    sleep(4)
    # Write file names to a text file
    with open("file_names.txt", "w") as file:
        for name in file_names:
            file.write(name + "\n")
    assert len(file_names) > 0


def test_search_file_by_type(utilityInstance, button_clicker):
    utilityInstance.click_on_my_drive_button()
    button_clicker.click_on_type_button()
    button_clicker.click_on_the_required_type()
    file_elements = utilityInstance.driver.find_elements_by_css_selector("div.KL4NAf") 
    # Extract file names from file elements
    file_names = [element.text for element in file_elements]
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
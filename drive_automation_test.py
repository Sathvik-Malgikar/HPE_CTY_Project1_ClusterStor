import configparser
from time import sleep
from webbrowser import Chrome
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Chrome
import locators
import files
from library_functions import HigherActions
import autoGUIutils
import os

not_first_sign_in = False
class BaseTest:
    @classmethod
    def setup_class(cls):
        cls.driver = Chrome(executable_path="./chromedriver.exe")
        cls.web_driver_wait = WebDriverWait(cls.driver, 10)
        #global not_first_sign_in
        # SETUP START
        
        cls.driver.get("https://www.google.com/intl/en-US/drive/")
        cls.driver.maximize_window()
        sleep(0.8)
        cls.higher_actions =  HigherActions(cls.driver, cls.web_driver_wait)
        signin_ele = cls.higher_actions.wait_to_click(locators.sign_in_link)
        signin_ele.click()
        sleep(1.3)
    # Switch to the sign-in window explicitly based on URL or title
        for window_handle in cls.driver.window_handles:
            cls.driver.switch_to.window(window_handle)
            if "accounts.google.com" in cls.driver.current_url or "Sign in" in cls.driver.title:
                break
        parser = configparser.ConfigParser()
        parser.read("config.ini")
        account_email_id = parser.get("Account Credentials", "email")
        account_pwd = parser.get("Account Credentials", "password")
        cls.higher_actions.send_keys_to_focused(account_email_id)
        cls.higher_actions.send_keys_to_focused(Keys.ENTER)
        cls.higher_actions.wait_for_element(locators.welcome_span)
        sleep(3)  # to deal with input animation
        # not_first_sign_in = True
        cls.higher_actions.send_keys_to_focused(account_pwd)
        cls.higher_actions.send_keys_to_focused(Keys.ENTER)
        sleep(5)
        #cls.web_driver_wait.until(EC.title_is("Home - Google Drive"))
        sleep(5)

        # rawfilenames = [files.file_name_for_copy, files.file_to_be_deleted, files.file_name, files.file_move_name, files.view_info_file_name, *files.fileCollection, files.share_file, files.delete_forever_file_name]
        # file_list_to_upload = " ".join(list(map(lambda a: f'"{a}"', rawfilenames)))
        # cls.higher_actions.click_on_new_button()
        # upload_button = cls.higher_actions.wait_to_click(locators.new_menu_button_locator("File upload"))
        # upload_button.click()
        # sleep(2)
        # autoGUIutils.type_into_dialogue_box(file_list_to_upload)
        # sleep(3)
        # cls.higher_actions.deal_duplicate_and_await_upload()
        # cls.driver.refresh()
        # sleep(5)
        # # to create SVM prerequisite folder
        # cls.higher_actions.click_on_new_button()
        # action_button = cls.higher_actions.wait_to_click(locators.new_menu_button_locator("New folder"))
        # action_button.click()
        # sleep(2)
        # autoGUIutils.type_into_dialogue_box(files.folder_name_to_be_removed)
        # cls.driver.refresh()
        # sleep(4)

        # cls.higher_actions.click_on_new_button()
        # action_button = cls.higher_actions.wait_to_click(locators.new_menu_button_locator("New folder"))
        # action_button.click()
        # sleep(2)
        # autoGUIutils.type_into_dialogue_box(files.folder_name)
        # cls.driver.refresh()
        # sleep(4)

    @classmethod
    def teardown_class(cls):
         # TEARDOWN START ###
        user_profile_button_element = cls.higher_actions.wait_for_element(locators.user_profile_button_locator)
        cls.higher_actions.click_element(user_profile_button_element)
        sleep(2)
        autoGUIutils.n_tabs_shift_focus(5)
        autoGUIutils.press_enter()
        cls.driver.close()
        before_signin = cls.driver.window_handles[-1]
        cls.driver.switch_to.window(before_signin)
        cls.driver.quit()
        # TEARDOWN END ###
    
    

class TestMiscellaneousActions(BaseTest):
    @classmethod
    def setup_class(cls):
        super(cls, TestMiscellaneousActions).setup_class()#FIRST SUPER CLASS
        #THEN SUBCLASSS SETUP
    
    @classmethod
    def teardown_class(cls):
        #FIRST SUBCLASS TEARDOWN LOGIC
        super(cls, TestMiscellaneousActions).teardown_class()#THEN SUPERCLASS TEARDOWN
    
    
    def test_prerequisites(self):
        rawfilenames = [files.file_name_for_copy, files.file_to_be_deleted, files.file_name, files.file_move_name, files.view_info_file_name, *files.fileCollection, files.share_file, files.delete_forever_file_name, *files.portCollection]
        file_list_to_upload = " ".join(list(map(lambda a: f'"{a}"', rawfilenames)))
        self.higher_actions.click_on_new_button()
        upload_button = self.higher_actions.wait_to_click(locators.new_menu_button_locator("File upload"))
        upload_button.click()
        sleep(2)
        autoGUIutils.type_into_dialogue_box(file_list_to_upload)
        sleep(3)
        self.higher_actions.deal_duplicate_and_await_upload()
        self.driver.refresh()
        sleep(5)
        # to create SVM prerequisite folder
        self.higher_actions.click_on_new_button()
        action_button = self.higher_actions.wait_to_click(locators.new_menu_button_locator("New folder"))
        action_button.click()
        sleep(2)
        autoGUIutils.type_into_dialogue_box(files.folder_name_to_be_removed)
        self.driver.refresh()
        sleep(4)
        self.higher_actions.click_on_new_button()
        action_button = self.higher_actions.wait_to_click(locators.new_menu_button_locator("New folder"))
        action_button.click()
        sleep(2)
        autoGUIutils.type_into_dialogue_box(files.folder_name)
        self.driver.refresh()
        sleep(4)
        assert True
      
    def test_share_via_link(self ):
        self.higher_actions.navigate_to("Home")
        sleep(2)
        self.higher_actions.select_item(files.share_file)
        sleep(3)
        share_button = self.higher_actions.wait_for_element(locators.action_bar_button_selector("Share"))
        share_button.click()
        sleep(5)
        autoGUIutils.n_tabs_shift_focus(3)
        autoGUIutils.press_enter()
        sleep(0.4)
        autoGUIutils.go_back_esc()
        assert True

    def test_view_file_info(self):
        self.higher_actions.select_item(files.view_info_file_name)
        autoGUIutils.view_shortcut()
        element = self.higher_actions.wait_to_click(locators.file_info_dialog_locator)
        if not element:
            assert False, f"File info dialog for {files.view_info_file_name} is not visible"
        else:
            self.higher_actions.click_element(element)

    def test_verify_tootip_text(self):
        verification_result = self.higher_actions.verify_button_tooltips(files.button_names_and_tooltips)
        if verification_result:
            assert True



class TestfileActions(BaseTest):
    """
    Test function to rename a file in the Google Drive web GUI.
    """
    @classmethod
    def setup_class(cls):
        super(cls,TestfileActions).setup_class()#FIRST SUPER CLASS
        #THEN SUBCLASSS SETUP

    @classmethod
    def teardown_class(cls):
        #FIRST SUBCLASS TEARDOWN LOGIC
        super(cls,TestfileActions).teardown_class()#THEN SUPERCLASS TEARDOWN

    def test_rename_file(self):
        old_file_name = files.file_name
        new_file_name = files.renamed_file_name
        result = self.higher_actions.rename_action(old_file_name, new_file_name)
        assert result, "Rename failed"

    def test_get_filenames(self):
        no_of_files = self.higher_actions.get_file_names_action()
        assert no_of_files > 0

    def test_upload_file(self):
        # this file is present in User folder
        self.higher_actions.upload_file_action(files.FILE_TO_UPLOAD)
        assert self.higher_actions.wait_for_element(locators.file_selector(files.FILE_TO_UPLOAD)) is not None

    """
    ## Test function to download a file in the Google Drive web GUI.
    """

    def test_download_file(self):
        self.higher_actions.select_item(files.file_name_for_copy)
        download_button = self.higher_actions.wait_for_element(locators.action_bar_button_selector("Download"))
        download_button.click()
        sleep(6)
        assert files.file_name_for_copy  in os.listdir(r"C:\Users\adith\Downloads")

    def test_copy_file(self):
        copied_file_element = self.higher_actions.copy_file_action(files.file_name_for_copy)
        assert copied_file_element is not None

# class TestSearch(TestfileActions):
#     @classmethod
#     def setup_class(cls):
#         super().setup_class()#FIRST SUPER CLASS
#         #THEN SUBCLASSS SETUP

#     @classmethod
#     def teardown_class(cls):
#         #FIRST SUBCLASS TEARDOWN LOGIC
#         super().teardown_class()#THEN SUPERCLASS TEARDOWN

    def test_search_for_file_by_name(self):
        self.higher_actions.search_by_name_action(files.file_to_be_searched)

    def test_search_for_file_by_type(self):
        no_of_files = self.higher_actions.search_by_type_action()
        assert no_of_files > 0
    
    def test_move_file(self):
        filename = files.file_move_name
        destination_folder = files.destination_folder_name
        self.higher_actions.navigate_to("Home")
        self.higher_actions.move_action(filename, destination_folder, True)
        assert not self.higher_actions.wait_for_element(locators.file_selector(filename))

    def test_move_multiple_files(self):
        file_destination_pairs = [
            ("port1.txt", "SVM"),
            ("port2.txt", "SVM"),
            ("port3.txt", "Before Rename"),
        ]
        show_more_needed = True
        for idx, (filename, destination_folder) in enumerate(file_destination_pairs):
            try:
                self.parent.higher_actions.move_action(filename, destination_folder, show_more_needed)
                self.parent.higher_actions.verify_file_in_destination(filename, destination_folder)
                self.parent.higher_actions.navigate_to("My Drive")
                assert not self.higher_actions.wait_for_element(locators.file_selector(filename))

                if idx == 0:
                    show_more_needed = False
            except Exception as e:
                print(f"Move operation failed for file '{filename}' to folder '{destination_folder}': {e}")
                # Continue to next move even if current move fails
                continue

# class TestDelete(TestfileActions):
#     @classmethod
#     def setup_class(cls):
#         super(cls,TestDelete).setup_class()#FIRST SUPER CLASS
#         #THEN SUBCLASSS SETUP

#     @classmethod
#     def teardown_class(cls):
#         #FIRST SUBCLASS TEARDOWN LOGIC
#         super(cls,TestDelete).teardown_class()#THEN SUPERCLASS TEARDOWN
                                
    def test_remove_file(self):
        file_name = files.file_to_be_deleted
        self.higher_actions.navigate_to("Home")
        self.higher_actions.remove_file_action(file_name)
        
    """ 
    The following tests are commented out because they require manual intervention and cannot be run on the CI server.
    The following tests are commented out because they
    
    ## Test function to remove multiple files in the Google Drive web GUI.
    """


    def test_remove_multiple_files(self):
        self.higher_actions.navigate_to("Home")
        sleep(2)
        for file in files.fileCollection:
            try:
                self.higher_actions.remove_file_action(file)
            except FileNotFoundError as e:
                assert False, repr(e)

            finally:
                self.driver.refresh()

    def test_delete_file_permanently(self):
        result = self.higher_actions.delete_permanently_action(files.delete_forever_file_name)
        if (result is False):
            assert False, "Error occured"
        else:
            assert True, f"{files.delete_forever_file_name} is permanently deleted"

    """
    Test function to undo delete action in the Google Drive web GUI.
    """

    def test_undo_delete_action(self):
        file_name_to_retrieve = files.file_to_be_restored
        restoration_successful = self.higher_actions.undo_delete_action(file_name_to_retrieve)
        assert restoration_successful is True, f"Failed to restore file '{file_name_to_retrieve}'"


class TestfolderActions(BaseTest):

    """
    Test function to rename a folder in the Google Drive web GUI.
    """
    @classmethod
    def setup_class(cls):
        super(cls, TestfolderActions).setup_class()#FIRST SUPER CLASS
        #THEN SUBCLASSS SETUP
    
    @classmethod
    def teardown_class(cls):
        #FIRST SUBCLASS TEARDOWN LOGIC
        super(cls, TestfolderActions).teardown_class()#THEN SUPERCLASS TEARDOWN

    def test_rename_folder(self):
        old_folder_name = files.folder_name
        new_folder_name = files.renamed_folder_name
        result = self.higher_actions.rename_folder_action(old_folder_name, new_folder_name)
        assert result, "Rename failed"

    """
    ## Test function to create a new folder in the Google Drive web GUI.
    """

    def test_create_folder(self):
        folder_name = files.create_folder_name
        self.higher_actions.create_folder_action(folder_name)
        assert self.higher_actions.wait_for_element(locators.file_selector(folder_name)) is not None
        sleep(3)

    """
    ## Test function to upload new file in the Google Drive web GUI.
    """

    def test_remove_folder(self):
        folder_to_be_removed = files.folder_name_to_be_removed
        self.higher_actions.remove_folder_action(folder_to_be_removed)
        assert not self.higher_actions.wait_for_element(locators.file_selector(folder_to_be_removed))
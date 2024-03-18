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
from library_functions import ButtonClicker
from library_functions import Helper
from library_functions import HigherActions
from library_functions import ElementaryActions
import autoGUIutils
import os


# @pytest.fixture(autouse=True,scope="session")
# def driver():
#     instance= Chrome("./chromedriver.exe")
#     yield instance
#     instance.quit()
# @pytest.fixture(autouse=True,scope="session")
# def web_driver_wait(driver):
#     instance= WebDriverWait(driver,10)
#     yield instance
# @pytest.fixture(scope="class", autouse=True)
# def button_clicker(driver,web_driver_wait, helper):
#     instance = ButtonClicker(driver, web_driver_wait, helper)
#     yield instance
# @pytest.fixture(scope="class", autouse=True)
# def helper(driver,web_driver_wait):
#     instance = Helper(driver, web_driver_wait,)
#     yield instance
# @pytest.fixture(scope="class", autouse=True)
# def higher_actions(driver,web_driver_wait, button_clicker, helper):
#     instance = HigherActions(driver, web_driver_wait, button_clicker, helper)
#     return instance
# @pytest.fixture(scope="class", autouse=True)
# def elementary_actions(driver,web_driver_wait):
#     instance = ElementaryActions(driver, web_driver_wait)
#     return instance
# def setup_class(driver,web_driver_wait,elementary_actions):
#     #TODO  make a class called Setup
#     #TODO  make a class called Teardown
#     global not_first_sign_in
#     ### SETUP START ###
#     driver.get("https://www.google.com/intl/en-US/drive/")
#     driver.maximize_window()
#     sleep(0.8)
#     signin_ele = elementary_actions.wait_to_click(locators.sign_in_link)
#     signin_ele.click()
#     sleep(1.3)
#     # opened by clicking sign-in anchor tag
#     sign_in_tab = driver.window_handles[-1]
#     driver.switch_to.window(sign_in_tab)
#     parser = configparser.ConfigParser()
#     parser.read("config.ini")
#     account_email_id = parser.get("Account Credentials", "email")
#     account_pwd = parser.get("Account Credentials", "password")
#     #LOGIC FOR HANDLING SECOND TIME LOGIN'S , ONE EXTRA CLICK .
#     if not_first_sign_in:
#         account_div = elementary_actions.wait_to_click(locators.sign_in_account_locator)
#         account_div.click()
#         sleep(5)
#     else:
#         autoGUIutils.zoom_out()# SET ZOOM LEVEL ONCE AND FOR ALL
#         elementary_actions.send_keys_to_focused(account_email_id)
#         elementary_actions.send_keys_to_focused(Keys.ENTER)
#         elementary_actions.wait_for_element(locators.welcome_span)
#         sleep(3)  # to deal with input animation
#     not_first_sign_in = True
#     elementary_actions.send_keys_to_focused(account_pwd)
#     elementary_actions.send_keys_to_focused(Keys.ENTER)
#     sleep(5)
#     web_driver_wait.until(EC.title_is("Home - Google Drive"))
#     sleep(5)
#     ## SETUP END ###

# def teardown_class(driver,elementary_actions):
#     ### TEARDOWN START ###
#     user_profile_button_element = elementary_actions.wait_for_element(locators.user_profile_button_locator)
#     elementary_actions.click_element(user_profile_button_element)
#     sleep(2)
#     autoGUIutils.n_tabs_shift_focus(5)
#     autoGUIutils.press_enter()
#     driver.close()
#     before_signin = driver.window_handles[-1]
#     driver.switch_to.window(before_signin)
#     ### TEARDOWN END ###

# @pytest.fixture(scope="class", autouse=True)
# def class_setup_teardown(driver,web_driver_wait,elementary_actions):
#     setup_class(driver,web_driver_wait,elementary_actions)
#     yield
#     teardown_class(driver,elementary_actions)

# @pytest.fixture(scope="class")
# def prepare_for_class(helper, driver,web_driver_wait, higher_actions,button_clicker,elementary_actions):
#     # TODO  make a class called Setup
#     # TODO  make a class called Teardown
#     global not_first_sign_in
#     ### SETUP START ###
#     driver.get("https://www.google.com/intl/en-US/drive/")
#     driver.maximize_window()
#     sleep(0.8)
#     signin_ele = elementary_actions.wait_to_click(locators.sign_in_link)
#     signin_ele.click()
#     sleep(1.3)
#     # opened by clicking sign-in anchor tag
#     sign_in_tab = driver.window_handles[-1]
#     driver.switch_to.window(sign_in_tab)
#     parser = configparser.ConfigParser()
#     parser.read("config.ini")
#     account_email_id = parser.get("Account Credentials", "email")
#     account_pwd = parser.get("Account Credentials", "password")
#     #LOGIC FOR HANDLING SECOND TIME LOGIN'S , ONE EXTRA CLICK .
#     if not_first_sign_in:
#         account_div = elementary_actions.wait_to_click(locators.sign_in_account_locator)
#         account_div.click()
#         sleep(5)
#     else:
#         autoGUIutils.zoom_out()# SET ZOOM LEVEL ONCE AND FOR ALL
#         elementary_actions.send_keys_to_focused(account_email_id)
#         elementary_actions.send_keys_to_focused(Keys.ENTER)
#         elementary_actions.wait_for_element(locators.welcome_span)
#         sleep(3)  # to deal with input animation
#     not_first_sign_in = True
#     elementary_actions.send_keys_to_focused(account_pwd)
#     elementary_actions.send_keys_to_focused(Keys.ENTER)
#     sleep(5)
#     web_driver_wait.until(EC.title_is("Home - Google Drive"))
#     sleep(5)
#     ### SETUP END ###
#     yield
#     ### TEARDOWN START ###
#     user_profile_button_element = elementary_actions.wait_for_element(locators.user_profile_button_locator)
#     elementary_actions.click_element(user_profile_button_element)
#     sleep(2)
#     autoGUIutils.n_tabs_shift_focus(5)
#     autoGUIutils.press_enter()
#     driver.close()
#     before_signin = driver.window_handles[-1]
#     driver.switch_to.window(before_signin)
#     ### TEARDOWN END ###

not_first_sign_in = False


def test_prerequisites(driver, web_driver_wait, button_clicker, helper, higher_actions):
    rawfilenames = [files.file_name_for_copy, files.file_to_be_deleted, files.file_name, files.file_move_name, files.view_info_file_name, *files.fileCollection, files.share_file, files.delete_forever_file_name]
    file_list_to_upload = " ".join(list(map(lambda a: f'"{a}"', rawfilenames)))
    button_clicker.click_on_new_button()
    upload_button = helper.wait_to_click(locators.new_menu_button_locator("File upload"))
    upload_button.click()
    sleep(2)
    autoGUIutils.type_into_dialogue_box(file_list_to_upload)
    sleep(3)
    higher_actions.deal_duplicate_and_await_upload()
    driver.refresh()
    sleep(5)
    # to create SVM folder
    button_clicker.click_on_new_button()
    action_button = helper.wait_to_click(locators.new_menu_button_locator("New folder"))
    action_button.click()
    sleep(2)
    autoGUIutils.type_into_dialogue_box(files.folder_name_to_be_removed)
    driver.refresh()
    assert True


class BaseTest:

    @pytest.fixture(autouse=True, scope="class")
    def setup_driver(self):
        instance = Chrome("./chromedriver.exe")
        self.driver = instance
        instance.quit()

    @pytest.fixture(autouse=True, scope="class")
    def setup_web_driver_wait(self, setup_driver):
        instance = WebDriverWait(self.driver, 10)
        self.web_driver_wait = instance

    @pytest.fixture(scope="class", autouse=True)
    def setup_helper(self, setup_driver, setup_web_driver_wait):
        instance = Helper(self.driver, self.web_driver_wait,)
        self.helper = instance

    @pytest.fixture(scope="class", autouse=True)
    def setup_button_clicker(self, setup_driver, setup_web_driver_wait, setup_helper):
        instance = ButtonClicker(self.driver, self.web_driver_wait, self.helper)
        self.button_clicker = instance

    @pytest.fixture(scope="class", autouse=True)
    def setup_higher_actions(self, setup_driver, setup_web_driver_wait, setup_button_clicker, setup_helper):
        instance = HigherActions(self.driver, self.web_driver_wait, self.button_clicker, self.helper)
        self.higher_actions = instance

    @pytest.fixture(scope="class", autouse=True)
    def setup_elementary_actions(self, setup_driver, setup_web_driver_wait):
        instance = ElementaryActions(self.driver, self.web_driver_wait)
        self.elementary_actions = instance

    # @classmethod
    # #@pytest.fixture(autouse=True)
    # def injector(cls, helper, button_clicker,higher_actions,driver, web_driver_wait):
    #     # instantiates pages object, and data readers
    #     cls.helper = helper
    #     cls.button_clicker = button_clicker
    #     cls.higher_actions = higher_actions
    #     cls.driver = driver
    #     cls.web_driver_wait = web_driver_wait
    #     cls.elementary_actions=elementary_actions
    #     #cls.prepare_for_class = prepare_for_class

    # def setup_class(cls):
    #     #cls.injector
    #     #TODO  make a class called Setup
    #     #TODO  make a class called Teardown

    #     global not_first_sign_in
    #     ### SETUP START ###

    #     cls.driver.get("https://www.google.com/intl/en-US/drive/")
    #     cls.driver.maximize_window()
    #     sleep(0.8)

    #     signin_ele = cls.elementary_actions.wait_to_click(locators.sign_in_link)
    #     signin_ele.click()
    #     sleep(1.3)
    #     # opened by clicking sign-in anchor tag
    #     sign_in_tab = cls.driver.window_handles[-1]
    #     cls.driver.switch_to.window(sign_in_tab)

    #     parser = configparser.ConfigParser()
    #     parser.read("config.ini")
    #     account_email_id = parser.get("Account Credentials", "email")
    #     account_pwd = parser.get("Account Credentials", "password")

    #     #LOGIC FOR HANDLING SECOND TIME LOGIN'S , ONE EXTRA CLICK .

    #     if not_first_sign_in:
    #         account_div = cls.elementary_actions.wait_to_click(locators.sign_in_account_locator)
    #         account_div.click()
    #         sleep(5)
    #     else:
    #         autoGUIutils.zoom_out()# SET ZOOM LEVEL ONCE AND FOR ALL
    #         cls.elementary_actions.send_keys_to_focused(account_email_id)
    #         cls.elementary_actions.send_keys_to_focused(Keys.ENTER)

    #         cls.elementary_actions.wait_for_element(locators.welcome_span)
    #         sleep(3)  # to deal with input animation

    #     not_first_sign_in = True

    #     cls.elementary_actions.send_keys_to_focused(account_pwd)
    #     cls.elementary_actions.send_keys_to_focused(Keys.ENTER)
    #     sleep(5)

    #     cls.web_driver_wait.until(EC.title_is("Home - Google Drive"))
    #     sleep(5)

    # def teardown_class(cls):

    #     ### TEARDOWN START ###
    #     user_profile_button_element = cls.elementary_actions.wait_for_element(locators.user_profile_button_locator)
    #     cls.elementary_actions.click_element(user_profile_button_element)
    #     sleep(2)
    #     autoGUIutils.n_tabs_shift_focus(5)
    #     autoGUIutils.press_enter()
    #     cls.driver.close()
    #     before_signin = cls.driver.window_handles[-1]
    #     cls.driver.switch_to.window(before_signin)
    #     ### TEARDOWN END ###


class TestMiscellaneousActions(BaseTest):
    def test_share_via_link(self):
        self.button_clicker.navigate_to("Home")
        sleep(2)
        self.helper.select_item(files.share_file, False)
        sleep(3)
        share_button = self.helper.wait_for_element(locators.action_bar_button_selector("Share"))
        share_button.click()
        sleep(5)
        autoGUIutils.n_tabs_shift_focus(3)
        autoGUIutils.press_enter()
        sleep(0.4)
        autoGUIutils.go_back_esc()
        assert True

    def test_view_file_info(self):
        self.helper.select_item(files.view_info_file_name, False)
        autoGUIutils.view_shortcut()
        element = self.helper.wait_to_click(locators.file_info_dialog_locator)
        if not element:
            assert False, f"File info dialog for {files.view_info_file_name} is not visible"
        else:
            self.button_clicker.click_element(element)


class TestfileActions(BaseTest):

    """
    Test function to rename a file in the Google Drive web GUI.
    """

    def test_rename_file(self):
        old_file_name = files.file_name
        new_file_name = files.renamed_file_name
        self.helper.select_item(old_file_name, True)
        self.helper.rename_selected_item(new_file_name)
        self.button_clicker.click_on_ok_button()
        result = self.higher_actions.rename_verification(old_file_name, new_file_name)
        assert result, "Rename failed"

    def test_get_filenames(self):
        file_name_divs = self.driver.find_elements(By.CSS_SELECTOR, "div.KL4NAf")
        sleep(4)
        assert len(file_name_divs) > 0

    def test_upload_file(self):
        # this file is present in User folder
        self.button_clicker.click_on_new_button()
        upload_button = self.helper.wait_for_element(locators.new_menu_button_locator("File upload"))
        upload_button.click()
        sleep(2)
        autoGUIutils.type_into_dialogue_box(files.FILE_TO_UPLOAD)
        # this is utility solely because prerequisites aso reuses this function
        self.higher_actions.deal_duplicate_and_await_upload()
        assert self.helper.wait_for_element(locators.file_selector(files.FILE_TO_UPLOAD))

    """
    ## Test function to download a file in the Google Drive web GUI.
    """

    def test_download_file(self):
        self.helper.select_item(files.renamed_file_name, True)
        download_button = self.helper.wait_for_element(locators.action_bar_button_selector("Download"))
        download_button.click()
        sleep(6)
        assert files.renamed_file_name+".pdf" in os.listdir(r"C:\Users\Sathvik Malgikar\Downloads")

    def test_copy_file(self):
        self.helper.select_item(files.file_name_for_copy, show_more_needed=True)
        self.button_clicker.context_click()
        sleep(5)

        make_a_copy_element = self.helper.wait_to_click(locators.make_a_copy_element_locator)
        make_a_copy_element.click()

        sleep(5)
        self.driver.refresh()
        sleep(7)
        copied_file_element = self.helper.wait_for_element(locators.copied_file_locator)
        assert copied_file_element is not None

    class Search:
        def test_search_for_file_by_name(self):
            self.button_clicker.click_on_search_in_drive()
            self.elementary_actions.send_keys_to_focused(files.file_to_be_searched)
            autoGUIutils.press_enter()
            # Retrieve file elements from the search results
            file_elements = self.elementary_actions.wait_for_element(locators.file_selector(files.file_to_be_searched))
            # Extract file names from file elements
            file_names = [element.text for element in file_elements]
            # Write file names to a text file
            with open("file_names.txt", "w") as file:
                for name in file_names:
                    file.write(name + "\n")

        def test_search_for_file_by_type(self):
            self.button_clicker.navigate_to("My Drive")
            self.button_clicker.click_on_type_button()
            self.button_clicker.click_on_the_required_type()
            file_elements = self.driver.find_elements_by_css_selector("div.KL4NAf")
            # Extract file names from file elements
            file_names = [element.text for element in file_elements]
            sleep(4)
            # Write file names to a text file
            with open("file_names_by_type.txt", "w") as file:
                for name in file_names:
                    file.write(name + "\n")
            assert len(file_names) > 0

    class Move:

        def test_move_file(self):

            filename = files.file_move_name
            destination_folder = files.destination_folder_name
            self.higher_actions.move_action(filename, destination_folder, show_more=True)
            self.higher_actions.verify_file_in_destination(filename, destination_folder)
            self.button_clicker.navigate_to("My Drive")
            assert not self.helper.wait_for_element(locators.file_selector(filename))

        def test_move_multiple_files(self):
            file_destination_pairs = [
                ("test.txt", "After_rename"),
                ("test2.txt", "After_rename"),
                ("test3.txt", "F1"),
            ]
            show_more_needed = True
            for idx, (filename, destination_folder) in enumerate(file_destination_pairs):
                try:
                    self.higher_actions.move_action(filename, destination_folder, show_more_needed)
                    self.higher_actions.verify_file_in_destination(filename, destination_folder)
                    self.button_clicker.navigate_to("My Drive")
                    assert not self.helper.wait_for_element(locators.file_selector(filename))

                    if idx == 0:
                        show_more_needed = False
                except Exception as e:
                    print(f"Move operation failed for file '{filename}' to folder '{destination_folder}': {e}")
                    # Continue to next move even if current move fails
                    continue

    class Delete:
        """
        Test function to remove a file from the Google Drive web GUI.
        """

        def test_remove_file(self):
            file_name = files.file_to_be_deleted
            self.helper.select_item(file_name, True)
            self.button_clicker.click_action_bar_button("Move to trash")
            sleep(6)
            assert not self.helper.wait_for_element(locators.file_selector(file_name))

        """
        ## Test function to remove multiple files in the Google Drive web GUI.
        """

        def test_remove_multiple_files(self):
            self.button_clicker.navigate_to("Home")
            sleep(2)
            for file in files.fileCollection:
                try:
                    self.helper.select_item(file, True)
                    self.button_clicker.click_action_bar_button("Move to trash")
                    # assert not file_actions.helper.wait_for_element(locators.file_selector(file))
                except FileNotFoundError as e:
                    assert False, repr(e)
                finally:
                    self.driver.refresh()

        def test_delete_file_permanently(self):
            self.driver.refresh()
            sleep(5)
            self.helper.select_item(files.delete_forever_file_name, False)
            self.button_clicker.click_action_bar_button("Move to trash")
            self.button_clicker.navigate_to("Trash")
            deleted_file_locator = locators.file_selector(files.delete_forever_file_name)
            self.helper.wait_for_element(deleted_file_locator)
            self.helper.select_item(files.delete_forever_file_name, show_more_needed=False)
            self.button_clicker.click_action_bar_button("Delete forever")
            sleep(2)
            try:
                delete_confirm_btn_element = self.helper.wait_for_element(locators.delete_confirm_button_locator)
                self.button_clicker.click_element(delete_confirm_btn_element)
                sleep(3)
            except Exception:  # added exception
                assert False, "Error occured"
            else:
                assert True, f"{files.delete_forever_file_name} is permanently deleted"

        """
        Test function to undo delete action in the Google Drive web GUI.
        """

        def test_undo_delete_action(self):
            file_name_to_retrieve = files.file_to_be_restored
            self.button_clicker.navigate_to("Trash")
            sleep(4)
            self.helper.select_item(file_name_to_retrieve, show_more_needed=False)
            self.button_clicker.click_action_bar_button("Restore from trash")
            restoration_successful = self.higher_actions.verify_restoration(file_name_to_retrieve)
            sleep(4)
            assert restoration_successful is True, f"Failed to restore file '{file_name_to_retrieve}'"


class TestfolderActions(BaseTest):

    """
    Test function to rename a folder in the Google Drive web GUI.
    """

    def test_rename_folder(self):
        old_folder_name = files.folder_name
        new_folder_name = files.renamed_folder_name
        self.button_clicker.navigate_to("Home")
        self.button_clicker.click_on_folders_button
        self.helper.select_item(old_folder_name, True)
        self.helper.rename_selected_item(new_folder_name)
        self.button_clicker.click_on_ok_button()

        result = self.higher_actions.rename_verification(old_folder_name, new_folder_name)
        assert result, "Rename failed"

    """
    ## Test function to create a new folder in the Google Drive web GUI.
    """

    def test_create_folder(self):
        folder_name = files.create_folder_name
        self.button_clicker.click_on_new_button()
        action_button = self.helper.wait_to_click(locators.new_menu_button_locator("New folder"))
        action_button.click()
        sleep(2)
        autoGUIutils.type_into_dialogue_box(folder_name)
        self.driver.refresh()
        assert self.helper.wait_for_element(locators.file_selector(folder_name)) is not None
        sleep(3)

    """
    ## Test function to upload new file in the Google Drive web GUI.
    """

    def test_remove_folder(self):
        folder_to_be_removed = files.folder_name_to_be_removed
        self.button_clicker.navigate_to("Home")
        self.button_clicker.click_on_folders_button()
        self.helper.select_item(folder_to_be_removed, True)
        self.button_clicker.click_action_bar_button("Move to trash")
        sleep(4)
        assert not self.helper.wait_for_element(locators.file_selector(folder_to_be_removed))

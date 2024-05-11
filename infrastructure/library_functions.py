from time import sleep
import pyautogui
import pyperclip
from selenium.webdriver.common.action_chains import ActionChains
import selenium.common.exceptions as EXC
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from infrastructure import locators
from webbrowser import Chrome
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
import configparser
from infrastructure import autoGUIutils

parser = configparser.ConfigParser()
parser.read("infrastructure/config.ini")

very_small_delay = float(parser.get("Delay Parameters", "very_small_delay"))
small_delay = float(parser.get("Delay Parameters", "small_delay"))
medium_delay = float(parser.get("Delay Parameters", "medium_delay"))
large_delay = float(parser.get("Delay Parameters", "large_delay"))


class ElementaryActions:
    """Class for performing elementary actions using Selenium WebDriver.

    This class provides methods to perform basic actions such as waiting for elements,
    double-clicking on elements, dragging and dropping elements, sending keys to elements,
    performing context clicks, and clicking on elements.

    Parameters:
    driver (Chrome): The Selenium Chrome WebDriver instance.
    web_driver_wait (WebDriverWait): The Selenium WebDriverWait instance for waiting on elements.
    """

    def __init__(self, driver: Chrome, web_driver_wait: WebDriverWait):
        self.driver = driver
        self.web_driver_wait = web_driver_wait

    def wait_for_element(self, locator):
        """Wait for the presence of an element.

        Parameters:
        locator (tuple): Locator for the web element.

        Returns:
        WebElement: The located WebElement.

        Raises:
        TimeoutException: If the element is not found within the specified timeout.
        """
        try:
            element = self.web_driver_wait.until(
                EC.presence_of_element_located(locator)
            )
            return element
        except TimeoutException:
            print(f"Timeout waiting for element with locator {locator}")
            return None

    def wait_for_elements(self, locator):
        """Wait for elements matching the locator to be present in the DOM.

        Parameters:
            locator (tuple): A tuple containing the locator strategy
            and value (e.g., (By.ID, 'element_id')).

        Returns:
            list: A list of matching elements, or an empty list if no elements are
            found within the timeout.
        """
        try:
            elements = self.web_driver_wait.until(
                EC.presence_of_all_elements_located(locator)
            )
            return elements
        except Exception as e:
            print(f"An error occurred while waiting for elements: {e}")
            return []

    def double_click_element(self, element):
        """Double-click on a given element.

        Parameters:
        element (WebElement): The WebElement to double-click.

        Raises:
        Exception: If an error occurs while double-clicking on the element.
        """
        action_chain = ActionChains(self.driver)
        try:
            action_chain.double_click(element).perform()
        except Exception as e:
            print(f"Error double clicking on element: {e}")
        sleep(medium_delay)

    def drag_and_drop_element(self, src_element, dst_element):
        """Drag and drop an element from source to destination.

        Parameters:
        src_element (WebElement): The WebElement to drag.
        dst_element (WebElement): The WebElement to drop onto.

        Raises:
        Exception: If an error occurs during the drag and drop operation.
        """
        action_chain = ActionChains(self.driver)
        try:
            temp = action_chain.drag_and_drop(src_element, dst_element)
            temp.perform()
        except Exception as e:
            print(f"Error dragging and dropping element: {e}")
        sleep(small_delay)

    def wait_to_click(self, locator):
        """Wait for an element to be clickable and click on it.

        Parameters:
        locator (tuple): Locator strategy and value for identifying the element.

        Returns:
        WebElement: The clickable WebElement.

        Raises:
        TimeoutException: If the element is not clickable within the specified timeout.
        """
        try:
            expectation = EC.element_to_be_clickable(locator)
            return self.web_driver_wait.until(expectation)
        except TimeoutException:
            print(f"Timeout waiting for element with locator {locator}")
            return None

    def rename_selected_item(self, new_file_name):
        """Rename the selected item with a new name.

        Parameters:
        new_file_name (str): The new name of the file.
        """
        pyautogui.press("n")
        sleep(small_delay)
        pyautogui.write(new_file_name)

    def send_keys_to_element(self, element_locator, text):
        """Send keys to a specified element.

        Parameters:
        element_locator (tuple): Locator strategy and value for identifying the element.
        text (str): The text to be sent to the element.

        Raises:
        Exception: If an error occurs while sending keys to the element.
        """
        try:
            element = self.driver.find_element(*element_locator)
            element.send_keys(text)
        except Exception as e:
            print(f"Error sending keys to element: {e}")

    def send_keys_to_focused(self, text):
        """Send keys to the currently focused element.

        Parameters:
        text (str): The text to be sent to the focused element.

        Raises:
        Exception: If an error occurs while sending keys to the focused element.
        """
        try:
            action_chain = ActionChains(self.driver)
            action_chain.send_keys(text)
            action_chain.perform()

        except Exception as e:
            print(f"Error sending keys to element: {e}")

    def context_click(self):
        """Perform a context click (right-click) operation."""
        action_chain = ActionChains(self.driver)
        action_chain.context_click().perform()
        sleep(small_delay)

    def refresh_and_wait_to_settle(self):
        """Perform a refresh operation and wait till the page loads."""
        self.driver.refresh()
        sleep(large_delay)

    def click_element(self, element):
        """Click on a specified element.

        Parameters:
        element (WebElement): The WebElement to click on.

        Raises:
        Exception: If an error occurs while clicking on the element.
        """
        action_chain = ActionChains(self.driver)
        try:
            action_chain.click(element).perform()
        except Exception as e:
            print(f"Error clicking on element: {e}")


class ButtonClicker(ElementaryActions):
    """Class for performing button-clicking actions using Selenium WebDriver.

    This class provides methods to click on various buttons such as action bar buttons,
    navigation buttons, OK button, Type button, folders button, search in Drive bar,
    New button, and other specific buttons.

    Parameters:
    driver (Chrome): The Selenium Chrome WebDriver instance.
    web_driver_wait (WebDriverWait): The Selenium WebDriverWait instance for
    waiting on elements.
    """

    def __init__(self, driver: Chrome, web_driver_wait: WebDriverWait):

        super().__init__(driver, web_driver_wait)

    def click_action_bar_button(self, button_name):
        """Click on a button in the action bar.

        Parameters:
        button_name (str): The name of the button to be clicked.
        """
        button_element = self.wait_to_click(
            locators.action_bar_button_selector(button_name)
        )
        button_element.click()

    def click_on_ok_button(self):
        """Click on the OK button."""
        ok_button = self.wait_to_click(locators.ok_button_locator)
        ok_button.click()
        sleep(small_delay)

    def click_on_close_button(self):
        """Click on the close button."""
        close_button = self.wait_to_click(locators.close_details_button)
        close_button.click()
        sleep(small_delay)

    def click_on_type_button(self):
        """Click on the Type button."""
        type_button = self.wait_to_click(locators.type_button_locator)
        type_button.click()

    def click_on_the_required_type(self, file_type):
        """Click on the required type.

        Parameters:
        file_type (str): The type of file to be clicked (e.g., 'Document', 'Folder').
        """
        required_type = self.wait_to_click(locators.type_of_file_selector(file_type))
        required_type.click()
        sleep(small_delay)

    def click_on_folders_button(self):
        """Click on the Folders button."""
        folders_btn = self.wait_to_click(locators.folders_button_locator)
        folders_btn.click()
        sleep(very_small_delay)

    def click_on_search_in_drive(self):
        """Click on the Search in Drive bar."""
        search_bar = self.wait_to_click(locators.search_bar_locator)
        search_bar.click()
        sleep(small_delay)

    def click_on_new_button(self):
        """Click on the New button."""
        new_button = self.wait_to_click(locators.new_button_selector)
        new_button.click()
        sleep(small_delay)

    def click_on_add_button(self):
        """Click on the Add button."""
        autoGUIutils.n_tabs_shift_focus(4)
        autoGUIutils.press_enter()

    def click_on_shortcut_folder_button(self):
        """Click on the Shortcut Folder Button button."""
        autoGUIutils.press_tab()
        autoGUIutils.press_enter()

    def navigate_to(self, button_name):
        """Navigate to a specific page available on the left menu.

        Parameters:
        button_name (str): The name of the button representing the page to navigate to.
        """
        button_element = self.wait_to_click(
            locators.left_menu_page_selector(button_name)
        )
        button_element.click()
        sleep(small_delay)


class HigherActions(ButtonClicker):
    """Class for performing higher-level actions using Selenium WebDriver.

    This class provides methods to perform various higher-level
    actions such as moving files,
    renaming files, uploading files, copying files, searching for files,
    removing files,
    permanently deleting files, undoing deletions, renaming folders, creating
    folders, and removing folders.

    Parameters:
    driver (Chrome): The Selenium Chrome WebDriver instance.
    web_driver_wait (WebDriverWait): The Selenium WebDriverWait instance for
    waiting on elements.
    button_clicker (ButtonClicker): An instance of the ButtonClicker class for
    performing button-clicking actions.
    """

    def __init__(self, driver: Chrome, web_driver_wait: WebDriverWait):
        super().__init__(driver, web_driver_wait)

    def select_item(self, item_name):
        """Select an item by its name.

        Parameters:
        item_name (str): Name of the item to be selected.

        Raises:
        FileNotFoundError: If the item with the specified name is not found.
        """
        action_chain = ActionChains(self.driver)
        try:
            temp_loc = locators.show_more_files
            show_more_button = self.driver.find_element(*temp_loc)
            if show_more_button.is_displayed():
                show_more_button.click()
                sleep(medium_delay)
        except NoSuchElementException:
            pass
        file_selector = locators.file_selector(item_name)
        file_element = self.wait_for_element(file_selector)
        if file_element:
            action_chain.move_to_element(file_element).click()
            action_chain.perform()
            return file_element
        else:
            raise FileNotFoundError

    def verify_search_results(self, expected_file_list):
        """Verify search results against expected file list.

        Parameters:
        expected_file_list (list): List of expected file names.

        Returns:
        bool: True if all expected files are found, False otherwise.
        """
        flag = True
        for expected_file in expected_file_list:
            file_element = self.wait_to_click(
                locators.file_selector(expected_file)
            )
            if not file_element:
                flag = False
                break
            self.double_click_element(
                file_element
            )
            autoGUIutils.go_back_esc()
        return flag

    def rename_verification(self, old_file_name, new_file_name):
        """Verify the renaming of a file.

        Parameters:
        old_file_name (str): The original name of the file.
        new_file_name (str): The new name of the file.

        Returns:
        bool: True if the file has been renamed successfully, False otherwise.
        """
        # Verify that the old file doesn't exist
        old_f_loc = locators.file_selector(old_file_name)
        old_file_element = self.wait_for_element(old_f_loc)
        assert (
            old_file_element is None
        ), f"Old file '{old_file_name}' still exists after rename operation."
        # Verify the existence of the new file
        renamed_file_element = self.wait_for_element(
            locators.file_selector(new_file_name)
        )
        assert (
            renamed_file_element is not None
        ), f"New file '{new_file_name}' not found after rename operation."
        # return true if both conditions are satisfied
        return True

    def deal_duplicate_and_await_upload(self, custom_timeout=80):
        """Handle duplicate file and await upload completion.

        This function deals with the situation where a file being uploaded already
        exists in Google Drive.
        It waits for the warning of the file being already present to show up.
        If the warning does not appear, it assumes the file is not already in Google Drive
        and proceeds to upload it as a new file. If the warning does appear,
        it assumes the file
        already exists and simulates pressing the spacebar to deal with the file.
        Finally, it waits until the upload completes, with a maximum wait time of 10 seconds.

        Returns:
        None

        Note:
        This function assumes that the file upload process can be initiated
        and completed successfully.
        If the warning detection or upload completion mechanism changes,
        this function may need to be updated accordingly.
        """
        # wait till upload completes, max 10 seconds by default
        # try block to deal with situation of file being there already
        # to see if the warning of file being already present shows up
        temp_ele = self.wait_for_element(locators.file_already_present_text)
        if temp_ele is None:
            print("file not already in google drive, uploading as new file")
        else:
            # to deal with file already exisiting
            autoGUIutils.n_tabs_shift_focus(2)
            pyautogui.press("space")
            sleep(small_delay)
        WebDriverWait(self.driver, custom_timeout).until_not(
            EC.text_to_be_present_in_element(locators.upload_status_span, "Uploading")
        )
        # to close the upload box (bottom-left)
        autoGUIutils.n_tabs_shift_focus(2)
        pyautogui.press("space")
        sleep(small_delay)

    def verify_file_in_destination(self, moved_fname, destination_folder):
        """Verify the presence of a file in the destination folder.

        Parameters:
        moved_fname (str): Name of the moved file.
        destination_folder (str): Name of the destination folder.

        Raises:
        AssertionError: If the file has not been moved successfully to the
        destination folder.
        """
        try:
            self.navigate_to("My Drive")
            # Double click the destination folder
            destination_folder_element = self.select_item(destination_folder)

            self.double_click_element(destination_folder_element)
        except EXC.StaleElementReferenceException:
            print("StaleElementReferenceException occurred...")
        except FileNotFoundError:
            assert False, "Destination folder not found!"
        # Verify file presence in the destination folder
        try:
            assert (
                self.select_item(moved_fname) is not None
            ), "File has not been moved successfully to the destination folder"
        except FileNotFoundError:
            assert False, "Moved file not found!"

    def verify_restoration(self, file_name):
        """Verify the restoration of a file.

        Parameters:
        file_name (str): Name of the file to be restored.

        Returns:
        bool: True if the file has been restored successfully, False otherwise.
        """
        # self.button_clicker.navigate_to("Home")
        self.click_on_search_in_drive()
        self.send_keys_to_focused(file_name)
        autoGUIutils.press_enter()
        try:
            self.select_item(file_name)
        except FileNotFoundError:
            assert False, "Restore/Undo Failed!"

    def move_action(self, move_fname, destination_folder_name):
        """Move a file to a specified destination folder.

        Parameters:
        move_fname (str): The name of the file to be moved.
        destination_folder_name (str): The name of the destination folder.

        Raises:
        None
        """
        self.select_item(move_fname)
        autoGUIutils.cut_selection()
        ele = self.select_item(destination_folder_name)
        self.double_click_element(ele)
        sleep(very_small_delay)
        autoGUIutils.paste_clipboard()
        sleep(small_delay)
        self.driver.back()
        sleep(small_delay)

    def undo_move_action(self, filename, folder):
        """Undo the move action of a file.

        Parameters:
        filename (str): The name of the file that was moved.
        folder (str): The name of the destination folder.

        Raises:
        None
        """
        self.move_action(filename, folder)
        try:
            undo_button = self.wait_for_element(locators.undo_button_selector)
            undo_button.click()
        except (TimeoutException, AttributeError):
            print("Undo button timed out! simulating ctrl+z ...")
            # keyboard.press("ctrl+z")
            pyautogui.hotkey("ctrl", "z")

    def verify_undo_move_action(self, filename, folder):
        """Verify the undo of a move action.

        Parameters:
        filename (str): Name of the file that was moved.
        folder (str): Name of the destination folder.

        Raises:
        AssertionError: If the file is still in the destination folder
        or not present in My Drive.
        """
        try:
            # Double click the destination folder
            destination_folder_element = self.select_item(folder)
            self.double_click_element(destination_folder_element)
        except EXC.StaleElementReferenceException:
            print(
                "StaleElementReferenceException occurred..."
            )
        except FileNotFoundError:
            assert False, "Destination Folder not found error!"
        # Verify file not present in the destination folder
        try:
            assert (
                self.select_item(filename) is None
            ), "File is still present in the destination folder"
        except FileNotFoundError:
            print("File is not present in destination after undo.")
        self.navigate_to("My Drive")
        try:
            self.select_item(filename)
            assert True  # able to select file after undo
        except FileNotFoundError:
            assert False, "File is not present in My Drive"

    def rename_action(self, old_file_name, new_file_name):
        """Rename a file.

        Parameters:
        old_file_name (str): The original name of the file.
        new_file_name (str): The new name to be assigned to the file.

        Returns:
        None
        """
        self.select_item(old_file_name)
        self.rename_selected_item(new_file_name)
        self.click_on_ok_button()

    def undo_rename_action(self, old_fname, new_fname):
        """Undo the renaming of a file.

        Parameters:
        old_fname (str): The original name of the file before renaming.
        new_fname (str): The new name of the file after renaming.

        Returns:
        bool: True if the renaming is successfully undone, False otherwise.
        """
        self.rename_action(old_fname, new_fname)
        sleep(small_delay)
        # press control+z
        pyautogui.hotkey("ctrl", "z")

    def undo_rename_verification(self, old_fname, new_fname):
        """Verify the undo operation of file renaming.

        Parameters:
        old_fname (str): The original name of the file before renaming.
        new_fname (str): The new name of the file after renaming.

        Returns:
        bool: True if the undo operation was successful, False otherwise.
        """
        # Verify the existence of the old file
        f_loc = locators.file_selector(old_fname)
        old_file_ele = self.wait_for_element(f_loc)
        assert (
            old_file_ele is not None
        ), f"ERROR old file '{old_fname}' does not exist after undo."
        # Verify that the new file doesn't exist
        renamed_file_element = self.wait_for_element(
            locators.file_selector(new_fname)
        )
        assert (
            renamed_file_element is None
        ), f"ERROR new file '{new_fname}' still exists after undo."

    def get_file_names_action(self):
        """Get the number of file names.

        Returns:
        int: The number of file names.
        """
        col_files = self.driver.find_elements(By.CSS_SELECTOR, "div.KL4NAf")
        sleep(very_small_delay)
        return len(col_files)

    def upload_file_action(self, file_to_upload):
        """Upload a file.

        Parameters:
        file_to_upload (str): The file path of the file to be uploaded.

        Raises:
        None
        """
        self.click_on_new_button()
        upload_button = self.wait_for_element(
            locators.new_menu_button_locator("File upload")
        )
        upload_button.click()
        sleep(small_delay)
        autoGUIutils.type_into_dialogue_box(file_to_upload)
        self.deal_duplicate_and_await_upload()

    def copy_file_action(self, file_name_for_copy):
        """Copy a file.

        Parameters:
        file_name_for_copy (str): The name of the file to be copied.

        Returns:
        WebElement: The WebElement of the copied file element.
        """
        self.select_item(file_name_for_copy)
        self.context_click()

        mkcopy_ele = self.wait_to_click(locators.make_a_copy_element_locator)
        mkcopy_ele.click()
        sleep(small_delay)
        copied_file_ele = self.select_item("Copy of " + file_name_for_copy)
        return copied_file_ele

    def verify_copy_file_action(self, copied_file_element, file_name_for_copy):
        """Verify copy file testcase results.

        Parameters:
        copied_file_element : The file element after created after copying.
        file_name_for_copy : The name of original file.

        Asserts True if both source and copied file exist otherwise False

        Returns:
        None
        """
        try:
            source_file_element = self.select_item(file_name_for_copy)
        except FileNotFoundError:
            print("source file missing adter copy action")
            source_file_element = None
        assert (
            copied_file_element and source_file_element
        ), "Copy verification failed!"

    def search_by_name_action(self, file_to_be_searched):
        """Search for a file by its name.

        Parameters:
        file_to_be_searched (str): The name of the file to be searched.

        Raises:
        None
        """
        self.navigate_to("My Drive")
        self.click_on_search_in_drive()
        sleep(small_delay)
        self.send_keys_to_focused(file_to_be_searched)
        autoGUIutils.press_enter()
        file_elements = self.wait_for_elements(
            locators.file_selector(file_to_be_searched)
        )
        if file_elements:
            file_names = [element.text for element in file_elements]
            with open("results/debug_file_names.log", "w") as file:
                for name in file_names:
                    file.write(name + "\n")
        else:
            print("No matching file elements found.")

    def search_by_type_action(self, filetype):
        """Search for files by their type.

        Parameters:
        filetype (str): The file type to search for.

        Returns:
        int: The number of files found by type.
        """
        self.navigate_to("My Drive")
        self.click_on_type_button()
        self.click_on_the_required_type(filetype)
        file_elements = self.driver.find_elements(*locators.fname_div)
        file_names = [element.text for element in file_elements]
        file_name = f"results/debug_file_names_{filetype}.log"
        with open(file_name, "w") as file:
            for name in file_names:
                file.write(name + "\n")
        return file_names

    def remove_file_action(self, file_name):
        """Remove a file.

        Parameters:
        file_name (str): The name of the file to be removed.

        Raises:
        AssertionError: If the file still exists after removal.
        """
        self.select_item(file_name)
        self.click_action_bar_button("Move to trash")
        temp_loc = locators.file_selector(file_name)
        sleep(small_delay)
        assert not self.wait_for_element(temp_loc)

    def delete_permanently_action(self, delete_forever_file_name):
        """Permanently delete a file.

        Parameters:
        delete_forever_file_name (str):
        The name of the file to be permanently deleted.

        Returns:
        bool:
        True if the file has been permanently deleted, False otherwise.
        """
        self.navigate_to("My Drive")
        self.select_item(delete_forever_file_name)
        self.click_action_bar_button("Move to trash")
        self.navigate_to("Trash")

        del_file_loc = locators.file_selector(delete_forever_file_name)
        self.wait_for_element(del_file_loc)

        self.select_item(delete_forever_file_name)
        self.click_action_bar_button("Delete forever")
        sleep(very_small_delay)
        try:
            delete_confirm_btn_element = self.wait_for_element(
                locators.delete_confirm_button_locator
            )
            self.click_element(delete_confirm_btn_element)
            sleep(small_delay)
        except Exception:
            return False
        return True

    def share_via_link(self, filename):
        """Share a file via link.

        Parameters:
        filename (str): The name of the file to be shared.

        Returns:
        None
        """
        self.open_share_window(filename)
        autoGUIutils.n_tabs_shift_focus(2)
        autoGUIutils.press_enter()
        autoGUIutils.press_down_arrow()
        autoGUIutils.press_enter()
        sleep(medium_delay)
        autoGUIutils.n_tabs_shift_focus(2)
        autoGUIutils.press_enter()
        autoGUIutils.go_back_esc()

    def undo_delete_action(self, fname):
        """Undo deletion of a file.

        Parameters:
        fname (str): The name of the file to be retrieved.

        Returns:
        bool: True if the file has been successfully restored, False otherwise.
        """
        self.navigate_to("Trash")
        self.select_item(fname)
        self.click_action_bar_button("Restore from trash")
        self.verify_restoration(fname)

    def rename_folder_action(self, old_folder_name, new_folder_name):
        """Rename a folder.

        Parameters:
        old_folder_name (str): The original name of the folder.
        new_folder_name (str): The new name of the folder.

        Returns:
        bool: True if the folder has been renamed successfully, False otherwise.
        """
        self.navigate_to("Home")
        self.click_on_folders_button()
        self.select_item(old_folder_name)
        self.rename_selected_item(new_folder_name)
        self.click_on_ok_button()
        result = self.rename_verification(old_folder_name, new_folder_name)
        return result

    def create_folder_action(self, folder_name):
        """Create a new folder.

        Parameters:
        folder_name (str): The name of the folder to be created.

        Raises:
        None
        """
        self.click_on_new_button()
        action_button = self.wait_to_click(
            locators.new_menu_button_locator("New folder")
        )
        action_button.click()
        autoGUIutils.type_into_dialogue_box(folder_name)
        sleep(very_small_delay)

    def remove_folder_action(self, folder_to_be_removed):
        """Remove a folder.

        Parameters:
        folder_to_be_removed (str): The name of the folder to be removed.

        Raises:
        None
        """
        self.navigate_to("Home")
        self.click_on_folders_button()
        self.select_item(folder_to_be_removed)
        self.click_action_bar_button("Move to trash")

    def verify_button_tooltips(self, btn_list):
        """
        Verify the tooltip text of buttons like "Home", "My Drive" etc.

        Parameters:
        btn_list (dict):
        A dictionary containing button names as keys and expected
        tooltip text as values.

        Returns:
        bool:
        True if all buttons are present and their tooltips match
        the expected text, False otherwise.
        """
        all_buttons_present = True
        self.navigate_to("Home")

        for button_name, expected_tt_txt in btn_list.items():
            try:
                button_element = self.wait_for_element(
                    locators.left_menu_page_selector(button_name)
                )
                action_chain = ActionChains(self.driver)
                action_chain.move_to_element(button_element).perform()
                sleep(very_small_delay)

                actual_tt_txt = button_element.get_attribute("title")

                if actual_tt_txt != expected_tt_txt:
                    print(f"Tooltip for '{button_name}' doesn't match!")
                    print(f"Exp:{expected_tt_txt}, Actual:{actual_tt_txt}")
                    all_buttons_present = False
            except NoSuchElementException:
                print(f"Button '{button_name}' not found.")
                all_buttons_present = False

        return all_buttons_present

    def verify_file_tooltips(self):
        """Verify tooltips for files in the Home page.

        Returns:
        bool: True if all files have tooltips, False otherwise.
        """
        self.navigate_to("Home")
        all_files_verified = True

        fname_divs = self.driver.find_elements(By.CSS_SELECTOR, "div.KL4NAf")
        file_names = [file_name_div.text for file_name_div in fname_divs]

        for file_name in file_names:
            try:
                self.select_item(file_name)
                sleep(very_small_delay)

                f_loc = locators.file_selector(file_name)
                file_element = self.wait_for_element(f_loc)
                actual_tooltip_text = file_element.get_attribute("title")

                if not actual_tooltip_text:
                    print(f"Tooltip text for '{file_name}' isn't present.")
                    all_files_verified = False
            except NoSuchElementException:
                print(f"File '{file_name}' not found.")
                all_files_verified = False

        return all_files_verified

    def verify_copied_link(self):
        """Verify if a link has been copied to the clipboard and
        access it in a new tab.

        Returns:
        None
        """
        try:
            shared_link = pyperclip.paste()
            print(f"Retrieved shared link: {shared_link}")

            try:
                pyautogui.hotkey("ctrl", "t")
                self.driver.switch_to.window(
                    self.driver.window_handles[-1]
                )
                pyautogui.hotkey("ctrl", "l")
                autoGUIutils.type_into_dialogue_box(shared_link)
                try:
                    error_message = self.driver.find_element(
                        *locators.error_message_selector
                    )
                    assert (
                        not error_message.is_displayed()
                    ), "Error message is displayed"
                except NoSuchElementException:
                    pass
                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[-1])
            except Exception as e:
                print(f"Error opening link in new tab: {e}")
                print("Continuing with test execution...")

        except pyperclip.exceptions.PyperclipException:
            print("Failed to access clipboard.")

    def open_share_window(self, file_to_be_shared):
        """Open the share window for a specified file.

        This function navigates to the Home page, selects the specified
        file, and opens the share window for that file.

        Parameters:
        file_to_be_shared (str): The name of the file for which the share
        window should be opened.

        Returns:
        None

        Note:
        This function assumes that the file can be located and that a
        share button is present in the action bar to open
        the share window. If the UI layout or navigation changes, this
        function may need to be updated accordingly.
        """
        self.navigate_to("Home")
        self.select_item(file_to_be_shared)
        share_button = self.wait_for_element(
            locators.action_bar_button_selector("Share")
        )
        share_button.click()
        sleep(medium_delay)

    def verify_share_link_to_friend(self, shared_file, email):
        """Verify if a file has been shared with a friend via email.

        This function checks if a specified file has been shared with
        a friend via email by attempting to locate the email
        address of the recipient in the share window. If the email
        address is found, it indicates that the file has been
        shared successfully.

        Parameters:
        shared_file (str): The name of the file to be shared.
        email (str): The email address of the recipient.

        Returns:
        bool: True if the file has been shared with the specified
        email address, False otherwise.

        Note:
        This function assumes that the share window displays the
        recipient's email address in a specified location
        (represented by 'locators.email_selector'). If the layout
        of the share window changes, this function may need to be
        updated accordingly.
        """
        self.open_share_window(shared_file)
        try:
            element = self.wait_for_element(locators.email_selector)
            if element is not None:
                assert True
        except TimeoutException:
            return False, f"Friend's email {email} not found in list"
        finally:
            autoGUIutils.go_back_esc()

    def share_link_to_friend(self, file_to_share, email):
        """Share a file link with a friend via email.

        This function initiates the sharing process for a specified
        file by opening the share window, entering the recipient's
        email address, and sending the share invitation. It also includes
        a brief message ("short notes") before finalizing
        the sharing process.

        Parameters:
        file_to_share (str): The name of the file to be shared.
        email (str): The email address of the recipient.

        Returns:
        None

        Note:
        This function assumes that the sharing process involves typing
        the recipient's email address into a dialogue box,
        navigating tabs to enter a message, and pressing 'Enter' to
        finalize the sharing process. If the sharing process changes
        in the future, this function may need to be updated accordingly.
        """
        self.open_share_window(file_to_share)
        autoGUIutils.type_into_dialogue_box(email)
        autoGUIutils.press_enter()
        autoGUIutils.n_tabs_shift_focus(3)
        autoGUIutils.type_into_dialogue_box("short notes")
        autoGUIutils.n_tabs_shift_focus(3)
        autoGUIutils.press_enter()
        self.refresh_and_wait_to_settle()

    def get_storage_used(self):
        """Get the amount of storage used in Google Drive.

        This function retrieves the amount of storage used in Google
        Drive by parsing the text of the storage element
        located using the provided locator. It extracts the storage
        capacity until the first occurrence of 'G' (indicating
        gigabytes) and returns it as a floating-point number.

        Returns:
        float: The amount of storage used in gigabytes.

        Note:
        This function assumes that the storage capacity is
        represented in gigabytes ('G'). If the format of the storage
        element changes, this function may need to be updated accordingly.
        """
        storage_ele = self.driver.find_element(*locators.storage_selector)
        capacity, units = (
            float(storage_ele.text.split(" ")[0]),
            storage_ele.text.split(" ")[1],
        )
        storage_units = {"KB": 1024, "MB": 1024**2, "GB": 1024**3}
        bytes = capacity * storage_units.get(units, 1)
        return bytes

    def traverse_path(self, path, from_home=False):
        """Traverse a given path in Google Drive.

        This function navigates through the folders in Google Drive
        to reach a specific path. It starts from the Home page by
        default or the current page if 'from_home' is set to True.

        Parameters:
        path (str): The path to traverse.
        from_home (bool): Flag indicating whether to start from the Home
        page. Defaults to False.

        Returns:
        None
        """
        if from_home:
            self.navigate_to("My Drive")
        for i in path.split("/"):
            folder_element = self.select_item(i)
            self.double_click_element(folder_element)

    def one_level_up(self):
        """Navigate one level up in the folder hierarchy.

        This function simulates clicking the navigation button
        to go one level up in the folder hierarchy.

        Returns:
        None
        """
        navigation_bar_item = locators.navigation_bar_items
        navbar_items = self.wait_for_elements(navigation_bar_item)
        self.click_element(navbar_items[-2])

    def navigate_to_path(self, current_path, required_path):
        """Navigate to a specified path in Google Drive.

        This function navigates to a specified path in Google Drive
        by comparing the current path with the required path and
        traversing through the folders accordingly.

        Parameters:
        current_path (str): The current path in Google Drive.
        required_path (str): The required path to navigate to.

        Returns:
        None
        """
        current_path = current_path.split("/")
        required_path = required_path.split("/")
        current_depth = len(current_path)
        i = 0
        while i < min(len(current_path), len(required_path)):
            if current_path[i] == required_path[i]:
                i += 1
            else:
                break

        for _ in range(current_depth - i):
            self.one_level_up()

        remaining_path = "/".join(required_path[i:])
        self.traverse_path(remaining_path)

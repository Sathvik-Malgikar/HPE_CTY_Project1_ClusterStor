from time import sleep
import pyautogui
from selenium.webdriver.common.action_chains import ActionChains
import selenium.common.exceptions as EXC
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import locators
from selenium.webdriver.common.by import By
import autoGUIutils


"""Class for performing elementary actions using Selenium WebDriver for Google Drive.

    This class provides methods to perform basic actions such as waiting for elements,
    double-clicking on elements, dragging and dropping elements, sending keys to elements,
    and performing context clicks.

    Parameters:
    driver (WebDriver): The Selenium WebDriver instance.
    web_driver_wait (WebDriverWait): The Selenium WebDriverWait instance for waiting on elements.
"""


class ElementaryActions:
    def __init__(self, driver, web_driver_wait):
        self.driver = driver
        self.web_driver_wait = web_driver_wait

    """Wait for the presence of an element.

        Parameters:
        locator (tuple): Locator for the web element.

        Returns:
        WebElement: The located WebElement.

        Raises:
        TimeoutException: If the element is not found within the specified timeout.
    """
    def wait_for_element(self, locator):
        try:
            element = self.web_driver_wait.until(
                EC.presence_of_element_located(locator))
            return element
        except TimeoutException:
            print(f"Timeout waiting for element with locator {locator}")
            return None

    """Double-click on a given element.

        Parameters:
        element (WebElement): The WebElement to double-click.

        Raises:
        Exception: If an error occurs while double-clicking on the element.
    """

    def double_click_element(self, element):
        action_chain = ActionChains(self.driver)
        try:
            action_chain.double_click(element).perform()
        except Exception as e:
            print(f"Error double clicking on element: {e}")

    """Drag and drop an element from source to destination.

        Parameters:
        source_element (WebElement): The WebElement to drag.
        destination_element (WebElement): The WebElement to drop onto.

        Raises:
        Exception: If an error occurs during the drag and drop operation.
    """

    def drag_and_drop_element(self, source_element, destination_element):
        action_chain = ActionChains(self.driver)
        try:
            action_chain.drag_and_drop(
                source_element, destination_element).perform()
        except Exception as e:
            print(f"Error dragging and dropping element: {e}")

    """Wait for an element to be clickable and click on it.

        Parameters:
        locator (tuple): Locator strategy and value for identifying the element.
        Returns:
        WebElement: The clickable WebElement.

        Raises:
        TimeoutException: If the element is not clickable within the specified timeout.
    """

    def wait_to_click(self, locator):
        try:
            element = self.web_driver_wait.until(EC.element_to_be_clickable(locator))
            return element
        except TimeoutException:
            print(f"Timeout waiting for element with locator {locator}")
            return None

    # def select_item(self, item_name, show_more_needed):
    #     # show_more_needed is to ensure backwards compatibility
    #     action_chain = ActionChains(self.driver)
    #     if (show_more_needed):  # old testcases do not have show_more param, so by default True,
    #     # newer testcases can explicitly mention if show more button is to be clicked or not before looking for file

    #         show_more_button = self.wait_to_click(
    #             locators.show_more_files
    #         )
    #         show_more_button.click()

    #     sleep(5)

    #     file_selector = locators.file_selector(item_name)
    #     file_element = self.wait_for_element(file_selector)
    #     if file_element:

    #         action_chain.move_to_element(file_element).click()
    #         action_chain.perform()
    #     else:
    #         raise FileNotFoundError

    """Rename the selected item with a new name.

        Parameters:
        new_file_name (str): The new name of the file.
    """
    def rename_selected_item(self, new_file_name):
        pyautogui.press('n')
        pyautogui.write(new_file_name)

    """Send keys to a specified element.

        Parameters:
        element_locator (tuple): Locator strategy and value for identifying the element.
        text (str): The text to be sent to the element.

        Raises:
        Exception: If an error occurs while sending keys to the element.
    """

    def send_keys_to_element(self, element_locator, text):
        try:
            element = self.driver.find_element(*element_locator)
            element.send_keys(text)
        except Exception as e:
            print(f"Error sending keys to element: {e}")

    """Send keys to the currently focused element.

        Parameters:
        text (str): The text to be sent to the focused element.

        Raises:
        Exception: If an error occurs while sending keys to the focused element.
    """

    def send_keys_to_focused(self, text):
        try:
            action_chain = ActionChains(self.driver)
            action_chain.send_keys(text)
            action_chain.perform()

        except Exception as e:
            print(f"Error sending keys to element: {e}")

    """Perform a context click (right-click) operation.
        Parameters:None
        Raises:
        None
    """

    def context_click(self):
        action_chain = ActionChains(self.driver)
        action_chain.context_click().perform()

    """Click on a specified element.

        Parameters:
        element (WebElement): The WebElement to click on.

        Raises:
        Exception: If an error occurs while clicking on the element.
    """
    def click_element(self, element):
        action_chain = ActionChains(self.driver)
        try:
            action_chain.click(element).perform()
        except Exception as e:
            print(f"Error clicking on element: {e}")


"""Class for performing button-clicking actions using Selenium WebDriver in Google Drive.

    This class provides methods to click on various buttons such as action bar buttons, navigation buttons,
    OK button, Type button, folders button, search in Drive bar, and New button.
    Parameters:
    driver (WebDriver): The Selenium WebDriver instance.
    web_driver_wait (WebDriverWait): The Selenium WebDriverWait instance for waiting on elements.
    helper (Helper): An instance of the Helper class for performing helper actions.
"""


class ButtonClicker:
    def __init__(self, driver, web_driver_wait, helper):
        self.driver = driver
        self.web_driver_wait = web_driver_wait

    """Click on a button in the action bar.
        Parameters:
        button_name (str): The name of the button to be clicked.
    """
    def click_action_bar_button(self, button_name):
        button_element = ElementaryActions.wait_to_click(locators.action_bar_button_selector(button_name))
        button_element.click()

    """Navigate to a specific page(available on the left menu.

        Parameters:
        button_name (str): The name of the button representing the page to navigate to.
    """

    def navigate_to(self, button_name):
        button_element = ElementaryActions.wait_to_click(locators.left_menu_page_selector(button_name))
        button_element.click()

    """Click on the OK button.
        Parameters: None
    """
    def click_on_ok_button(self):
        ok_button = ElementaryActions.wait_to_click(locators.ok_button_locator)
        ok_button.click()
        sleep(3)

    """Click on the Type button."""
    def click_on_type_button(self):
        type_button = ElementaryActions.wait_to_click(locators.type_button_locator)
        type_button.click()

    """Click on the required type."""
    def click_on_the_required_type(self):
        required_type = ElementaryActions.wait_to_click(locators.type_of_file_locator)
        required_type.click()
        sleep(6)

    """Click on the Folders button."""
    def click_on_folders_button(self):
        folders_button = ElementaryActions.wait_to_click(locators.folders_button_locator)
        folders_button.click()
        sleep(5)

    """Click on the Search in Drive bar."""
    def click_on_search_in_drive(self):
        search_bar = ElementaryActions.wait_to_click(locators.search_bar_locator)
        search_bar.click()
        sleep(5)

    """Click on the New button."""
    def click_on_new_button(self):
        new_button = ElementaryActions.wait_to_click(locators.new_button_selector)
        new_button.click()
        sleep(2)


"""Class providing helper methods for performing various tasks in Google Drive.

    This class encapsulates functionalities such as selecting an item, verifying search results,
    verifying renaming of a file, dealing with duplicate files during upload, verifying file presence
    in the destination folder, and verifying the restoration of a file.

    Parameters:
    driver (WebDriver): The Selenium WebDriver instance.
    web_driver_wait (WebDriverWait): The Selenium WebDriverWait instance for waiting on elements.
"""


class Helper:
    def __init__(self, driver, web_driver_wait):
        self.driver = driver
        self.web_driver_wait = web_driver_wait

    """Select an item by its name.

        Parameters:
        item_name (str): Name of the item to be selected.
        show_more_needed (bool): Flag indicating whether to click the "Show More" button.

        Raises:
        FileNotFoundError: If the item with the specified name is not found.
    """
    def select_item(self, item_name, show_more_needed):
        # show_more_needed is to ensure backwards compatibility
        action_chain = ActionChains(self.driver)
        if (show_more_needed):  # old testcases do not have show_more param, so by default True,
            # newer testcases can explicitly mention if show more button is to be clicked or not before looking for file
            show_more_button = ElementaryActions.wait_to_click(
                locators.show_more_files
            )
            show_more_button.click()
        sleep(5)
        file_selector = locators.file_selector(item_name)
        file_element = ElementaryActions.wait_for_element(file_selector)
        if file_element:
            action_chain.move_to_element(file_element).click()
            action_chain.perform()
        else:
            raise FileNotFoundError

    """Verify search results against expected file list.

        Parameters:
        expected_file_list (list): List of expected file names.

        Returns:
        bool: True if all expected files are found, False otherwise.
    """
    def verify_search_results(self, expected_file_list):  # TODO return one boolean
        flag = True
        for expected_file in expected_file_list:
            file_element = ElementaryActions.wait_to_click(locators.file_selector(expected_file))  # TODO Check this once
            if not file_element:
                flag = False
                break
            ElementaryActions.double_click_element(file_element)  # TODO ask saad whether opening is needed
            sleep(3)
            autoGUIutils.go_back_esc()
        return flag

    """Verify the renaming of a file.

        Parameters:
        old_file_name (str): The original name of the file.
        new_file_name (str): The new name of the file.

        Returns:
        bool: True if the file has been renamed successfully, False otherwise.
        """
    def rename_verification(self, old_file_name, new_file_name):
        # Verify that the old file doesn't exist
        old_file_element = ElementaryActions.wait_for_element(locators.file_selector(old_file_name))
        assert old_file_element is None, f"Old file '{old_file_name}' still exists after rename operation."
        # Verify the existence of the new file
        renamed_file_element = ElementaryActions.wait_for_element(locators.file_selector(new_file_name))
        assert renamed_file_element is not None, f"New file '{new_file_name}' not found after rename operation."
        # return tru if bot conditions are satisfied
        return True

    def deal_duplicate_and_await_upload(self):
        # try block to deal with situation of file being there already
        try:
            # to see if the warning of file being alreay ent shows up
            ElementaryActions.wait_for_element(locators.file_already_present_text)
        except EXC.NoSuchElementException:

            print("file not already in google drive, uploading as new file")
        else:
            # to deal with file already exisiting
            autoGUIutils.n_tabs_shift_focus(2)

            sleep(0.5)
            pyautogui.press("space")
            sleep(1)
        finally:
            # wait till upload completes, max 10 seconds for now
            self.web_driver_wait.until(EC.presence_of_element_located(
                locators.upload_complete_text))
            sleep(2)

    """Verify the presence of a file in the destination folder.

        Parameters:
        moved_file_name (str): Name of the moved file.
        destination_folder (str): Name of the destination folder.

        Raises:
        AssertionError: If the file has not been moved successfully to the destination folder.
    """
    def verify_file_in_destination(self, moved_file_name, destination_folder):
        try:
            # Double click the destination folder
            destination_folder_element = ElementaryActions.wait_for_element(locators.file_selector(destination_folder))
            ElementaryActions.double_click_element(destination_folder_element)
            sleep(4)
        except EXC.StaleElementReferenceException:
            print("StaleElementReferenceException occurred. Retrying...")  # TODO either actually retry or remove "retrying"
        # Verify file presence in the destination folder
        assert ElementaryActions.wait_for_element(locators.file_selector(moved_file_name)) is not None, "File has not been moved successfully to the destination folder"

    """Verify the restoration of a file.

        Parameters:
        file_name (str): Name of the file to be restored.

        Returns:
        bool: True if the file has been restored successfully, False otherwise.
    """
    def verify_restoration(self, file_name):  # REDO this function
        # self.button_clicker.navigate_to("Home")
        ButtonClicker.click_on_search_in_drive()
        sleep(2)
        ElementaryActions.send_keys_to_focused(file_name)
        sleep(2)
        file_element = ElementaryActions.wait_for_element(locators.file_selector(file_name))
        if file_element:
            return True
        else:
            return False


"""Class for performing higher-level actions using Selenium WebDriver in Google Drive.

    This class provides methods to perform various higher-level actions such as moving files, renaming files,
    uploading files, copying files, searching for files, removing files, permanently deleting files, undoing
    deletions, renaming folders, creating folders, and removing folders.

    Parameters:
    driver (WebDriver): The Selenium WebDriver instance.
    web_driver_wait (WebDriverWait): The Selenium WebDriverWait instance for waiting on elements.
    button_clicker (ButtonClicker): An instance of the ButtonClicker class for performing button-clicking actions.
    helper (Helper): An instance of the Helper class for performing helper actions.
"""


class HigherActions:
    def __init__(self, driver, web_driver_wait, button_clicker, helper):
        self.driver = driver
        self.web_driver_wait = web_driver_wait
        self.button_clicker = button_clicker
        self.helper = helper

    """Move a file to a specified destination folder.

        Parameters:
        move_file_name (str): The name of the file to be moved.
        destination_folder_name (str): The name of the destination folder.
        show_more (bool): Flag indicating whether to click the "Show More" button.

        Raises:
        None
    """

    def move_action(self, move_file_name, destination_folder_name, show_more):
        self.helper.select_item(move_file_name, show_more_needed=show_more)
        sleep(2)
        file_element = self.helper.wait_for_element(locators.file_selector(move_file_name))
        destination_folder_element = self.helper.wait_for_element(locators.file_selector(destination_folder_name))
        self.helper.drag_and_drop_element(file_element, destination_folder_element)
        sleep(3)

    """Rename a file.

        Parameters:
        old_file_name (str): The original name of the file.
        new_file_name (str): The new name of the file.

        Returns:
        bool: True if the file has been renamed successfully, False otherwise.
    """

    def rename_action(self, old_file_name, new_file_name):
        self.helper.select_item(old_file_name, True)
        self.helper.rename_selected_item(new_file_name)
        self.button_clicker.click_on_ok_button()
        result = self.helper.rename_verification(old_file_name, new_file_name)
        return result

    """Get the number of file names.

        Returns:
        int: The number of file names.
    """

    def get_file_names_action(self):
        file_name_divs = self.driver.find_elements(By.CSS_SELECTOR, "div.KL4NAf")
        sleep(4)
        return len(file_name_divs)

    """Upload a file.

        Parameters:
        file_to_upload (str): The file path of the file to be uploaded.

        Raises:
        None
    """

    def upload_file_action(self, file_to_upload):
        self.button_clicker.click_on_new_button()
        upload_button = self.helper.wait_for_element(locators.new_menu_button_locator("File upload"))
        upload_button.click()
        sleep(2)
        autoGUIutils.type_into_dialogue_box(file_to_upload)
        # this is utility solely because prerequisites aso reuses this function
        self.helper.deal_duplicate_and_await_upload()

    """Copy a file.

        Parameters:
        file_name_for_copy (str): The name of the file to be copied.

        Returns:
        WebElement: The WebElement of the copied file element.
    """

    def copy_file_action(self, file_name_for_copy):
        self.helper.select_item(file_name_for_copy, show_more_needed=True)
        self.button_clicker.context_click()
        sleep(5)

        make_a_copy_element = self.helper.wait_to_click(locators.make_a_copy_element_locator)
        make_a_copy_element.click()

        sleep(5)
        self.driver.refresh()
        sleep(7)
        copied_file_element = self.helper.wait_for_element(locators.copied_file_locator)
        return copied_file_element

    """Search for a file by its name.

        Parameters:
        file_to_be_searched (str): The name of the file to be searched.

        Raises:
        None
    """

    def search_by_name_action(self, file_to_be_searched):
        ButtonClicker.click_on_search_in_drive()
        ElementaryActions.send_keys_to_focused(file_to_be_searched)
        autoGUIutils.press_enter()
        # Retrieve file elements from the search results
        file_elements = ElementaryActions.wait_for_elements(locators.file_selector(file_to_be_searched))
        # Extract file names from file elements
        file_names = [element.text for element in file_elements]
        # Write file names to a text file
        with open("file_names.txt", "w") as file:
            for name in file_names:
                file.write(name + "\n")

    """Search for files by their type.

        Returns:
        int: The number of files found by type.
    """

    def search_by_type_action(self):
        ButtonClicker.navigate_to("My Drive")
        ButtonClicker.click_on_type_button()
        ButtonClicker.click_on_the_required_type()
        file_elements = self.driver.find_elements_by_css_selector("div.KL4NAf")
        # Extract file names from file elements
        file_names = [element.text for element in file_elements]
        sleep(4)
        # Write file names to a text file
        with open("file_names_by_type.txt", "w") as file:
            for name in file_names:
                file.write(name + "\n")
        return len(file_names)

    """Remove a file.

        Parameters:
        file_name (str): The name of the file to be removed.

        Raises:
        AssertionError: If the file still exists after removal.
    """

    def remove_file_action(self, file_name):
        self.helper.select_item(file_name, True)
        self.button_clicker.click_action_bar_button("Move to trash")
        sleep(6)
        assert not self.helper.wait_for_element(locators.file_selector(file_name))

    """Permanently delete a file.

        Parameters:
        delete_forever_file_name (str): The name of the file to be permanently deleted.

        Returns:
        bool: True if the file has been permanently deleted, False otherwise.
    """

    def delete_permanently_action(self, delete_forever_file_name):
        self.driver.refresh()
        sleep(5)
        self.helper.select_item(delete_forever_file_name, False)
        self.button_clicker.click_action_bar_button("Move to trash")
        self.button_clicker.navigate_to("Trash")

        deleted_file_locator = locators.file_selector(delete_forever_file_name)
        self.helper.wait_for_element(deleted_file_locator)

        self.helper.select_item(delete_forever_file_name, show_more_needed=False)
        self.button_clicker.click_action_bar_button("Delete forever")
        sleep(2)
        try:
            delete_confirm_btn_element = self.helper.wait_for_element(locators.delete_confirm_button_locator)
            self.button_clicker.click_element(delete_confirm_btn_element)
            sleep(3)
        except Exception:
            return False
        return True

    """Undo deletion of a file.

        Parameters:
        file_name_to_retrieve (str): The name of the file to be retrieved.

        Returns:
        bool: True if the file has been successfully restored, False otherwise.
    """

    def undo_delete_action(self, file_name_to_retrieve):
        self.button_clicker.navigate_to("Trash")
        sleep(4)
        self.helper.select_item(file_name_to_retrieve, show_more_needed=False)
        self.button_clicker.click_action_bar_button("Restore from trash")
        restoration_successful = self.higher_actions.verify_restoration(file_name_to_retrieve)
        sleep(4)
        return restoration_successful

    """Rename a folder.

        Parameters:
        old_folder_name (str): The original name of the folder.
        new_folder_name (str): The new name of the folder.

        Returns:
        bool: True if the folder has been renamed successfully, False otherwise.
    """

    def rename_folder_action(self, old_folder_name, new_folder_name):
        self.button_clicker.navigate_to("Home")
        self.button_clicker.click_on_folders_button
        self.helper.select_item(old_folder_name, True)
        self.helper.rename_selected_item(new_folder_name)
        self.button_clicker.click_on_ok_button()
        result = self.higher_actions.rename_verification(old_folder_name, new_folder_name)
        return result

    """Create a new folder.

        Parameters:
        folder_name (str): The name of the folder to be created.

        Raises:
        None
    """

    def create_folder_action(self, folder_name):
        self.button_clicker.click_on_new_button()
        action_button = self.helper.wait_to_click(locators.new_menu_button_locator("New folder"))
        action_button.click()
        sleep(2)
        autoGUIutils.type_into_dialogue_box(folder_name)
        self.driver.refresh()

    """Remove a folder.

        Parameters:
        folder_to_be_removed (str): The name of the folder to be removed.

        Raises:
        None
    """

    def remove_folder_action(self, folder_to_be_removed):
        self.button_clicker.navigate_to("Home")
        self.button_clicker.click_on_folders_button()
        self.helper.select_item(folder_to_be_removed, True)
        self.button_clicker.click_action_bar_button("Move to trash")
        sleep(4)

    # def select_file_from_trash(self):# TODO parmeterize filename just like select_file and merge these two functions.
    #     action_chain = ActionChains(self.driver)
    #     file_element = self.helper.wait_for_element(locators.file_selector(files.file_to_be_restored))
    #     #TODO REMOVE "files" AND PARAMTERIZE
    #     if not file_element:
    #         assert False, "File Not Found in Trash"
    #     else:
    #         action_chain.move_to_element(file_element).click().perform()
    #         sleep(6)

    # def search_file_by_name(self,filename):
    #     self.button_clicker.click_on_search_in_drive()
    #     autoGUIutils.type_into_dialogue_box(filename)

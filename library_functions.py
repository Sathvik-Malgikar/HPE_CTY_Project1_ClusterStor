from time import sleep
import pyautogui
from selenium.webdriver.common.action_chains import ActionChains
import selenium.common.exceptions as EXC
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import locators
from selenium.common.exceptions import NoSuchElementException
from webbrowser import Chrome
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
import configparser

import autoGUIutils

"""Class for performing elementary actions using Selenium WebDriver for Google Drive.

    This class provides methods to perform basic actions such as waiting for elements,
    double-clicking on elements, dragging and dropping elements, sending keys to elements,
    and performing context clicks.
    Parameters:
    driver (WebDriver): The Selenium WebDriver instance.
    web_driver_wait (WebDriverWait): The Selenium WebDriverWait instance for waiting on elements.
"""

parser = configparser.ConfigParser()
parser.read("config.ini")
small_delay = float(parser.get("Delay Parameters", "small_delay"))
medium_delay = float(parser.get("Delay Parameters", "medium_delay"))
large_delay = float(parser.get("Delay Parameters", "large_delay"))

small_delay = float(parser.get("Delay Parameters", "small_delay"))
medium_delay = float(parser.get("Delay Parameters", "medium_delay"))
large_delay = float(parser.get("Delay Parameters", "large_delay"))

class ElementaryActions:
    def __init__(self, driver : Chrome, web_driver_wait : WebDriverWait):
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
        
    def wait_for_elements(self, locator):
        """
        Wait for elements matching the locator to be present in the DOM.
        
        Args:
            locator: A tuple containing the locator strategy and value (e.g., (By.ID, 'element_id')).
            timeout: Maximum time to wait for the elements (default is 10 seconds).
        
        Returns:
            A list of matching elements, or an empty list if no elements are found within the timeout.
        """
        try:
            elements = self.web_driver_wait.until(EC.presence_of_all_elements_located(locator))
            return elements
        except Exception as e:
            print(f"An error occurred while waiting for elements: {e}")
            return []

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
    
    """Perform a refresh operation and wait till the page loads.
        Parameters:None
        Raises:
        None
    """
    
    def refresh_and_wait_to_settle(self):
        self.driver.refresh()
        sleep(large_delay)    
    

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


class ButtonClicker(ElementaryActions):
    
    def __init__(self,driver,web_driver_wait):

        super().__init__(driver,web_driver_wait)
        #self.web_driver_wait = web_driver_wait
        #self = ElementaryActions(self.driver, self.web_driver_wait)

    """Click on a button in the action bar.
        Parameters:
        button_name (str): The name of the button to be clicked.
    """
    def click_action_bar_button(self, button_name):
        button_element = self.wait_to_click(locators.action_bar_button_selector(button_name))
        button_element.click()

   

    """Click on the OK button.
        Parameters: None
    """
    def click_on_ok_button(self):
        ok_button = self.wait_to_click(locators.ok_button_locator)
        ok_button.click()
        sleep(small_delay)

    """Click on the Type button."""
    def click_on_type_button(self):
        type_button = self.wait_to_click(locators.type_button_locator)
        type_button.click()

    """Click on the required type."""
    def click_on_the_required_type(self):
        required_type = self.wait_to_click(locators.type_of_file_locator)
        required_type.click()
        sleep(large_delay)

    """Click on the Folders button."""
    def click_on_folders_button(self):
        folders_button = self.wait_to_click(locators.folders_button_locator)
        folders_button.click()
        sleep(large_delay)

    """Click on the Search in Drive bar."""
    def click_on_search_in_drive(self):
        search_bar = self.wait_to_click(locators.search_bar_locator)
        search_bar.click()
        sleep(large_delay)

    """Click on the New button."""
    def click_on_new_button(self):
        new_button = self.wait_to_click(locators.new_button_selector)
        new_button.click()
        sleep(small_delay)
    

    def click_on_add_button(self):
        # add_button = self.elementary_actions.wait_to_click(locators.add_button_locator)
        # add_button.click()
        # sleep(2)
        autoGUIutils.press_tab()
        autoGUIutils.press_tab()
        autoGUIutils.press_tab()
        autoGUIutils.press_tab()
        autoGUIutils.press_enter()

    def click_on_shortcut_folder_button(self):
        autoGUIutils.press_tab()
        autoGUIutils.press_enter()

    """Navigate to a specific page(available on the left menu.

        Parameters:
        button_name (str): The name of the button representing the page to navigate to.
    """
    

    def navigate_to(self, button_name):
        button_element = self.wait_to_click(locators.left_menu_page_selector(button_name))
        button_element.click()
        sleep(small_delay)


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

class HigherActions(ButtonClicker) :
    def __init__(self, driver, web_driver_wait):
         
        super().__init__(driver,web_driver_wait)
    #     self.driver = driver
    #     self.web_driver_wait = web_driver_wait
    #     self.button_clicker = ButtonClicker(self.driver,self.web_driver_wait)
    #     self.elementary_actions = ElementaryActions(self.driver,self.web_driver_wait)

    
    """Select an item by its name.

        Parameters:
        item_name (str): Name of the item to be selected.
        

        Raises:
        FileNotFoundError: If the item with the specified name is not found.
    """
    def select_item(self, item_name):
        action_chain = ActionChains(self.driver)
        try:
            show_more_button = self.driver.find_element(*locators.show_more_files)
            if show_more_button.is_displayed():
                show_more_button.click()
                sleep(small_delay)
        except NoSuchElementException:
            pass
        # Hand
        sleep(large_delay)
        file_selector = locators.file_selector(item_name)
        file_element = self.wait_for_element(file_selector)
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
            file_element = self.wait_to_click(locators.file_selector(expected_file))  # TODO Check this once
            if not file_element:
                flag = False
                break
            self.double_click_element(file_element)  # TODO ask saad whether opening is needed
            sleep(medium_delay)
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
        old_file_element = self.wait_for_element(locators.file_selector(old_file_name))
        assert old_file_element is None, f"Old file '{old_file_name}' still exists after rename operation."
        # Verify the existence of the new file
        renamed_file_element = self.wait_for_element(locators.file_selector(new_file_name))
        assert renamed_file_element is not None, f"New file '{new_file_name}' not found after rename operation."
        # return tru if bot conditions are satisfied
        return True

    def deal_duplicate_and_await_upload(self):
        # try block to deal with situation of file being there already
        try:
            # to see if the warning of file being alreay ent shows up
            self.wait_for_element(locators.file_already_present_text)
        except EXC.NoSuchElementException:

            print("file not already in google drive, uploading as new file")
        else:
            # to deal with file already exisiting
            autoGUIutils.n_tabs_shift_focus(2)
            pyautogui.press("space")
            sleep(small_delay)
        finally:
            # wait till upload completes, max 10 seconds for now
            self.web_driver_wait.until(EC.presence_of_element_located(
                locators.upload_complete_text))
            sleep(small_delay)

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
            destination_folder_element = self.wait_for_element(locators.file_selector(destination_folder))
            self.double_click_element(destination_folder_element)
            sleep(medium_delay)
        except EXC.StaleElementReferenceException:
            print("StaleElementReferenceException occurred. Retrying...")  # TODO either actually retry or remove "retrying"
        # Verify file presence in the destination folder
        assert self.wait_for_element(locators.file_selector(moved_file_name)) is not None, "File has not been moved successfully to the destination folder"

    """Verify the restoration of a file.

        Parameters:
        file_name (str): Name of the file to be restored.

        Returns:
        bool: True if the file has been restored successfully, False otherwise.
    """
    def verify_restoration(self, file_name):  # REDO this function
        # self.button_clicker.navigate_to("Home")
        self.click_on_search_in_drive()
        sleep(small_delay)
        self.send_keys_to_focused(file_name)
        sleep(small_delay)
        file_element = self.wait_for_element(locators.file_selector(file_name))
        if file_element:
            return True
        else:
            return False

    
    """Move a file to a specified destination folder.

        Parameters:
        move_file_name (str): The name of the file to be moved.
        destination_folder_name (str): The name of the destination folder.
        show_more (bool): Flag indicating whether to click the "Show More" button.

        Raises:
        None
    """

    def move_action(self, move_file_name, destination_folder_name, show_more):
        self.select_item(move_file_name)
        file_element = self.wait_for_element(locators.file_selector(move_file_name))
        destination_folder_element = self.wait_for_element(locators.file_selector(destination_folder_name))
        self.drag_and_drop_element(file_element, destination_folder_element)
        sleep(medium_delay)

    """Rename a file.

        Parameters:
        old_file_name (str): The original name of the file.
        new_file_name (str): The new name of the file.

        Returns:
        bool: True if the file has been renamed successfully, False otherwise.
    """

    def rename_action(self, old_file_name, new_file_name):
        self.select_item(old_file_name)
        self.rename_selected_item(new_file_name)
        self.click_on_ok_button()
        
    
    def undo_rename_action(self, old_file_name, new_file_name):
        self.rename_action(old_file_name, new_file_name)
        # press control+z 
        pyautogui.hotkey('ctrl', 'z')
        result = self.rename_verification(old_file_name, new_file_name)
        return result


    """Get the number of file names.

        Returns:
        int: The number of file names.
    """

    def get_file_names_action(self):
        file_name_divs = self.driver.find_elements(By.CSS_SELECTOR, "div.KL4NAf")
        sleep(medium_delay)
        return len(file_name_divs)

    """Upload a file.

        Parameters:
        file_to_upload (str): The file path of the file to be uploaded.

        Raises:
        None
    """

    def upload_file_action(self, file_to_upload):
        self.click_on_new_button()
        upload_button = self.wait_for_element(locators.new_menu_button_locator("File upload"))
        upload_button.click()
        sleep(medium_delay)
        autoGUIutils.type_into_dialogue_box(file_to_upload)
        # this is utility solely because prerequisites aso reuses this function
        self.deal_duplicate_and_await_upload()
        sleep(medium_delay)

    """Copy a file.

        Parameters:
        file_name_for_copy (str): The name of the file to be copied.

        Returns:
        WebElement: The WebElement of the copied file element.
    """

    def copy_file_action(self, file_name_for_copy):
        self.select_item(file_name_for_copy)
        self.context_click()
        sleep(medium_delay)

        make_a_copy_element = self.wait_to_click(locators.make_a_copy_element_locator)
        make_a_copy_element.click()

        sleep(medium_delay)
        self.driver.refresh()
        sleep(large_delay)
        copied_file_element = self.wait_for_element(locators.copied_file_locator)
        return copied_file_element

    """Search for a file by its name.

        Parameters:
        file_to_be_searched (str): The name of the file to be searched.

        Raises:
        None
    """

    def search_by_name_action(self, file_to_be_searched):
        self.navigate_to("My Drive")
        self.click_on_search_in_drive()
        sleep(2)
        self.send_keys_to_focused(file_to_be_searched)
        autoGUIutils.press_enter()
        # Retrieve file elements from the search results
        file_elements = self.wait_for_elements(locators.file_selector(file_to_be_searched))
        # Extract file names from file elements
        if file_elements:
        # Extract file names from file elements
            file_names = [element.text for element in file_elements]
        
        # Write file names to a text file
            with open("file_names.txt", "w") as file:
                for name in file_names:
                    file.write(name + "\n")
        else:
            print("No matching file elements found.")


    """Search for files by their type.

        Returns:
        int: The number of files found by type.
    """

    def search_by_type_action(self):
        self.navigate_to("My Drive")
        self.click_on_type_button()
        self.click_on_the_required_type()
        file_elements = self.driver.find_elements_by_css_selector("div.KL4NAf")
        # Extract file names from file elements
        file_names = [element.text for element in file_elements]
        sleep(medium_delay)
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
        self.select_item(file_name)
        self.click_action_bar_button("Move to trash")
        sleep(medium_delay)
        assert not self.wait_for_element(locators.file_selector(file_name))

    """Permanently delete a file.

        Parameters:
        delete_forever_file_name (str): The name of the file to be permanently deleted.

        Returns:
        bool: True if the file has been permanently deleted, False otherwise.
    """

    

    def delete_permanently_action(self, delete_forever_file_name):
        self.driver.refresh()
        sleep(large_delay)
        self.button_clicker.navigate_to("Trash")
        self.select_item(delete_forever_file_name)
        self.click_action_bar_button("Move to trash")
        self.navigate_to("Trash")

        deleted_file_locator = locators.file_selector(delete_forever_file_name)
        self.wait_for_element(deleted_file_locator)

        self.select_item(delete_forever_file_name)
        self.click_action_bar_button("Delete forever")
        sleep(small_delay)
        try:
            delete_confirm_btn_element = self.wait_for_element(locators.delete_confirm_button_locator)
            self.click_element(delete_confirm_btn_element)
            sleep(medium_delay)
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
        self.navigate_to("Trash")
        sleep(medium_delay)
        self.select_item(file_name_to_retrieve)
        self.click_action_bar_button("Restore from trash")
        restoration_successful = self.verify_restoration(file_name_to_retrieve)
        sleep(medium_delay)
        return restoration_successful

    """Rename a folder.

        Parameters:
        old_folder_name (str): The original name of the folder.
        new_folder_name (str): The new name of the folder.

        Returns:
        bool: True if the folder has been renamed successfully, False otherwise.
    """

    def rename_folder_action(self, old_folder_name, new_folder_name):
        self.navigate_to("Home")
        self.click_on_folders_button()
        self.select_item(old_folder_name)
        self.rename_selected_item(new_folder_name)
        self.click_on_ok_button()
        result = self.rename_verification(old_folder_name, new_folder_name)
        return result

    """Create a new folder.

        Parameters:
        folder_name (str): The name of the folder to be created.

        Raises:
        None
    """

    def create_folder_action(self, folder_name):
        self.click_on_new_button()
        action_button = self.wait_to_click(locators.new_menu_button_locator("New folder"))
        action_button.click()
        sleep(small_delay)
        autoGUIutils.type_into_dialogue_box(folder_name)
        self.driver.refresh()

    """Remove a folder.

        Parameters:
        folder_to_be_removed (str): The name of the folder to be removed.

        Raises:
        None
    """

    def remove_folder_action(self, folder_to_be_removed):
        self.navigate_to("Home")
        self.click_on_folders_button()
        self.select_item(folder_to_be_removed)
        self.click_action_bar_button("Move to trash")
        sleep(medium_delay) 
        
    def verify_button_tooltips(self, button_names_and_tooltips):
        """
        Verify the tooltip text of buttons like "Home", "My Drive" etc.

        Parameters:
        button_names_and_tooltips (dict): A dictionary containing button names as keys and expected tooltip text as values.

        Returns:
        bool: True if all buttons are present and their tooltips match the expected text, False otherwise.
        """
        # Initialize flag to track verification status
        all_buttons_present = True
        self.navigate_to("Home")

        # Loop through each button name and expected tooltip text
        for button_name, expected_tooltip_text in button_names_and_tooltips.items():
            try:
                # Hover over the button to trigger the tooltip
                button_element = self.wait_for_element(locators.left_menu_page_selector(button_name))
                action_chain = ActionChains(self.driver)
                action_chain.move_to_element(button_element).perform()
                sleep(small_delay)  # Add a short delay to allow the tooltip to appear

                # Get the actual tooltip text
                actual_tooltip_text = button_element.get_attribute('title')

                # Check if the actual tooltip text matches the expected tooltip text
                if actual_tooltip_text != expected_tooltip_text:
                    print(f"Tooltip text for button '{button_name}' does not match. Expected: '{expected_tooltip_text}', Actual: '{actual_tooltip_text}'")
                    all_buttons_present = False
            except NoSuchElementException:
                print(f"Button '{button_name}' not found.")
                all_buttons_present = False

        return all_buttons_present
    

    def verify_file_tooltips(self):
        self.navigate_to("Home")
        # Initialize flag to track verification status
        all_files_verified = True

        # Get the list of file names
        file_name_divs = self.driver.find_elements(By.CSS_SELECTOR, "div.KL4NAf")
        file_names = [file_name_div.text for file_name_div in file_name_divs]

        # Loop through each file name
        for file_name in file_names:
            try:
                # Select the file to trigger the tooltip
                self.select_item(file_name)
                sleep(small_delay)  # Add a short delay to allow the tooltip to appear

                # Get the actual tooltip text
                file_element = self.wait_for_element(locators.file_selector(file_name))
                actual_tooltip_text = file_element.get_attribute('title')

                # Check if the tooltip text is present
                if not actual_tooltip_text:
                    print(f"Tooltip text for file '{file_name}' is not present.")
                    all_files_verified = False
            except NoSuchElementException:
                print(f"File '{file_name}' not found.")
                all_files_verified = False

        return all_files_verified

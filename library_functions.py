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
from selenium.common.exceptions import TimeoutException
import locators
import files
import autoGUIutils

class Helper:
    def __init__(self, driver, web_driver_wait):
        self.driver = driver
        self.web_driver_wait = web_driver_wait

    def wait_for_element(self,locator):
        try:
            element = self.web_driver_wait.until(
                EC.presence_of_element_located(locator))
            return element
        except TimeoutException:
            print(f"Timeout waiting for element with locator {locator}")
            return None
    
    def double_click_element(self,element):
        action_chain = ActionChains(self.driver)
        try:
            action_chain.double_click(element).perform()
        except Exception as e:
            print(f"Error double clicking on element: {e}")
    
    def drag_and_drop_element(self,source_element, destination_element):
        action_chain = ActionChains(self.driver)
        try:
            action_chain.drag_and_drop(
                source_element, destination_element).perform()
        except Exception as e:
            print(f"Error dragging and dropping element: {e}") 

    def wait_to_click(self,locator):
        try:
            element = self.web_driver_wait.until(EC.element_to_be_clickable(locator))
            return element
        except TimeoutException:
            print(f"Timeout waiting for element with locator {locator}")
            return None
    
    def select_item(self, item_name, show_more_needed):
        # show_more_needed is to ensure backwards compatibility
        action_chain = ActionChains(self.driver)
        if (show_more_needed):  # old testcases do not have show_more param, so by default True,
        # newer testcases can explicitly mention if show more button is to be clicked or not before looking for file
        
            show_more_button = self.wait_to_click(
                locators.show_more_files
            )
            show_more_button.click()

        sleep(5)
        
        file_selector = locators.file_selector(item_name)
        file_element = self.wait_for_element(file_selector)
        if file_element:
            
            action_chain.move_to_element(file_element).click()
            action_chain.perform()
        else:
            raise FileNotFoundError
        

    def rename_selected_item(self, new_file_name):
        pyautogui.press('n')
        pyautogui.write(new_file_name)



class ButtonClicker:
    def __init__(self, driver, web_driver_wait, helper):
        self.driver = driver
        self.web_driver_wait = web_driver_wait
        self.helper = helper

    
    def click_action_bar_button(self, button_name):
        button_element = self.helper.wait_to_click(locators.action_bar_button_selector(button_name))
        button_element.click()

    def navigate_to(self, button_name):
        button_element = self.helper.wait_to_click(locators.left_menu_page_selector(button_name))
        button_element.click()
        
    def click_on_ok_button(self):
        ok_button = self.helper.wait_to_click(locators.ok_button_locator)
        ok_button.click()
        sleep(3)

    def click_on_type_button(self):
        type_button = self.helper.wait_to_click(locators.type_button_locator)
        type_button.click()

    def click_on_the_required_type(self):
        required_type = self.helper.wait_to_click(locators.type_of_file_locator)
        required_type.click()
        sleep(6)

    def click_on_folders_button(self):
        folders_button = self.helper.wait_to_click(locators.folders_button_locator)
        folders_button.click()
        sleep(5)

    def click_on_search_in_drive(self):
        search_bar = self.helper.wait_to_click(locators.search_bar_locator)
        search_bar.click()
        sleep(5)

    def click_on_new_button(self):
        new_button = self.helper.wait_to_click(locators.new_button_selector)
        new_button.click()
        sleep(2)

    def context_click(self):
        action_chain = ActionChains(self.driver)
        action_chain.context_click().perform()
    
    def click_element(self,element):
        action_chain = ActionChains(self.driver)
        try:
            action_chain.click(element).perform()
        except Exception as e:
            print(f"Error clicking on element: {e}")





class HigherActions:
    def __init__(self, driver, web_driver_wait, button_clicker, helper):
        self.driver = driver
        self.web_driver_wait = web_driver_wait
        self.button_clicker = button_clicker
        self.helper = helper

    def verify_restoration(self,file_name):
        self.button_clicker.navigate_to("Home")
        # if (self.helper.wait_for_element( locators.file_selector(file_name))):
        #     return True
        # else:
        #     assert False, f"File '{file_name}' Not Restored"
        file_elements = self.search_file_by_name(file_name)
        if(len(file_name) >0):
            return True
        else:
            return False

    def move_action(self,move_file_name,destination_folder_name,show_more):
        
        self.helper.select_item(move_file_name, show_more_needed=show_more)
        sleep(2)
        
        file_element = self.helper.wait_for_element(locators.file_selector(move_file_name))
        destination_folder_element = self.helper.wait_for_element(locators.file_selector(destination_folder_name))
        self.helper.drag_and_drop_element(file_element, destination_folder_element)
        sleep(3)

    def verify_file_in_destination(self,moved_file_name,destination_folder):
        try:
            # Double click the destination folder
            destination_folder_element = self.helper.wait_for_element(locators.file_selector(destination_folder))
            self.helper.double_click_element(destination_folder_element)
            sleep(4)
        except EXC.StaleElementReferenceException:
            print("StaleElementReferenceException occurred. Retrying...")
            
        # Verify file presence in the destination folder
        assert self.helper.wait_for_element(locators.file_selector(moved_file_name))!=None, "File has not been moved successfully to the destination folder"

    def rename_verification(self, old_file_name, new_file_name):
        
        renamed_file_element = self.helper.wait_for_element(locators.file_selector(new_file_name))
        return renamed_file_element != None 

    def select_file_from_trash(self):
        action_chain = ActionChains(self.driver)
        
        file_element = self.helper.wait_for_element(locators.file_selector(files.file_to_be_restored))
                
        if not file_element:
            assert False, "File Not Found in Trash"
        else:
     
            action_chain.move_to_element(file_element).click().perform()
            
            sleep(6)

    def send_keys_to_element(self,element_locator, text):
        try:
            element = self.driver.find_element(*element_locator)
            element.send_keys(text)
        except Exception as e:
            print(f"Error sending keys to element: {e}")

    def send_keys_to_focused( self,text):
        try:
            action_chain = ActionChains(self.driver)
            
            action_chain.send_keys(text)
            action_chain.perform()
            
        except Exception as e:
            print(f"Error sending keys to element: {e}")

    def deal_duplicate_and_await_upload(self):
        # try block to deal with situation of file being there already
        try:
            # to see if the warning of file being alreay ent shows up
            self.helper.wait_for_element(locators.file_already_present_text)
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
            self.web_driver_wait.until(EC.presence_of_element_located(
                locators.upload_complete_text))
            sleep(2)

    def search_file_by_name(self,filename,utilityInstance):
        self.button_clicker.click_on_search_in_drive()
        autoGUIutils.type_into_dialogue_box(filename)
        file_element = self.helper.wait_to_click(locators.file_selector(files.file_to_be_searched))
        self.helper.double_click_element(file_element)
        sleep(3)
        autoGUIutils.go_back_esc()
        return file_element




class CommonActions:
    def __init__(self):
        pass
    
    def setup(self):# TODO to be removed
        self.driver = Chrome()
        self.web_driver_wait = WebDriverWait(self.driver , 10)
    
    def teardown(self):# TODO to be removed
        self.driver.quit()

    
    """
    ## Utility function to rename a folder in Google Drive GUI.

    def rename_folder(old_folder_name, new_folder_name)

    Parameters:
    - old_folder_name (str): The current name of the folder to be renamed.
    - new_folder_name (str): The desired new name for the folder.

    Returns:
    None

    Raises:
    FileNotFoundError: If the folder with the old name does not exist on Google Drive.

    Usage:
    rename_folder(old_folder_name, new_folder_name)
    """

    # def rename_folder(self, old_folder_name, new_folder_name):
    #     action_chain = ActionChains(self.driver)
    #     try:
    #         self.select_item(old_folder_name)
    #     except FileNotFoundError as e:
    #         raise e
    #     else:
    #         folder_element = self.wait_for_element(locators.folder_locator)

    #         action_chain.move_to_element(folder_element).send_keys("n").perform()
    #         action_chain = ActionChains(self.driver)# making a new one instead of clearing

    #         sleep(3)

    #         action_chain.send_keys(new_folder_name).perform()

    #         # Locate and click the OK button
    #         ok_button = self.wait_to_click(locators.ok_button_locator)
    #         ok_button.click()
    #         sleep(10)

        
    """
    Utility function to click on the trash button in the GUI.

    Parameters:
        None

    Returns:
        None

    Raises:
        TimeoutException: If the trash button is not clickable within the specified timeout.

    Usage:
        click_trash_button()
    """

    
    # def click_trash_button(self):
    #     trash_button = self.wait_to_click(locators.left_menu_page_selector("Trash"))
    #     trash_button.click()
    #     sleep(5)
    
    """
    ## Utility function to select a file/folder in Google Drive GUI
    def select_item(item_name,show_more_needed=True)

    Parameters:
    - item_name: Name of file/folder to be selected
    - show_more_needed: If true (default), then click on "Show more results" button

    Returns:
    None

    Raises:
    FileNotFoundError: If the file/folder does not exist on Google Drive.

    Usage:
    select_file(item_name)
    select_file(item_name,show_more_needed=False)

    Additional :
    - show_more_needed is to ensure backwards compatibility
    - old testcases do not have show_more param, so by default True
    - newer testcases can explicitly mention if show more button is to be clicked or not before looking for file
    """
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
            

    

    """
    Utility function to click on the 'Restore from Trash' button in the GUI.

    Parameters:
        None

    Returns:
        None

    Raises:
        TimeoutException: If the 'Restore from Trash' button is not clickable within the specified timeout.

    Usage:
        click_on_restore_from_trash_button()
    """



    # def click_on_restore_from_trash_button(self):
    #     restore_from_trash_button = self.wait_to_click(locators.action_bar_button_selector("Restore from trash"))
    #     restore_from_trash_button.click()
    #     sleep(3)


    # def click_on_home_button(self):
    #     home_button = self.wait_to_click(locators.left_menu_page_selector("Home"))
    #     home_button.click()
    #     sleep(5)

    # def click_on_my_drive_button(self):
    #     my_drive_button = self.wait_to_click(locators.left_menu_page_selector("My Drive"))
    #     my_drive_button.click()
    #     sleep(5)

        
    """
    Utility function to verify if a file has been restored.

    This function clicks on the home button, then checks if the specified file exists in the folder.

    Parameters:
        file_name (str): The name of the file to verify.

    Returns:
        bool: True if the file is restored, False otherwise.

    Raises:
        AssertionError: If the file is not found after restoration.

    Usage:
        verify_restoration(file_name)
    """
    
    # def verify_restoration(self,file_name):
    #     self.click_on_home_button()
    #     if (self.wait_for_element( locators.file_selector(file_name))):
    #         return True
    #     else:
    #         assert False, f"File '{file_name}' Not Restored"

    # def move_action(self,move_file_name,destination_folder_name,show_more):
        
    #     self.select_file(move_file_name, show_more_needed=show_more)
    #     sleep(2)
        
    #     file_element = self.wait_for_element(locators.file_selector(move_file_name))
    #     destination_folder_element = self.wait_for_element(locators.file_selector(destination_folder_name))
    #     self.drag_and_drop_element(file_element, destination_folder_element)
    #     sleep(3)

    


    # def verify_file_in_destination(self,moved_file_name,destination_folder):
    #     try:
    #         # Double click the destination folder
    #         destination_folder_element = self.wait_for_element(locators.file_selector(destination_folder))
    #         self.double_click_element(destination_folder_element)
    #         sleep(4)
    #     except EXC.StaleElementReferenceException:
    #         print("StaleElementReferenceException occurred. Retrying...")
            
    #     # Verify file presence in the destination folder
    #     assert self.wait_for_element(locators.file_selector(moved_file_name))!=None, "File has not been moved successfully to the destination folder"



    # def rename_selected_item(self, new_file_name):
    #     pyautogui.press('n')
    #     pyautogui.write(new_file_name)
    
        
    """
    Utility function to click on the OK button in the GUI.

    Parameters:
        None

    Returns:
        None

    Raises:
        TimeoutException: If the OK button is not clickable within the specified timeout.

    Usage:
        click_on_ok_button()
    """

    # def click_on_ok_button(self):
    #     ok_button = self.wait_to_click(locators.ok_button_locator)
    #     ok_button.click()
    
    #     sleep(3)

        
    """
    Utility function to verify if file renaming was successful.

    Parameters:
        old_file_name (str): The original name of the file.
        new_file_name (str): The new name of the file.

    Returns:
        None

    Raises:
        AssertionError: If the original file is found after renaming, or if the new file is not found after renaming.

    Usage:
        rename_verification(old_file_name, new_file_name)
    """


    # def rename_verification(self, old_file_name, new_file_name):
        
    #     renamed_file_element = self.wait_for_element(locators.file_selector(new_file_name))
    #     if renamed_file_element == None:
    #         assert False, f"New File '{new_file_name}' Not Found after Rename"
    #     else:
    #         assert True , "Rename successfull"

    


    """
    Utility function to select a file from the trash in the GUI.

    Parameters:
        None

    Returns:
        None

    Raises:
        AssertionError: If no file is found in the trash.

    Usage:
        select_file_from_trash()
    """

    # def select_file_from_trash(self):
    #     action_chain = ActionChains(self.driver)
        
    #     file_element = self.wait_for_element(locators.file_selector(files.file_to_be_restored))
                
    #     if not file_element:
    #         assert False, "File Not Found in Trash"
    #     else:
     
    #         action_chain.move_to_element(file_element).click().perform()
            
    #         sleep(6)
    
    """
    ## Utility function to click delete button on a selected file/folder in the Google Drive web GUI.
    def delete_file()

    Parameters:
    None

    Returns:
    None

    Raises:
    -

    Usage:
    delete_file()
    """

    # def delete_file(self):
    #     # click on delete button
    #     delete_button = self.wait_for_element(locators.action_bar_button_selector("Move to trash")) # some times this is called 'Remove' // in edge i guess
    #     delete_button.click()
        
    #     sleep(3)
    
    
    """
    Utility function to open a folder in the Google Drive GUI.

    Parameters:
        folder_name (str): The name of the folder to be opened.

    Returns:
        bool: True if the folder is successfully opened, False otherwise.

    Raises:
        TimeoutException: If the folder cannot be opened within the specified timeout.

    Usage:
        result = open_folder(folder_name)
    """

    # def open_folder(self,folder_name):

    #     try:
         
    #         folder_element = self.select_item(folder_name)
    #         self.double_click_element(folder_element)

    #         return True
    #     except EXC.TimeoutException as e:
    #         print(f"TimeoutException: {e}")
    #         return False

    """
    Utility function to send keys to an element on the web page.

    Parameters:
        element_locator (tuple): A tuple representing the locator strategy and value for the element.
        text (str): The text to be sent to the element.

    Returns:
        None

    Raises:
        Exception: If there is an error sending keys to the element.

    Usage:
        send_keys_to_element(element_locator, text)
    """


    # def send_keys_to_element(self,element_locator, text):
    #     try:
    #         element = self.driver.find_element(*element_locator)
    #         element.send_keys(text)
    #     except Exception as e:
    #         print(f"Error sending keys to element: {e}")

    # def send_keys_to_focused( self,text):
    #     try:
    #         action_chain = ActionChains(self.driver)
            
    #         action_chain.send_keys(text)
    #         action_chain.perform()
            
    #     except Exception as e:
    #         print(f"Error sending keys to element: {e}")
    


    # def context_click(self):
    #     action_chain = ActionChains(self.driver)
    #     action_chain.context_click().perform()


    # def wait_for_element(self,locator):
    #     try:
    #         element = self.web_driver_wait.until(
    #             EC.presence_of_element_located(locator))
    #         return element
    #     except TimeoutException:
    #         print(f"Timeout waiting for element with locator {locator}")
    #         return None


    # def wait_to_click(self,locator):
    #     try:
    #         element = self.web_driver_wait.until(EC.element_to_be_clickable(locator))
    #         return element
    #     except TimeoutException:
    #         print(f"Timeout waiting for element with locator {locator}")
    #         return None


    # def click_element(self,element):
    #     action_chain = ActionChains(self.driver)
    #     try:
    #         action_chain.click(element).perform()
    #     except Exception as e:
    #         print(f"Error clicking on element: {e}")


    # def double_click_element(self,element):
    #     action_chain = ActionChains(self.driver)
    #     try:
    #         action_chain.double_click(element).perform()
    #     except Exception as e:
    #         print(f"Error double clicking on element: {e}")
    

    """
    Utility function to perform a drag-and-drop action in the GUI.

    Parameters:
        source_element (WebElement): The element to be dragged.
        destination_element (WebElement): The element onto which the source element will be dropped.

    Returns:
        None

    Raises:
        None

    Usage:
        drag_and_drop_element(source_element, destination_element)
    """


    # def drag_and_drop_element(self,source_element, destination_element):
    #     action_chain = ActionChains(self.driver)
    #     try:
    #         action_chain.drag_and_drop(
    #             source_element, destination_element).perform()
    #     except Exception as e:
    #         print(f"Error dragging and dropping element: {e}")  


    # def click_on_type_button(self):
    #     type_button = self.wait_to_click(locators.type_button_locator)
    #     type_button.click()

    # def click_on_the_required_type(self):
    #     required_type = self.wait_to_click(locators.type_of_file_locator)
    #     required_type.click()
    #     sleep(6)
        
    # def click_on_folders_button(self):
    #     folders_button = self.wait_to_click(locators.folders_button_locator)
    #     folders_button.click()
    #     sleep(5)

    # def click_on_search_in_drive(self):
    #     search_bar = self.wait_to_click(locators.search_bar_locator)
    #     search_bar.click()
    #     sleep(5)
    
    # def click_on_new_button(self):
    #     # clicks on new button
       
    #     new_button = self.wait_to_click(locators.new_button_selector)
    #     new_button.click()
    #     sleep(2)

      


    # def deal_duplicate_and_await_upload(self):
    #     # try block to deal with situation of file being there already
    #     try:
    #         # to see if the warning of file being alreay ent shows up
    #         self.wait_for_element(locators.file_already_present_text)
    #     except EXC.NoSuchElementException:

    #         print("file not already in google drive, uploading as new file")
    #     else:
    #         # to deal with file already exisiting
    #         pyautogui.press("tab")
    #         pyautogui.press("tab")

    #         sleep(0.5)
    #         pyautogui.press("space")
    #         sleep(1)
    #     finally:
    #         # wait till upload completes, max 10 seconds for now
    #         self.web_driver_wait.until(EC.presence_of_element_located(
    #             locators.upload_complete_text))
    #         sleep(2)



# def navigateTo(self,path):
#     for foldername in path.split("/"):  # A/B/example.mp3
#         if verify_item_presence(foldername):
#             open_folder(foldername)
#             sleep(4)
#             clear_action_chain()
#         else:
#             print(f"navigateTo {path} failed, {foldername} not found!")
#             return -1
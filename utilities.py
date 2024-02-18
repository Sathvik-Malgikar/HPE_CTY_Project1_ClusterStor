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


class Utilities:
    def __init__(self):
        pass
    
    def setup(self):
        self.driver = Chrome(executable_path="./chromedriver.exe")
        self.web_driver_wait = WebDriverWait(self.driver , 10)
    
    def teardown(self):
        self.driver.quit()

    def remove_file(self, file_name):
        try:
            self.select_item(file_name)
        except FileNotFoundError as e:
            raise e
        else:
            self.delete_file()

    def rename_folder(self, old_folder_name, new_folder_name):
        action_chain = ActionChains(self.driver)
        try:
            self.select_item(old_folder_name)
        except FileNotFoundError as e:
            raise e
        else:
            folder_element = self.wait_for_element(*locators.folder_locator)

            action_chain.move_to_element(folder_element).send_keys("n").perform()
            action_chain = ActionChains(self.driver)# making a new one instead of clearing

            sleep(3)

            action_chain.send_keys(new_folder_name).perform()

            # Locate and click the OK button
            ok_button = self.web_driver_wait.until(
                EC.element_to_be_clickable(locators.ok_button_locator))
            ok_button.click()
            sleep(10)


    
    def click_trash_button(self):
        trash_button = self.web_driver_wait.until(
            EC.element_to_be_clickable(locators.trash_button_locator))
        trash_button.click()
        sleep(5)

    def select_item(self, item_name, show_more_needed):
        # show_more_needed is to ensure backwards compatibility
        action_chain = ActionChains(self.driver)
        if (show_more_needed):  # old testcases do not have show_more param, so by default True,
        # newer testcases can explicitly mention if show more button is to be clicked or not before looking for file

            self.web_driver_wait.until(
                EC.presence_of_element_located(
                    locators.show_more_files
                ),
            )
            show_more_button = self.wait_for_element(
                *locators.show_more_files
            )
            show_more_button.click()

        sleep(5)
        # Find file
        try:
            file_selector = locators.file_selector(item_name)
            file_element = self.wait_for_element(file_selector)
        except:
            raise FileNotFoundError("File Not found")
        else:
            
            action_chain.move_to_element(file_element).click()
            action_chain.perform()



    def click_on_restore_from_trash_button(self):
        restore_from_trash_button = self.web_driver_wait.until(
            EC.element_to_be_clickable(locators.restore_from_trash_button_locator))
        restore_from_trash_button.click()
        sleep(3)


    def click_on_home_button(self):
        home_button = self.web_driver_wait.until(
            EC.element_to_be_clickable(locators.home_button_locator))
        home_button.click()
        sleep(3)

    
    def verify_restoration(self,file_name):
        self.click_on_home_button()
        if (self.verify_item_presence(file_name)):
            return True
        else:
            assert False, f"File '{file_name}' Not Restored"

    def rename_selected_item(self, new_file_name):
        pyautogui.press('n')
        pyautogui.write(new_file_name)

    def click_on_ok_button(self):
        ok_button = self.web_driver_wait.until(
            EC.element_to_be_clickable(locators.ok_button_locator))
        ok_button.click()
    
        sleep(3)

    def rename_verification(self, old_file_name, new_file_name):
        
        renamed_file_element = self.wait_for_element(locators.renamed_file_name_selector)
        if renamed_file_element == None:
            assert False, f"New File '{new_file_name}' Not Found after Rename"
        else:
            assert True , "Rename successfull"


    def select_file_from_trash(self):
        action_chain = ActionChains(self.driver)
        
        file_element = self.wait_for_element(locators.trashed_file_locator)
                
        if not file_element:
            assert False, "File Not Found in Trash"
        else:
     
            action_chain.move_to_element(file_element).click().perform()
            
            sleep(6)
        
    def delete_file(self):
        # click on delete button
        self.web_driver_wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//div[@role='button' and @aria-label='Move to trash' and @aria-hidden='false' and @aria-disabled='false']",
                )
            ),
        )
        delete_button = self.driver.find_element(
            By.XPATH,
            "//div[@role='button' and @aria-label='Move to trash' and @aria-hidden='false' and @aria-disabled='false']",
        )
        delete_button.click()
        sleep(3)
    
    def open_folder(self,open_folder):

        try:
            # Use a CSS selector to find the file by its name
            file_locator = (By.CSS_SELECTOR,
                            f'div.uXB7xe[aria-label*="{open_folder}"]')
            folder_element = self.driver.find_element(*file_locator)
            self.double_click_element(folder_element)

            return True
        except EXC.TimeoutException as e:
            print(f"TimeoutException: {e}")
            return False


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
    


    def context_click(self):
        action_chain = ActionChains(self.driver)
        action_chain.context_click().perform()

    def verify_item_presence(self,item_name, timeout=10):
        item_locator = (
            By.XPATH, f'//div[@class="uXB7xe" and contains(@aria-label,"{item_name}" )]')
        return self.wait_for_element(item_locator)
  


    def wait_for_element(self,locator):
        try:
            element = self.web_driver_wait.until(
                EC.presence_of_element_located(locator))
            return element
        except TimeoutException:
            print(f"Timeout waiting for element with locator {locator}")
            return None


    def wait_to_click(self,locator):
        try:
            element = self.web_driver_wait.until(EC.element_to_be_clickable(locator))
            return element
        except TimeoutException:
            print(f"Timeout waiting for element with locator {locator}")
            return None


    def click_element(self,element):
        action_chain = ActionChains(self.driver)
        try:
            action_chain.click(element).perform()
        except Exception as e:
            print(f"Error clicking on element: {e}")


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




    def click_on_new_button(self):
        # clicks on new button
        self.web_driver_wait.until(EC.element_to_be_clickable(
            locators.new_button_selector))
        new_button = self.wait_for_element(*locators.new_button_selector)
        new_button.click()
        sleep(2)

        # clicks on new file
        self.web_driver_wait.until(EC.element_to_be_clickable(
            locators.file_upload_button_selector))
        upload_button = self.wait_for_element(*locators.file_upload_button_selector)
        upload_button.click()
        sleep(3)


    def deal_duplicate_and_await_upload(self):
        # try block to deal with situation of file being there already
        try:
            # to see if the warning of file being alreay present shows up
            self.wait_for_element(*locators.file_already_present_text)
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
"""
Utility function to undo delete action in the Google Drive web GUI.
"""
# def undo_delete_action(driver, action_chain, web_driver_wait, file_to_be_retrieved):
#     trash_button = web_driver_wait.until(EC.element_to_be_clickable(locators.trash_button_locator))
#     trash_button.click()
#     sleep(5)

#     try:
#         web_driver_wait.until(EC.presence_of_element_located(locators.trashed_file_locator))
#     except:
#         assert False, "File Not Found in Trash"
#     else:
#         # Click on the trashed file
#         trashed_file_element = driver.find_element(*locators.trashed_file_locator)
#         action_chain.move_to_element(trashed_file_element).click().perform()
#         sleep(6)
#         restore_from_trash_button = web_driver_wait.until(EC.element_to_be_clickable(locators.restore_from_trash_button_locator))
#         restore_from_trash_button.click()
#         sleep(3)

#     # Check whether the file has actually been restored or not
#     try:
#         home_button = web_driver_wait.until(EC.element_to_be_clickable(locators.home_button_locator))
#         home_button.click()
#         sleep(3)
#         web_driver_wait.until(EC.presence_of_element_located(locators.restored_file_locator))
#     except:
#         assert False, f"File '{file_to_be_retrieved}' Not Restored"




# def navigateTo(self,path):
#     for foldername in path.split("/"):  # A/B/example.mp3
#         if verify_item_presence(foldername):
#             open_folder(foldername)
#             sleep(4)
#             clear_action_chain()
#         else:
#             print(f"navigateTo {path} failed, {foldername} not found!")
#             return -1

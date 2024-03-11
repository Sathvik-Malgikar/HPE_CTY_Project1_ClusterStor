from time import sleep
import pyautogui
from selenium.webdriver.common.action_chains import ActionChains
import selenium.common.exceptions as EXC
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import locators
import files#TODO REMOVE THIS
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
        file_elements = self.search_file_by_name(file_name)
        if(len(file_elements) >0):
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
            print("StaleElementReferenceException occurred. Retrying...")# TODO either actually retry or remove "retrying"
            
        # Verify file presence in the destination folder
        assert self.helper.wait_for_element(locators.file_selector(moved_file_name))!=None, "File has not been moved successfully to the destination folder"

    def rename_verification(self, old_file_name, new_file_name):
        
        # TODO old file shouldnt exist, verify that.
        renamed_file_element = self.helper.wait_for_element(locators.file_selector(new_file_name))
        return renamed_file_element != None 

    def select_file_from_trash(self):# TODO parmeterize filename just like select_file and merge these two functions.
        action_chain = ActionChains(self.driver)
        
        file_element = self.helper.wait_for_element(locators.file_selector(files.file_to_be_restored))
        #TODO REMOVE "files" AND PARAMTERIZE
                
        if not file_element:
            assert False, "File Not Found in Trash"
        else:
     
            action_chain.move_to_element(file_element).click().perform()
            
            sleep(6)

    def send_keys_to_element(self,element_locator, text):# TODO not high level , so shift elsewhere
        try:
            element = self.driver.find_element(*element_locator)
            element.send_keys(text)
        except Exception as e:
            print(f"Error sending keys to element: {e}")

    def send_keys_to_focused( self,text):# TODO not high level , so shift elsewhere
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

    def search_file_by_name(self,filename):
        self.button_clicker.click_on_search_in_drive()
        autoGUIutils.type_into_dialogue_box(filename)
    
    def verify_search_results(self,expected_file_list):#TODO return one boolean
        flag=True
        for expected_file in expected_file_list:
                
            file_element = self.helper.wait_to_click(locators.file_selector(expected_file))# TODO Check this once
            if not file_element:
                flag=False
                break
            self.helper.double_click_element(file_element)#TODO ask saad whether opening is needed
            sleep(3)
            autoGUIutils.go_back_esc()
        return flag
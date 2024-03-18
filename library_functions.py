from time import sleep
import pyautogui
from selenium.webdriver.common.action_chains import ActionChains
import selenium.common.exceptions as EXC
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import locators
import autoGUIutils
from selenium.webdriver.common.by import By

class ElementaryActions:
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
        

    def rename_selected_item(self, new_file_name):
        pyautogui.press('n')
        pyautogui.write(new_file_name)

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
    
    def click_element(self,element):
        action_chain = ActionChains(self.driver)
        try:
            action_chain.click(element).perform()
        except Exception as e:
            print(f"Error clicking on element: {e}")



class ButtonClicker:
    def __init__(self, driver, web_driver_wait, helper):
        self.driver = driver
        self.web_driver_wait = web_driver_wait

    def click_action_bar_button(self, button_name):
        button_element = ElementaryActions.wait_to_click(locators.action_bar_button_selector(button_name))
        button_element.click()

    def navigate_to(self, button_name):
        button_element = ElementaryActions.wait_to_click(locators.left_menu_page_selector(button_name))
        button_element.click()
        
    def click_on_ok_button(self):
        ok_button = ElementaryActions.wait_to_click(locators.ok_button_locator)
        ok_button.click()
        sleep(3)

    def click_on_type_button(self):
        type_button = ElementaryActions.wait_to_click(locators.type_button_locator)
        type_button.click()

    def click_on_the_required_type(self):
        required_type = ElementaryActions.wait_to_click(locators.type_of_file_locator)
        required_type.click()
        sleep(6)

    def click_on_folders_button(self):
        folders_button = ElementaryActions.wait_to_click(locators.folders_button_locator)
        folders_button.click()
        sleep(5)

    def click_on_search_in_drive(self):
        search_bar = ElementaryActions.wait_to_click(locators.search_bar_locator)
        search_bar.click()
        sleep(5)

    def click_on_new_button(self):
        new_button = ElementaryActions.wait_to_click(locators.new_button_selector)
        new_button.click()
        sleep(2)

    

class Helper:
    def __init__(self, driver, web_driver_wait):
        self.driver = driver
        self.web_driver_wait = web_driver_wait
    
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
    
    def verify_search_results(self,expected_file_list):#TODO return one boolean
        flag=True
        for expected_file in expected_file_list:
                
            file_element = ElementaryActions.wait_to_click(locators.file_selector(expected_file))# TODO Check this once
            if not file_element:
                flag=False
                break
            ElementaryActions.double_click_element(file_element)#TODO ask saad whether opening is needed
            sleep(3)
            autoGUIutils.go_back_esc()
        return flag
    
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
    
    def verify_file_in_destination(self,moved_file_name,destination_folder):
        try:
            # Double click the destination folder
            destination_folder_element = ElementaryActions.wait_for_element(locators.file_selector(destination_folder))
            ElementaryActions.double_click_element(destination_folder_element)
            sleep(4)
        except EXC.StaleElementReferenceException:
            print("StaleElementReferenceException occurred. Retrying...")# TODO either actually retry or remove "retrying"
            
        # Verify file presence in the destination folder
        assert ElementaryActions.wait_for_element(locators.file_selector(moved_file_name))!=None, "File has not been moved successfully to the destination folder"

    def verify_restoration(self,file_name):            #REDO this function
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
    

class HigherActions:
    def __init__(self, driver, web_driver_wait, button_clicker, helper):
        self.driver = driver
        self.web_driver_wait = web_driver_wait
        self.button_clicker = button_clicker
        self.helper = helper

    def move_action(self,move_file_name,destination_folder_name,show_more):
        
        self.helper.select_item(move_file_name, show_more_needed=show_more)
        sleep(2)
        file_element = self.helper.wait_for_element(locators.file_selector(move_file_name))
        destination_folder_element = self.helper.wait_for_element(locators.file_selector(destination_folder_name))
        self.helper.drag_and_drop_element(file_element, destination_folder_element)
        sleep(3)

    def rename_action(self,old_file_name,new_file_name):
        self.helper.select_item(old_file_name, True)
        self.helper.rename_selected_item(new_file_name)
        self.button_clicker.click_on_ok_button()
        result = self.helper.rename_verification(old_file_name, new_file_name)
        return result
    
    def get_file_names_action(self):
        file_name_divs = self.driver.find_elements(By.CSS_SELECTOR , 
            "div.KL4NAf")
        sleep(4)
        return len(file_name_divs)
    
    def upload_file_action(self,file_to_upload):
        self.button_clicker.click_on_new_button()
        upload_button = self.helper.wait_for_element(locators.new_menu_button_locator("File upload"))
        upload_button.click()
        sleep(2)
        autoGUIutils.type_into_dialogue_box(file_to_upload)
        # this is utility solely because prerequisites aso reuses this function
        self.helper.deal_duplicate_and_await_upload()

    def copy_file_action(self,file_name_for_copy):
        self.helper.select_item(file_name_for_copy,show_more_needed=True)
        self.button_clicker.context_click()
        sleep(5)

        make_a_copy_element = self.helper.wait_to_click(locators.make_a_copy_element_locator)
        make_a_copy_element.click()

        sleep(5)
        self.driver.refresh()
        sleep(7)
        copied_file_element = self.helper.wait_for_element(locators.copied_file_locator)
        return copied_file_element
    
    def search_by_name_action(self,file_to_be_searched):
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
    
    def remove_file_action(self,file_name):
        self.helper.select_item(file_name,True)
        self.button_clicker.click_action_bar_button("Move to trash")  
        sleep(6)
        assert not self.helper.wait_for_element(locators.file_selector(file_name)) 

    def delete_permanently_action(self,delete_forever_file_name):
        self.driver.refresh()
        sleep(5)    
        self.helper.select_item( delete_forever_file_name,False)
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
        except:
            return False
        return True
    
    def undo_delete_action(self,file_name_to_retrieve):
        self.button_clicker.navigate_to("Trash")
        sleep(4)
        self.helper.select_item(file_name_to_retrieve, show_more_needed=False)
        self.button_clicker.click_action_bar_button("Restore from trash")
        restoration_successful = self.higher_actions.verify_restoration(file_name_to_retrieve)
        sleep(4)
        return restoration_successful
    
    def rename_folder_action(self,old_folder_name,new_folder_name):
        self.button_clicker.navigate_to("Home")
        self.button_clicker.click_on_folders_button
        self.helper.select_item(old_folder_name,True)
        self.helper.rename_selected_item(new_folder_name)
        self.button_clicker.click_on_ok_button()
        result = self.higher_actions.rename_verification(old_folder_name, new_folder_name)
        return result
    
    def create_folder_action(self,folder_name):
        self.button_clicker.click_on_new_button()
            
        action_button = self.helper.wait_to_click(locators.new_menu_button_locator("New folder"))
        action_button.click()
        sleep(2)

        autoGUIutils.type_into_dialogue_box(folder_name)
        
        self.driver.refresh()

    def remove_folder_action(self,folder_to_be_removed):
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
    

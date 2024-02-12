import configparser
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
import locators
import files
import utilities


class DriveUtils:
    def __init__(self, driver : Chrome, action_chain : ActionChains, web_driver_wait : WebDriverWait):
        self.driver = driver
        self.action_chain = action_chain
        self.web_driver_wait = web_driver_wait
    
    def remove_file(self, file_name):
        utilities.remove_file(self.driver, self.action_chain, self.web_driver_wait, file_name)

    def rename_file(self, old_file_name, new_file_name):
        utilities.rename_file(self.driver, self.action_chain, self.web_driver_wait, old_file_name, new_file_name)

    def rename_folder(self, old_folder_name, new_folder_name):
        utilities.rename_folder(self.driver, self.action_chain, self.web_driver_wait, old_folder_name, new_folder_name)

    def undo_delete_action(self, file_name_to_retrieve):
        utilities.undo_delete_action(self.driver, self.action_chain, self.web_driver_wait, file_name_to_retrieve)

    def select_file(self, file_name, show_more_needed=False):
        utilities.select_file(self.driver, self.action_chain, self.web_driver_wait, file_name, show_more_needed)

    def click_trash_button(self):
        utilities.click_trash_button(self.web_driver_wait)
    
    def select_file_to_be_restored(self, file_to_be_restored):
        utilities.select_file_to_be_restored(self.driver, self.action_chain, self.web_driver_wait, file_to_be_restored)
    
    def clcik_on_restore_from_trash_button(self):
        utilities.clcik_on_restore_from_trash_button(self.web_driver_wait)
    
    def clcik_on_home_button(self):
        utilities.clcik_on_home_button(self.web_driver_wait)
    
    def verify_restoration(self, file_name):
        utilities.verify_restoration(self.web_driver_wait, file_name)


"""
    Pytest fixture for providing a Selenium WebDriver instance with Chrome.
"""
@pytest.fixture(scope="session", autouse=True)
def driver():
    # svc = Service(executable_path="./chromedriver.exe")
    webdriver = Chrome(executable_path="./chromedriver.exe")
    yield webdriver
    webdriver.quit()


"""
    Pytest fixture for providing an ActionChains instance for Selenium WebDriver.
"""
@pytest.fixture(scope="session", autouse=True)
def action_chain(driver):
    chain = ActionChains(driver)
    yield chain
    chain.reset_actions()
    for device in chain.w3c_actions.devices:
        device.clear_actions()


"""
    Pytest fixture for providing a WebDriverWait instance for Selenium WebDriver.
"""
@pytest.fixture(scope="session", autouse=True)
def web_driver_wait(driver):
    w_wait = WebDriverWait(driver, 10)
    yield w_wait

@pytest.fixture(scope="session", autouse=True)
def drive_utils(driver, action_chain, web_driver_wait):
    return DriveUtils(driver, action_chain, web_driver_wait)



"""
    Test function for signing into Google Drive using Selenium WebDriver.
"""
def test_signin(drive_utils):
    drive_utils.driver.get("https://www.google.com/intl/en-US/drive/")
    drive_utils.driver.maximize_window()
    sleep(0.8)

    drive_utils.web_driver_wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Sign in")))

    signin_ele = drive_utils.driver.find_element(By.LINK_TEXT, "Sign in")
    signin_ele.click()
    sleep(1.3)
    # opened by clicking sign-in anchor tag
    sign_in_tab = drive_utils.driver.window_handles[-1]
    drive_utils.driver.switch_to.window(sign_in_tab)
    sleep(1.3)
    cfp = configparser.ConfigParser()
    cfp.read("config.ini")
    account_email_id = cfp.get("Account Credentials", "email")
    print("Sending email")
    drive_utils.action_chain.send_keys(account_email_id)
    drive_utils.action_chain.send_keys(Keys.ENTER)
    drive_utils.action_chain.perform()
    drive_utils.web_driver_wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//span[contains(text(), 'Welcome')]")
        ),
    )
    sleep(1.5)  # to deal with input animation
    drive_utils.action_chain.reset_actions()
    for device in drive_utils.action_chain.w3c_actions.devices:
        device.clear_actions()
    account_pwd = cfp.get("Account Credentials", "password")
    drive_utils.action_chain.send_keys(account_pwd)
    drive_utils.action_chain.send_keys(Keys.ENTER)
    drive_utils.action_chain.perform()
    sleep(5)
  
    try:
        drive_utils.web_driver_wait.until(EC.title_is("Home - Google Drive"))
        assert True
       
    except TimeoutError:
        assert False
    else:
        pyautogui.keyDown("ctrl")
        pyautogui.press("-")
        pyautogui.press("-")
        pyautogui.keyUp("ctrl")
        


"""
    Test function to retrieve filenames from the Google Drive web GUI.
"""
def test_get_filenames(drive_utils):
    file_name_divs = drive_utils.driver.find_elements_by_css_selector("div.KL4NAf")
    sleep(4)
    assert len(file_name_divs) > 0


"""
Test function to remove a file from the Google Drive web GUI.
"""
def test_remove_file(drive_utils):
    file_name = files.trashed_file_name
    drive_utils.remove_file(file_name)
    drive_utils.driver.refresh()


"""
Test function to rename a file in the Google Drive web GUI.
"""
def test_rename_file(drive_utils):
    old_file_name = files.file_name
    new_file_name = files.renamed_file_name
    drive_utils.rename_file(old_file_name, new_file_name)
    drive_utils.driver.refresh()


"""
Test function to rename a folder in the Google Drive web GUI.
"""
def test_rename_folder(driver, action_chain, web_driver_wait):
    old_folder_name = files.folder_name
    new_folder_name = files.renamed_folder_name
    utilities.rename_folder(driver, action_chain, web_driver_wait, old_folder_name, new_folder_name)
    # driver.refresh()
    assert True

"""
Test function to undo delete action in the Google Drive web GUI.
"""
def test_undo_delete_action(drive_utils):
    file_name_to_retrieve = files.file_to_be_restored
    drive_utils.click_trash_button()
    drive_utils.select_file_to_be_restored(file_name_to_retrieve)
    drive_utils.clcik_on_restore_from_trash_button()
    drive_utils.verify_restoration(file_name_to_retrieve)


"""
## Test function to create a new folder in the Google Drive web GUI.
"""
def test_create_folder(driver, action_chain, web_driver_wait):
    # wait until the New button is clickable
    new_btn = web_driver_wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                '//*[@id="drive_main_page"]/div/div[3]/div/button[1]/span[1]/span',
            )
        )
    )
    new_btn.click()
    sleep(4)

    # wait for the list of options to appear
    new_folder_option = web_driver_wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="drive_main_page"]/div/div[3]/div/button[1]')
        )
    )

    # move to the list and click on the New folder option
    action_chain.move_to_element(new_folder_option).click().perform()

    # Wait for the new folder dialog to appear
    # new_folder_dialog = web_driver_wait.until(
    #     EC.presence_of_element_located((By.CLASS_NAME,"FidVJb"))
    # )

    web_driver_wait.until(EC.presence_of_element_located((By.CLASS_NAME, "LUNIy")))

    # Find the input field and clear any existing text
    input_field = driver.find_element(By.CSS_SELECTOR, ".LUNIy")
    input_field.clear()
    # sleep(5)

    input_field.send_keys("Applied crypto")
    input_field.send_keys(Keys.ENTER)

    sleep(10)
    # #Wait for the folder element to appear in the list
    folder_element = web_driver_wait.until(
        EC.presence_of_element_located((By.XPATH, "//*[text()='Applied crypto']"))
    )
    assert folder_element.is_displayed(), "Folder element is not visible"


"""
## Test function to upload new file in the Google Drive web GUI.
"""
def test_upload_file(driver,web_driver_wait,action_chain):
    FILE_TO_UPLOAD = "Screenshot (177).png" # this file is present in User folder
    
    # clicks on new button
    web_driver_wait.until(EC.element_to_be_clickable(locators.new_button_selector))
    btn = driver.find_element(*locators.new_button_selector)
    btn.click()
    sleep(2)
    
    # clicks on new file
    web_driver_wait.until(EC.element_to_be_clickable(locators.file_upload_button_selector))
    btn = driver.find_element(*locators.file_upload_button_selector)
    btn.click()
    sleep(3)
    
    # types into dialogue box
    pyautogui.typewrite(FILE_TO_UPLOAD)
    sleep(1)
    pyautogui.press("enter")
    sleep(5)
    
    # try block to deal with situation of file being there already
    try:
        # to see if the warning of file being alreay present shows up
        driver.find_element(*locators.file_already_present_text)
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
        web_driver_wait.until(EC.presence_of_element_located(locators.upload_complete_text))
        sleep(2)
        # a refresh to make sure file shows up
        driver.refresh()
        
        # a small wait to ensure page is stable after refresh
        web_driver_wait.until(EC.presence_of_element_located(locators.file_name_containerdiv))
        sleep(5)
        
        # looks for the uploade file in drive 
        file_name_divs = driver.find_elements(*locators.file_name_containerdiv)
        file_names= list(map(lambda a:a.text, file_name_divs))
        assert FILE_TO_UPLOAD in file_names
    
"""
## Test function to download a file in the Google Drive web GUI.
"""  
def test_download_file(driver,web_driver_wait,action_chain):
    web_driver_wait.until(EC.element_to_be_clickable(locators.file_selector(files.renamed_file_name)))
    sleep(2)
    btn = driver.find_element(*locators.file_selector(files.renamed_file_name))
    btn.click()
    web_driver_wait.until(EC.element_to_be_clickable(locators.download_file_selector))
    sleep(2)
    btn = driver.find_element(*locators.download_file_selector)
    btn.click()
    sleep(3)

"""
## Test function to remove multiple files in the Google Drive web GUI.
"""
def test_remove_multiple_files(driver, action_chain, web_driver_wait):
    files = ['test.txt','test1.txt']
    for file in files:
        try:
            utilities.remove_file(driver, action_chain, web_driver_wait,file)
        except FileNotFoundError as e:
            assert False,repr(e)
        finally:
            action_chain.reset_actions()
            for device in action_chain.w3c_actions.devices:
                device.clear_actions()
            driver.refresh()




def test_copy_file(driver, action_chain, web_driver_wait):
    file_name = 'test.txt'
   
    utilities.select_file(driver, action_chain, web_driver_wait, file_name)
    action_chain.context_click().perform()

    sleep(2)

    make_a_copy_element = driver.find_element(By.CSS_SELECTOR, 'div[aria-label="Make a copy"]')
    make_a_copy_element.click()
 
    sleep(2)
    
    expected_copied_file_name = f'Copy of {file_name}'

    copied_file_element = utilities.is_file_found(driver, web_driver_wait, expected_copied_file_name)

        
    assert copied_file_element is not None

 

def test_move_file(driver, action_chain, web_driver_wait):
   
    file_name = "test2.txt"
    destination_folder_name = "After_rename"

    utilities.select_file(driver,action_chain,web_driver_wait,file_name,show_more_needed=True)
    utilities.clear_action_chain(action_chain)
    sleep(2)
    
    file_element = driver.find_element(By.CSS_SELECTOR, f'div.uXB7xe[aria-label*="{file_name}"]')
    destination_folder_element = driver.find_element(By.XPATH, f'//div[contains(@aria-label, "{destination_folder_name}")]')

    action_chain.drag_and_drop(file_element, destination_folder_element).perform()
    sleep(5)
    
    
    
    

def test_view_file_info(driver, action_chain, web_driver_wait):
    file_name = 'test.txt'  # Replace with the file you want to view info for
    utilities.select_file(driver, action_chain, web_driver_wait, file_name)
    

    action_chain.send_keys("gd").perform()
    
    # Wait for the file info dialog to appear
    web_driver_wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.wbg7nb"))
    )
    
    # Assert that the file info dialog is visible
    try:
        file_info_dialog_locator = (
            By.CSS_SELECTOR,
            "div.wbg7nb",
        )
        web_driver_wait.until(
            EC.presence_of_element_located(file_info_dialog_locator)
        )
    except:
        assert False, f"File info dialog for {file_name} is not visible"

        
def test_delete_file_permanently(driver, action_chain, web_driver_wait):
    driver.refresh()
    sleep(5)
    file_name = 'test.txt'  # Replace with the file you want to delete permanently
    utilities.remove_file(driver, action_chain, web_driver_wait, file_name)

    # Empty the trash
    web_driver_wait.until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='Trash']"))
    ).click()
    
    # Wait for the deleted file to appear in the trash
    deleted_file_locator = locators.file_selector(file_name)
    web_driver_wait.until(
        EC.presence_of_element_located(deleted_file_locator)
    )
    
    utilities.clear_action_chain(action_chain)
    # Select the file in the trash
    utilities.select_file(driver, action_chain, web_driver_wait, file_name, show_more_needed=False)
    
    # Click on the "Delete forever" button
    delete_forever_button_locator = (By.XPATH, "//div[@aria-label='Delete forever']")
    web_driver_wait.until(
        EC.element_to_be_clickable(delete_forever_button_locator)
    ).click()
    
    # Add a sleep for 2 seconds to even it out
    sleep(2)

    
    web_driver_wait.until(
        EC.element_to_be_clickable(locators.delete_confirm_button_locator)
    )
    
    # Assert that the file is permanently deleted
    try:
        confirm_btn_element = driver.find_element(*locators.delete_confirm_button_locator)
        confirm_btn_element.click()
        sleep(3)
    except:
        assert False, "Error occured"
    else:
        assert True, f"{file_name} is permanently deleted"


"""
## Test function to logout from the Google Drive web GUI.
"""
def test_logout(driver, action_chain, web_driver_wait):

    # Click on the user profile button to open the menu
    
    user_profile_button_locator = (By.XPATH, '//*[@id="gb"]/div[2]/div[3]/div[1]/div[2]/div') 
    web_driver_wait.until(EC.presence_of_element_located(user_profile_button_locator))
    user_profile_button = driver.find_element(*user_profile_button_locator)
    action_chain.move_to_element(user_profile_button).click().perform()
    sleep(2)

    # Click on the "Sign out" button in the menu
    try:
        sign_out_button_locator = (By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div/div/div/div[2]/div/div[2]/div[2]/span/span[2]')
    
        web_driver_wait.until(EC.presence_of_element_located(sign_out_button_locator))
        sign_out_button = driver.find_element(*sign_out_button_locator)
        action_chain.move_to_element(sign_out_button).click().perform()

        # Wait for the logout to complete
        web_driver_wait.until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, "Sign out")))
    except Exception as e:
        print("error occured ",e)
        
    # Assert that the login screen is visible after logging out
    assert driver.title == "Home - Google Drive"
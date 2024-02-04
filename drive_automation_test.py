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
import locators
import utilities

"""
    Pytest fixture for providing a Selenium WebDriver instance with Chrome.

    Yields:
    WebDriver: A Selenium WebDriver instance.

    Cleanup:
    Quits the WebDriver instance after the test session.

    Usage:
    This fixture can be used in test functions by including it as a parameter.

    Example:
    def test_example(driver):
        # Use driver in your test
        driver.get("https://example.com")
        # Rest of the test logic
"""


@pytest.fixture(scope="session")
def driver():
    # svc = Service(executable_path="./chromedriver.exe")
    webdriver = Chrome(executable_path="./chromedriver.exe")
    yield webdriver
    webdriver.quit()


"""
    Pytest fixture for providing an ActionChains instance for Selenium WebDriver.

    Args:
    - driver (WebDriver): The Selenium WebDriver instance.

    Yields:
    ActionChains: An ActionChains instance.

    Cleanup:
    Resets and clears actions from the ActionChains instance after it has been used in a test.

    Usage:
    This fixture can be used in test functions by including it as a parameter.

    Example:
    def test_example(action_chain):
        # Use action_chain in your test
        action_chain.move_to_element(element).click().perform()
        # Rest of the test logic
"""


@pytest.fixture
def action_chain(driver):
    chain = ActionChains(driver)
    yield chain
    chain.reset_actions()
    for device in chain.w3c_actions.devices:
        device.clear_actions()


"""
    Pytest fixture for providing a WebDriverWait instance for Selenium WebDriver.

    Args:
    - driver (WebDriver): The Selenium WebDriver instance.

    Yields:
    WebDriverWait: A WebDriverWait instance with a timeout of 10 seconds.

    Usage:
    This fixture can be used in test functions by including it as a parameter.

    Example:
    def test_example(web_driver_wait):
        # Use web_driver_wait in your test
        element = web_driver_wait.until(
            EC.presence_of_element_located((By.ID, "example_element"))
        )
        # Rest of the test logic
"""


@pytest.fixture
def web_driver_wait(driver):
    w_wait = WebDriverWait(driver, 10)
    yield w_wait


"""
    Test function for signing into Google Drive using Selenium WebDriver.

    Parameters:
    - driver (WebDriver): The Selenium WebDriver instance.
    - action_chain (ActionChains): The Selenium ActionChains instance for performing user actions.
    - web_driver_wait (WebDriverWait): The Selenium WebDriverWait instance for waiting on elements.

    Returns:
    None

    Raises:
    AssertionError: If the title of the page after signing in is not "Home - Google Drive".

    Usage:
    test_signin(driver, action_chain, web_driver_wait)
"""


def test_signin(driver, action_chain, web_driver_wait):
    driver.get("https://www.google.com/intl/en-US/drive/")
    driver.maximize_window()
    sleep(0.8)

    web_driver_wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Sign in")))

    signin_ele = driver.find_element(By.LINK_TEXT, "Sign in")
    signin_ele.click()
    sleep(1.3)
    # opened by clicking sign-in anchor tag
    sign_in_tab = driver.window_handles[-1]
    driver.switch_to.window(sign_in_tab)
    sleep(1.3)
    cfp = configparser.ConfigParser()
    cfp.read("config.ini")
    account_email_id = cfp.get("Account Credentials", "email")
    print("Sending email")
    action_chain.send_keys(account_email_id)
    action_chain.send_keys(Keys.ENTER)
    action_chain.perform()
    web_driver_wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//span[contains(text(), 'Welcome')]")
        ),
    )
    sleep(1.5)  # to deal with input animation
    action_chain.reset_actions()
    for device in action_chain.w3c_actions.devices:
        device.clear_actions()
    account_pwd = cfp.get("Account Credentials", "password")
    action_chain.send_keys(account_pwd)
    action_chain.send_keys(Keys.ENTER)
    action_chain.perform()
    sleep(5)
  
    try:
        web_driver_wait.until(EC.title_is("Home - Google Drive"))
        assert True
       
    except TimeoutError:
        assert False
    else:
        pyautogui.keyDown("ctrl")
        pyautogui.press("-")
        pyautogui.press("-")
        pyautogui.keyUp("ctrl")
        




"""
Test function to rename a file in the Google Drive web GUI.

Parameters:
- driver (WebDriver): The Selenium WebDriver instance.
- action_chain (ActionChains): The Selenium ActionChains instance for performing user actions.
- web_driver_wait (WebDriverWait): The Selenium WebDriverWait instance for waiting on elements.

Returns:
None

Raises:
AssertionError: If the file is not found or cannot be renamed.

Usage:
test_rename_file(driver, action_chain, web_driver_wait)
"""


def test_rename_file(driver, action_chain, web_driver_wait):
    file_name = "cty_ppt.pdf" # TODO rename to be parameterized
    new_file_name = "renamed_cty"
# TODO modularize
    web_driver_wait.until(
        EC.presence_of_element_located(
            (By.XPATH, '//button[@class="UywwFc-d UywwFc-d-Qu-dgl2Hf"]')
        ),
    )

    try:
        web_driver_wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    f'//div[@class="uXB7xe" and contains(@aria-label,"{file_name}" )]',
                )
            ),
        )
    except:
        assert False, "File Not Found"
    else:
        file_element = driver.find_element(
            By.XPATH, f'//div[@class="uXB7xe" and contains(@aria-label, "{file_name}")]'
        )
        action_chain.move_to_element(file_element).click()
        action_chain.perform()
        sleep(3)

        action_chain.reset_actions()
        for device in action_chain.w3c_actions.devices:
            device.clear_actions()

        sleep(1)
        action_chain.move_to_element(file_element).click()
        action_chain.send_keys("n")
        action_chain.perform()
        action_chain.reset_actions()
        for device in action_chain.w3c_actions.devices:
            device.clear_actions()

        sleep(3)

        action_chain.send_keys(new_file_name).perform()

        # Locate and click the OK button
        ok_button_locator = (
            By.XPATH,
            '//button[@name="ok" and contains(@class, "h-De-Vb h-De-Y")]',
        )
        ok_button = web_driver_wait.until(EC.element_to_be_clickable(ok_button_locator))
        ok_button = driver.find_element(
            By.XPATH, '//button[@name="ok" and contains(@class, "h-De-Vb h-De-Y")]'
        )
        ok_button.click()

        sleep(10)


"""
    Test function to retrieve filenames from the Google Drive web GUI.

    Parameters:
    - driver (WebDriver): The Selenium WebDriver instance.
    - action_chain (ActionChains): The Selenium ActionChains instance for performing user actions.
    - web_driver_wait (WebDriverWait): The Selenium WebDriverWait instance for waiting on elements.

    Returns:
    None

    Raises:
    AssertionError: If no filenames are found.

    Usage:
    test_get_filenames(driver, action_chain, web_driver_wait)
"""

def test_get_filenames(driver, action_chain, web_driver_wait):
    file_name_divs = driver.find_elements_by_css_selector("div.KL4NAf")

    sleep(4)
    assert len(file_name_divs) > 0


"""
Test function to remove a file from the Google Drive web GUI.

Parameters:
- driver (WebDriver): The Selenium WebDriver instance.
- action_chain (ActionChains): The Selenium ActionChains instance for performing user actions.
- web_driver_wait (WebDriverWait): The Selenium WebDriverWait instance for waiting on elements.

Returns:
None

Raises:
AssertionError: If the file is not found or cannot be deleted.

Usage:
test_remove_file(driver, action_chain, web_driver_wait)
"""


def test_remove_file(driver, action_chain, web_driver_wait):
    file_name = 'test.txt'
    utilities.remove_file(driver, action_chain, web_driver_wait,file_name)
    


"""
Test function to create a new folder in the Google Drive web GUI.

Parameters:
- driver (WebDriver): The Selenium WebDriver instance.
- action_chain (ActionChains): The Selenium ActionChains instance for performing user actions.
- web_driver_wait (WebDriverWait): The Selenium WebDriverWait instance for waiting on elements.

Returns:
None

Raises:
AssertionError: If the folder is not created successfully.

Usage:
test_create_folder(driver, action_chain, web_driver_wait)
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
Test function to logout from the Google Drive web GUI.

Parameters:
- driver (WebDriver): The Selenium WebDriver instance.
- action_chain (ActionChains): The Selenium ActionChains instance for performing user actions.
- web_driver_wait (WebDriverWait): The Selenium WebDriverWait instance for waiting on elements.

Returns:
None

Raises:
AssertionError: If logout fails or the login screen is not visible after logout.

Usage:
test_logout(driver, action_chain, web_driver_wait)
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
    
    
    
def test_download_file(driver,web_driver_wait,action_chain):
    # download's first file in drive
    web_driver_wait.until(EC.element_to_be_clickable(locators.file_selector))
    sleep(2)
    btn = driver.find_element(*locators.file_selector)
    btn.click()
    web_driver_wait.until(EC.element_to_be_clickable(locators.download_file_selector))
    sleep(2)
    btn = driver.find_element(*locators.download_file_selector)
    btn.click()
    sleep(3)


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

  
    file_element = driver.find_element(By.CSS_SELECTOR, f'div.uXB7xe[aria-label*="{file_name}"]')
    destination_folder_element = driver.find_element(By.XPATH, f'//div[contains(@aria-label, "{destination_folder_name}")]')

   
    action_chain = ActionChains(driver)
    action_chain.drag_and_drop(file_element, destination_folder_element).perform()

    
    sleep(5)

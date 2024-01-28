import configparser
from time import sleep

import pyautogui
import pytest
from selenium.webdriver import Chrome
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

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
    assert driver.title == "Home - Google Drive"


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
    # print(file_name_divs,len(file_name_divs))
    # for div in file_name_divs:
    #     print(div.text)
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
    file_name = "test.txt"
    # Click on Show more results to view all files
    web_driver_wait.until(
        EC.presence_of_element_located(
            (By.XPATH, '//button[@class="UywwFc-d UywwFc-d-Qu-dgl2Hf"]')
        ),
    )
    show_more_button = driver.find_element(
        By.XPATH, '//button[@class="UywwFc-d UywwFc-d-Qu-dgl2Hf"]'
    )
    show_more_button.click()
    sleep(3)
    # Find file
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
        # click on delete button
        web_driver_wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//div[@role='button' and @aria-label='Move to trash' and @aria-hidden='false' and @aria-disabled='false']",
                )
            ),
        )
        delete_button = driver.find_element(
            By.XPATH,
            "//div[@role='button' and @aria-label='Move to trash' and @aria-hidden='false' and @aria-disabled='false']",
        )
        delete_button.click()
        sleep(3)
        assert True


def test_rename_file(driver, action_chain, web_driver_wait):
    file_name = "test.txt"

    web_driver_wait.until(
        EC.presence_of_element_located(
            (By.XPATH, '//button[@class="UywwFc-d UywwFc-d-Qu-dgl2Hf"]')
        ),
    )
    show_more_button = driver.find_element(
        By.XPATH, '//button[@class="UywwFc-d UywwFc-d-Qu-dgl2Hf"]'
    )
    show_more_button.click()
    sleep(3)
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
        pyautogui.keyDown("ctrl")
        pyautogui.press("-")
        pyautogui.keyUp("ctrl")
        file_element = driver.find_element(
            By.XPATH, f'//div[@class="uXB7xe" and contains(@aria-label, "{file_name}")]'
        )
        action_chain.move_to_element(file_element).click()
        action_chain.perform()
        sleep(3)

        rename_button_locator = (
            By.XPATH,
            "//div[@role='button' and @aria-label='Rename' and @aria-expanded='false']",
        )

        web_driver_wait.until(EC.presence_of_element_located(rename_button_locator))
        # print(more_actions_button)
        rename_button = driver.find_element(
            rename_button_locator[0], rename_button_locator[1]
        )
        sleep(3)
        rename_button.click()
        sleep(3)



def test_create_folder(driver, action_chain, web_driver_wait):
    #wait until the New button is clickable
    new_btn = web_driver_wait.until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="drive_main_page"]/div/div[3]/div/button[1]/span[1]/span'))
    )
    new_btn.click()
    sleep(4)

    #wait for the list of options to appear
    new_folder_option = web_driver_wait.until(
        EC.element_to_be_clickable((By.XPATH,'//*[@id="drive_main_page"]/div/div[3]/div/button[1]'))
    )

    #move to the list and click on the New folder option
    action_chain.move_to_element(new_folder_option).click().perform()

    #Wait for the new folder dialog to appear
    # new_folder_dialog = web_driver_wait.until(
    #     EC.presence_of_element_located((By.CLASS_NAME,"FidVJb"))
    # )

    web_driver_wait.until(EC.presence_of_element_located((By.CLASS_NAME, "LUNIy")))

    #Find the input field and clear any existing text
    input_field = driver.find_element(By.CSS_SELECTOR, ".LUNIy")
    input_field.clear()
    # sleep(5)
   
    input_field.send_keys("Applied crypto")
    input_field.send_keys(Keys.ENTER)
    
    

    sleep(10)
    # #Wait for the folder element to appear in the list
    folder_element = web_driver_wait.until(EC.presence_of_element_located((By.XPATH, "//*[text()='Applied crypto']")))
    assert folder_element.is_displayed(), "Folder element is not visible"
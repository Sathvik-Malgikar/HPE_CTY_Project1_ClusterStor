import configparser
from time import sleep

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
    cfp.read()
    account_email_id = cfp.get("Account Credentials","email")
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

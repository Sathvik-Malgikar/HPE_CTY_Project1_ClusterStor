from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pytest
from time import sleep


@pytest.fixture
def driver():
    # svc = Service(executable_path="./chromedriver.exe")
    webdriver = Chrome(executable_path="./chromedriver.exe")
    yield webdriver
    webdriver.quit()


@pytest.fixture
def actionchain(driver):
    chain = ActionChains(driver)
    yield chain
    chain.reset_actions()


def test_signin(driver, actionchain):
    driver.get("https://www.google.com/intl/en-US/drive/")
    driver.maximize_window()
    sleep(0.8)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.LINK_TEXT, "Sign in")
        )
    )

    signin_ele = driver.find_element(By.LINK_TEXT, "Sign in")
    signin_ele.click()
    sleep(1.3)
    # opened by clicking sign-in anchor tag
    sign_in_tab = driver.window_handles[-1]
    driver.switch_to.window(sign_in_tab)
    sleep(1.3)

    print("Sending email")
    actionchain.send_keys(
        "beautifulselena4@gmail.com").send_keys(Keys.ENTER).perform()
    sleep(7)
    actionchain.reset_actions()  # does not seem to work
    actionchain.send_keys("SeleniumHPE$$").send_keys(Keys.ENTER).perform()
    sleep(15)
    assert driver.title == "Home - Google Drive"

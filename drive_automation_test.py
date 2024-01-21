from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pytest
from time import sleep

@pytest.fixture(scope="session")
def driver():
    # svc = Service(executable_path="./chromedriver.exe")
    webdriver = Chrome(executable_path="./chromedriver.exe")
    yield webdriver
    webdriver.quit()


@pytest.fixture
def action_chain(driver):
    chain = ActionChains(driver)
    yield chain
    chain.reset_actions()
    for device in chain.w3c_actions.devices:
        device.clear_actions()


@pytest.fixture
def web_driver_wait(driver):
    w_wait = WebDriverWait(driver,10)
    yield w_wait
    


def test_signin(driver,action_chain,web_driver_wait):
    driver.get("https://www.google.com/intl/en-US/drive/")
    driver.maximize_window()
    sleep(0.8)

    web_driver_wait.until(
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
    action_chain.send_keys(
        "beautifulselena4@gmail.com")
    action_chain.send_keys(Keys.ENTER)
    action_chain.perform()
    web_driver_wait.until(
        EC.presence_of_element_located(
            (By.XPATH,"//span[contains(text(), 'Welcome')]")), 
    )
    sleep(1.5)  # to deal with input animation
    action_chain.reset_actions()  
    for device in action_chain.w3c_actions.devices:
        device.clear_actions()
    
    action_chain.send_keys("SeleniumHPE$$")
    action_chain.send_keys(Keys.ENTER)
    action_chain.perform()
    sleep(5)
    assert driver.title == "Home - Google Drive"
    

def test_get_filenames(driver,action_chain,web_driver_wait):
    file_name_divs = driver.find_elements_by_css_selector("div.KL4NAf")
    # print(file_name_divs,len(file_name_divs))
    # for div in file_name_divs:
    #     print(div.text)
    sleep(4)
    assert len(file_name_divs)>0

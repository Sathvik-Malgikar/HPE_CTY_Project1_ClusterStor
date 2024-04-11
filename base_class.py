from time import sleep
from selenium.webdriver import Chrome
from selenium.webdriver.support.wait import WebDriverWait
from infrastructure.library_functions import HigherActions
from infrastructure import locators
import configparser
from infrastructure import autoGUIutils

from selenium.webdriver.common.keys import Keys
from win10toast import ToastNotifier

tn = ToastNotifier()

def toast_testcase_name(func):
    def wrapper(*args , **kwargs):
        tn.show_toast(f"Now running - {func.__name__[5:]}",f"Testcase being executed : {func.__name__[5:]}\n - ClusterStor Web Interface Test Automation",duration=10)
        return func(*args,**kwargs)
    return wrapper


class BaseTest:
    @classmethod
    def setup_class(cls):
        # global not_first_sign_in
        cls.driver = Chrome(executable_path="./tools/chromedriver.exe")
        cls.web_driver_wait = WebDriverWait(cls.driver, 10)
        
        cls.driver.get("https://www.google.com/intl/en-US/drive/")
        cls.driver.maximize_window()
        sleep(3)
        cls.higher_actions =  HigherActions(cls.driver, cls.web_driver_wait)
        signin_ele = cls.higher_actions.wait_to_click(locators.sign_in_link)
        signin_ele.click()
    # Switch to the sign-in window explicitly based on URL or title
        for window_handle in cls.driver.window_handles:
            cls.driver.switch_to.window(window_handle)
            if "accounts.google.com" in cls.driver.current_url or "Sign in" in cls.driver.title:
                break
        parser = configparser.ConfigParser()
        parser.read("infrastructure/config.ini")
        account_email_id = parser.get("Account Credentials", "alt_email")
        account_pwd = parser.get("Account Credentials", "alt_password")
     
        cls.higher_actions.send_keys_to_focused(account_email_id)
        cls.higher_actions.send_keys_to_focused(Keys.ENTER)
        cls.higher_actions.wait_for_element(locators.welcome_span)
        # deal with input animation 
        sleep(3)
        # not_first_sign_in = True
        cls.higher_actions.send_keys_to_focused(account_pwd)
        cls.higher_actions.send_keys_to_focused(Keys.ENTER)
        #cls.web_driver_wait.until(EC.title_is("Home - Google Drive"))

    @classmethod
    def teardown_class(cls):
         # TEARDOWN START ###
        user_profile_button_element = cls.higher_actions.wait_for_element(locators.user_profile_button_locator)
        cls.higher_actions.click_element(user_profile_button_element)
        autoGUIutils.n_tabs_shift_focus(5)
        autoGUIutils.press_enter()
        cls.driver.close()
        before_signin = cls.driver.window_handles[-1]
        cls.driver.switch_to.window(before_signin)
        cls.driver.quit()
        # TEARDOWN END ###
    
    
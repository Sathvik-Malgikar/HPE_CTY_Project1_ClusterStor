from time import sleep
from selenium.webdriver import Chrome,ChromeOptions
from selenium.webdriver.support.wait import WebDriverWait
from infrastructure.library_functions import HigherActions
from infrastructure import locators
import configparser
from infrastructure import autoGUIutils

from selenium.webdriver.common.keys import Keys
from win10toast import ToastNotifier

tn = ToastNotifier()

def plain_toast(title,msg):
    tn.show_toast(title,msg,duration=10)

def toast_testcase_name(func):
    def wrapper(*args , **kwargs):
        tn.show_toast(f"Now running - {func.__name__[5:]}",f"Testcase being executed : {func.__name__[5:]}\n - ClusterStor Web Interface Test Automation",duration=10)
        return func(*args,**kwargs)
    return wrapper


class Base:
    @classmethod
    def setup_class(cls):
        # global not_first_sign_in
        
        # Create an instance of the ChromeOptions class
        options = ChromeOptions()

        # Add the chrome switch to disable notifications
        options.add_argument("--disable-notifications")
        
        cls.driver = Chrome(options=options)
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
        account_email_id = parser.get("Account Credentials", "email")
        account_pwd = parser.get("Account Credentials", "password")
     
        cls.higher_actions.send_keys_to_focused(account_email_id)
        cls.higher_actions.send_keys_to_focused(Keys.ENTER)
        cls.higher_actions.wait_for_element(locators.welcome_span)
        # deal with input animation 
        sleep(3)
        # not_first_sign_in = True
        cls.higher_actions.send_keys_to_focused(account_pwd)
        cls.higher_actions.send_keys_to_focused(Keys.ENTER)
        #cls.web_driver_wait.until(EC.title_is("Home - Google Drive"))
        
        # AT HOME PAGE ,LOGGED IN , CLEANING RESIDUAL FILES
        cls.higher_actions.navigate_to("My Drive")
        autoGUIutils.select_all() 
        autoGUIutils.press_delete()
        
        # cls.higher_actions.click_on_folders_button()
        # autoGUIutils.select_all() 
        # autoGUIutils.press_delete()
        
        cls.higher_actions.navigate_to("Trash")
        button_found = cls.higher_actions.wait_to_click(locators.empty_trash_button)
        if button_found:
            button_found.click()
            autoGUIutils.n_tabs_shift_focus(3)
            autoGUIutils.press_enter()
        
        cls.higher_actions.navigate_to("Home")

    @classmethod
    def teardown_class(cls):
        # TEARDOWN START ###
         
        cls.higher_actions.navigate_to("My Drive")
        autoGUIutils.select_all() 
        autoGUIutils.press_delete()
        
        # cls.higher_actions.click_on_folders_button()
        # autoGUIutils.select_all() 
        # autoGUIutils.press_delete()
        
        cls.higher_actions.navigate_to("Trash")
        button_found = cls.higher_actions.wait_to_click(locators.empty_trash_button)
        if button_found:
            button_found.click()
            autoGUIutils.n_tabs_shift_focus(3)
            autoGUIutils.press_enter()
        
        
        user_profile_button_element = cls.higher_actions.wait_for_element(locators.user_profile_button_locator)
        cls.higher_actions.click_element(user_profile_button_element)
        autoGUIutils.n_tabs_shift_focus(5)
        autoGUIutils.press_enter()
        cls.driver.close()
        before_signin = cls.driver.window_handles[-1]
        cls.driver.switch_to.window(before_signin)
        cls.driver.quit()
        # TEARDOWN END ###
    
    
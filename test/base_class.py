from time import sleep
from selenium.webdriver import Chrome, ChromeOptions, Firefox, FirefoxOptions
from selenium.webdriver.support.wait import WebDriverWait
from infrastructure.library_functions import HigherActions
from infrastructure import locators
import configparser
from infrastructure import autoGUIutils
import os
import files
import inspect
from selenium.webdriver.common.keys import Keys
from win10toast import ToastNotifier

tn = ToastNotifier()
chosen_driver = "Chrome"  # "Chrome" or "Firefox"

def get_num_selected_testcases():
    with open("test/selected_test_cases.txt", "r") as f:
        return len(f.read().split("\n"))


def is_selected(testcase_name):
    with open("test/selected_test_cases.txt", "r") as f:
        sel_list = f.read().split("\n")
    return testcase_name in sel_list

def get_number_of_testcases(test_class):
    return len(inspect.getmembers(test_class, inspect.isfunction))


def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"{file_path} deleted successfully.")
    else:
        print(f"{file_path} does not exist.")


def plain_toast(title, msg):
    """
    Display a plain toast notification.


    Args:
        title (str): The title of the toast notification.
        msg (str): The message of the toast notification.

    Returns:
        None
    """
    tn.show_toast(title, msg, duration=10)


def toast_testcase_name(func):
    """
    A decorator function that displays a toast notification with
    the name of the test case being executed.

    Args:
        func: The function being decorated.

    Returns:
        The decorated function.

    """

    def wrapper(*args, **kwargs):
        tn.show_toast(
            f"Now running - {func.__name__[5:]}",
            f"Testcase being executed : {func.__name__[5:]}\n - ClusterStor Web Interface Test Automation",
            duration=10,
        )
        return func(*args, **kwargs)

    return wrapper


class Base:
    """
    This is the base class for all the test case classes.
    It provides basic login and logout for selected driver.
    Supported drivers are Chrome and Firefox.
    These can be selected by changing the driver variable
    in pytest.ini file.
    """

    @classmethod
    def setup_class(cls):
        """
        Set up the test class by initializing the web driver,
        navigating to the Google Drive sign-in page,
        and performing necessary actions to log in and clean
        up residual files.

        Args:
            cls: The class object.

        Returns:
            None
        """
        path1 = os.path.join(
            os.path.expanduser("~"), "Downloads", files.FILE_TO_UPLOAD
            )
        dwnld_dir = os.path.join(os.path.expanduser("~"), "Downloads")
        path2 = os.path.join(
            dwnld_dir, files.file_name_for_download
        )
        print("Clearing previous test-downloads.")
        delete_file(path1)
        delete_file(path2)
        # Create an instance of the DriverOptions class
        if chosen_driver == "Firefox":
            options = FirefoxOptions()
        else:
            options = ChromeOptions()

        # Add the chrome switch to disable notifications
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-animations")
        options.add_argument("--disable-infobars")
                # Add preferences
        prefs = {
            "profile.default_content_setting_values.notifications": 2,  # Disable notifications
            "profile.default_content_setting_values.popups": 2,          # Disable popups
            "profile.default_content_setting_values.animations": 2,      # Disable animations
            # Add more preferences as needed
        }

        # Add preferences to Chrome options
        options.add_experimental_option("prefs", prefs)

        if chosen_driver == "Firefox":
            cls.driver = Firefox("tools/geckodriver.exe", options=options)
        else:
            cls.driver = Chrome("tools/chromedriver.exe", options=options)

        cls.web_driver_wait = WebDriverWait(cls.driver, 10)
        cls.driver.get("https://www.google.com/intl/en-US/drive/")
        cls.driver.maximize_window()
        sleep(3)
        cls.higher_actions = HigherActions(cls.driver, cls.web_driver_wait)
        signin_ele = cls.higher_actions.wait_to_click(locators.sign_in_link)
        signin_ele.click()

        # Switch to the sign-in window explicitly based on URL or title
        for window_handle in cls.driver.window_handles:
            cls.driver.switch_to.window(window_handle)
            if (
                "accounts.google.com" in cls.driver.current_url
                or "Sign in" in cls.driver.title
            ):
                break

        parser = configparser.ConfigParser()
        parser.read("infrastructure/config.ini")
        cls.higher_actions.wait_for_element(locators.span_with_text("Sign"))
        sleep(2)
        account_email_id = parser.get("Account Credentials", "email")
        account_pwd = parser.get("Account Credentials", "password")

        cls.higher_actions.send_keys_to_focused(account_email_id)
        cls.higher_actions.send_keys_to_focused(Keys.ENTER)
        # deal with input animation
        cls.higher_actions.wait_for_element(locators.span_with_text("Welcome"))
        sleep(2.5)
        # not_first_sign_in = True
        cls.higher_actions.send_keys_to_focused(account_pwd)
        cls.higher_actions.send_keys_to_focused(Keys.ENTER)
        # cls.web_driver_wait.until(EC.title_is("Home - Google Drive"))

        # AT HOME PAGE ,LOGGED IN , CLEANING RESIDUAL FILES
        cls.higher_actions.navigate_to("My Drive")
        sleep(1.5)
        autoGUIutils.select_all()
        autoGUIutils.press_delete()

        # cls.higher_actions.click_on_folders_button()
        # autoGUIutils.select_all()
        # autoGUIutils.press_delete()

        cls.higher_actions.navigate_to("Trash")
        button_found = cls.higher_actions.wait_to_click(locators.empty_trash_btn)
        if button_found:
            button_found.click()
            autoGUIutils.n_tabs_shift_focus(3)
            autoGUIutils.press_enter()

        cls.higher_actions.navigate_to("Home")
        plain_toast("Login successful.", "Waiting for prerequisites to finish.")

    @classmethod
    def teardown_class(cls):
        """
        This method is called after all test cases in the
        class have been executed.
        It performs the necessary cleanup actions such as
        logging out, deleting files, and closing the driver.

        Args:
            cls: The class object representing the test class.

        Returns:
            None
        """
        plain_toast("Logging out ...", "Finished executing all testcases.")
        # TEARDOWN START ###
        cls.higher_actions.navigate_to("My Drive")
        autoGUIutils.select_all()
        autoGUIutils.press_delete()

        # cls.higher_actions.click_on_folders_button()
        # autoGUIutils.select_all()
        # autoGUIutils.press_delete()

        cls.higher_actions.navigate_to("Trash")
        button_found = cls.higher_actions.wait_to_click(locators.empty_trash_btn)
        if button_found:
            button_found.click()
            autoGUIutils.n_tabs_shift_focus(3)
            autoGUIutils.press_enter()

        user_profile_button_element = cls.higher_actions.wait_for_element(
            locators.user_profile_button_locator
        )
        cls.higher_actions.click_element(user_profile_button_element)
        sleep(2)
        autoGUIutils.n_tabs_shift_focus(5)
        autoGUIutils.press_enter()
        cls.driver.close()
        before_signin = cls.driver.window_handles[-1]
        cls.driver.switch_to.window(before_signin)
        cls.driver.quit()
        # TEARDOWN END ###

"""
## Utility function to select a file in Google Drive GUI
def select_file(driver, action_chain, web_driver_wait,file_name)

Parameters:
- driver (WebDriver): The Selenium WebDriver instance.
- action_chain (ActionChains): The Selenium ActionChains instance for performing user actions.
- web_driver_wait (WebDriverWait): The Selenium WebDriverWait instance for waiting on elements.
- file_name: Name of file/folder to be selected

Returns:
None

Raises:
FileNotFoundError: If the file/folder does not exist on Google Drive.

Usage:
select_file(driver, action_chain, web_driver_wait, file_name)

Additional :
- show_more_needed is to ensure backwards compatibility
- old testcases do not have show_more param, so by default True
- newer testcases can explicitly mention if show more button is to be clicked or not before looking for file
"""

"""
## Utility function to select a folder in Google Drive GUI
def select_folder(driver, action_chain, web_driver_wait,folder_name)

Parameters:
- driver (WebDriver): The Selenium WebDriver instance.
- action_chain (ActionChains): The Selenium ActionChains instance for performing user actions.
- web_driver_wait (WebDriverWait): The Selenium WebDriverWait instance for waiting on elements.
- folder_name: Name of file/folder to be selected

Returns:
None

Raises:
FileNotFoundError: If the folder does not exist on Google Drive.

Usage:
select_folder(driver, action_chain, web_driver_wait, folder)
"""

"""
## Utility function to click delete button on a selected file/folder in the Google Drive web GUI.
def delete_file(driver,action_chain,web_driver_wait)

Parameters:
- driver (WebDriver): The Selenium WebDriver instance.
- action_chain (ActionChains): The Selenium ActionChains instance for performing user actions.
- web_driver_wait (WebDriverWait): The Selenium WebDriverWait instance for waiting on elements.

Returns:
None

Raises:
-

Usage:
delete_file(driver, action_chain, web_driver_wait)
"""


"""
## Utility function to perform delete action on the file/folder in the Google Drive web GUI.

def remove_file(driver, action_chain, web_driver_wait,file_name)

Parameters:
- driver (WebDriver): The Selenium WebDriver instance.
- action_chain (ActionChains): The Selenium ActionChains instance for performing user actions.
- web_driver_wait (WebDriverWait): The Selenium WebDriverWait instance for waiting on elements.
- file_name: Name of file/folder to be deleted.

Returns:
None

Raises:
-

Usage:
remove_file(driver, action_chain, web_driver_wait,file_name)
"""


"""
## Utility function to rename a folder in Google Drive GUI.

Parameters:
- driver (WebDriver): The Selenium WebDriver instance.
- action_chain (ActionChains): The Selenium ActionChains instance for performing user actions.
- web_driver_wait (WebDriverWait): The Selenium WebDriverWait instance for waiting on elements.
- old_folder_name (str): The current name of the folder to be renamed.
- new_folder_name (str): The desired new name for the folder.

Returns:
None

Raises:
FileNotFoundError: If the folder with the old name does not exist on Google Drive.

Usage:
rename_folder(driver, action_chain, web_driver_wait, old_folder_name, new_folder_name)
"""


"""
## Utility function to rename a file in Google Drive GUI.

Parameters:
- driver (WebDriver): The Selenium WebDriver instance.
- action_chain (ActionChains): The Selenium ActionChains instance for performing user actions.
- web_driver_wait (WebDriverWait): The Selenium WebDriverWait instance for waiting on elements.
- old_file_name (str): The current name of the file to be renamed.
- new_file_name (str): The desired new name for the file.

Returns:
None

Raises:
FileNotFoundError: If the file with the old name does not exist on Google Drive.

Usage:
rename_file(driver, action_chain, web_driver_wait, old_file_name, new_file_name)
"""


"""
## Utility function to undo the delete action on a file in the Google Drive web GUI.

Parameters:
- driver (WebDriver): The Selenium WebDriver instance.
- action_chain (ActionChains): The Selenium ActionChains instance for performing user actions.
- web_driver_wait (WebDriverWait): The Selenium WebDriverWait instance for waiting on elements.
- file_to_be_retrieved (str): The name of the file to be restored from the trash.

Returns:
None

Raises:
FileNotFoundError: If the file with the given name is not found in the trash.

Usage:
undo_delete_action(driver, action_chain, web_driver_wait, file_to_be_retrieved)
"""



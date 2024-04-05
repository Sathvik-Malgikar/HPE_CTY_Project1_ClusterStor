from time import sleep
import locators
import files
import autoGUIutils

from base_class import BaseTest

class TestfolderActions(BaseTest):

    """
    Test function to rename a folder in the Google Drive web GUI.
    """
    @classmethod
    def setup_class(cls):
        super(cls, TestfolderActions).setup_class()#FIRST SUPER CLASS
        #THEN SUBCLASS SETUP
        folders_to_create = [files.folder_name, files.folder_name_to_be_removed]
        
        for folder_name in folders_to_create:
            cls.higher_actions.click_on_new_button()
            action_button = cls.higher_actions.wait_to_click(locators.new_menu_button_locator("New folder"))
            action_button.click()
            sleep(2)
            autoGUIutils.type_into_dialogue_box(folder_name)
            cls.driver.refresh()
            sleep(4)

       
    
    @classmethod
    def teardown_class(cls):
        #FIRST SUBCLASS TEARDOWN LOGIC
        folders_to_clean = [files.renamed_folder_name , files.create_folder_name]
        for foldername in folders_to_clean:
            cls.higher_actions.remove_file_action(foldername) # remove_file_action works for both file and folder
        
        super(cls, TestfolderActions).teardown_class()#THEN SUPERCLASS TEARDOWN

    def test_rename_folder(self):
        old_folder_name = files.folder_name
        new_folder_name = files.renamed_folder_name
        result = self.higher_actions.rename_folder_action(old_folder_name, new_folder_name)
        assert result, "Rename failed"

    """
    ## Test function to create a new folder in the Google Drive web GUI.
    """

    def test_create_folder(self):
        folder_name = files.create_folder_name
        self.higher_actions.create_folder_action(folder_name)
        assert self.higher_actions.wait_for_element(locators.file_selector(folder_name)) is not None
        sleep(3)

    """
    ## Test function to upload new file in the Google Drive web GUI.
    """

    def test_remove_folder(self):
        folder_to_be_removed = files.folder_name_to_be_removed
        self.higher_actions.remove_folder_action(folder_to_be_removed)
        assert not self.higher_actions.wait_for_element(locators.file_selector(folder_to_be_removed))
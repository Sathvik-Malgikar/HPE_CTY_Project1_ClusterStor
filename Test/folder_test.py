import sys
import inspect
from infrastructure import locators
import files
from infrastructure import autoGUIutils
from base_class import Base, toast_testcase_name, plain_toast
sys.path.append(r'C:\HPE_CTY_Project1_ClusterStor')


class TestfolderActions(Base):

    """
    Test function to rename a folder in the Google Drive web GUI.
    """
    @classmethod
    def setup_class(cls):
        super(cls, TestfolderActions).setup_class()  # FIRST SUPER CLASS
        plain_toast("Executing suite : " + cls.__name__, f"Contains {len(inspect.getmembers(TestfolderActions,inspect.isfunction))} testcases")
        # THEN SUBCLASS SETUP
        folders_to_create = [files.renamed_folder_name, files.destination_folder_name, files.create_folder_name, files.folder_to_be_moved, files.folder_name, files.folder_name_to_be_removed]
        for folder_name in folders_to_create:
            cls.higher_actions.click_on_new_button()
            action_button = cls.higher_actions.wait_to_click(locators.new_menu_button_locator("New folder"))
            action_button.click()
            autoGUIutils.type_into_dialogue_box(folder_name)
            cls.higher_actions.refresh_and_wait_to_settle()

    @classmethod
    def teardown_class(cls):
        # FIRST SUBCLASS TEARDOWN LOGIC
        # folders_to_clean = [files.renamed_folder_name , files.destination_folder_name,files.create_folder_name]
        # for foldername in folders_to_clean:
        #     cls.higher_actions.remove_file_action(foldername) # remove_file_action works for both file and folder
        super(cls, TestfolderActions).teardown_class()  # THEN SUPERCLASS TEARDOWN

    @toast_testcase_name
    def test_rename_folder(self):
        old_folder_name = files.folder_name
        new_folder_name = files.renamed_folder_name
        result = self.higher_actions.rename_folder_action(old_folder_name, new_folder_name)
        assert result, "Rename failed"

    """
    ## Test function to create a new folder in the Google Drive web GUI.
    """

    @toast_testcase_name
    def test_create_folder(self):
        folder_name = files.create_folder_name
        self.higher_actions.create_folder_action(folder_name)
        assert self.higher_actions.wait_for_element(locators.file_selector(folder_name)) is not None

    """
    ## Test function to upload new file in the Google Drive web GUI.
    """

    @toast_testcase_name
    def test_remove_folder(self):
        folder_to_be_removed = files.folder_name_to_be_removed
        self.higher_actions.remove_folder_action(folder_to_be_removed)
        assert not self.higher_actions.wait_for_element(locators.file_selector(folder_to_be_removed))

    @toast_testcase_name
    def test_move_folder(self):
        foldername = files.folder_to_be_moved
        destination_folder = files.destination_folder_name
        # self.higher_actions.navigate_to("Home")
        # self.higher_actions.click_on_folders_button()
        self.higher_actions.move_action(foldername, destination_folder)
        self.higher_actions.verify_file_in_destination(foldername, destination_folder)
        self.higher_actions.navigate_to("My Drive")
        self.driver.refresh()
        assert not self.higher_actions.wait_for_element(locators.file_selector(foldername))

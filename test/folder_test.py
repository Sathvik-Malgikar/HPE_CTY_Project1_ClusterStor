from test.base_class import Base, get_number_of_testcases
from test.base_class import toast_testcase_name, plain_toast

from infrastructure import locators
import files


class TestfolderActions(Base):
    @classmethod
    def setup_class(cls):
        super(cls, TestfolderActions).setup_class()  # FIRST SUPER CLASS
        # THEN SUBCLASS SETUP
        folders_to_create = [
            files.destination_folder_name,
            files.folder_to_be_moved,
            files.folder_name,
            files.folder_name_to_be_removed,
        ]
        for folder_name in folders_to_create:
            cls.higher_actions.create_folder_action(folder_name)

        n_testcases = get_number_of_testcases(TestfolderActions)
        plain_toast(
            f"Prerequisites for suite {cls.__name__} ready.",
            f"Contains {n_testcases} testcases, starting now.",
        )

    @classmethod
    def teardown_class(cls):
        # FIRST SUBCLASS TEARDOWN LOGIC
        super(cls, TestfolderActions).teardown_class()

    @toast_testcase_name
    def test_rename_folder(self):
        old_folder_name = files.folder_name
        new_folder_name = files.renamed_folder_name
        result = self.higher_actions.rename_folder_action(
            old_folder_name, new_folder_name)
        assert result, "Rename failed"

    @toast_testcase_name
    def test_create_folder(self):
        folder_name = files.create_folder_name
        self.higher_actions.create_folder_action(folder_name)
        temp_loc = locators.file_selector(folder_name)
        assert (
            self.higher_actions.wait_for_element(temp_loc)
            is not None
        )

    @toast_testcase_name
    def test_remove_folder(self):
        folder_to_be_removed = files.folder_name_to_be_removed
        self.higher_actions.remove_folder_action(folder_to_be_removed)
        assert not self.higher_actions.wait_for_element(
            locators.file_selector(folder_to_be_removed)
        )

    @toast_testcase_name
    def test_move_folder(self):
        foldername = files.folder_to_be_moved
        dst_folder = files.destination_folder_name
        # self.higher_actions.navigate_to("Home")
        # self.higher_actions.click_on_folders_button()
        self.higher_actions.move_action(foldername, dst_folder)
        self.higher_actions.verify_file_in_destination(foldername, dst_folder)
        self.higher_actions.navigate_to("My Drive")
        assert not self.higher_actions.wait_for_element(
            locators.file_selector(foldername)
        )

from test.base_class import Base, toast_testcase_name, plain_toast

import pytest

from infrastructure import locators
import files
from infrastructure import autoGUIutils
import hashlib
import os
import inspect


class TestfileActions(Base):
    @classmethod
    def setup_class(cls):
        super(cls, TestfileActions).setup_class()  # FIRST SUPER CLASS
        # THEN SUBCLASS SETUP
        prereqs = [
            files.undo_file_move,
            *list(map(lambda a:a[0], files.file_destination_pairs)),
            files.file_move_name,
            files.file_name,
            files.file_name_for_copy,
            files.file_name_for_download,
            files.file_to_be_deleted,
            *files.remove_multiple_files,
            files.delete_forever_file_name,
            files.undo_rename,
        ]
        file_list_to_upload = " ".join(list(map(lambda a: f'"{a}"', prereqs)))
        cls.higher_actions.click_on_new_button()
        upload_button = cls.higher_actions.wait_to_click(
            locators.new_menu_button_locator("File upload")
        )
        upload_button.click()
        autoGUIutils.type_into_dialogue_box(file_list_to_upload)
        cls.higher_actions.deal_duplicate_and_await_upload()
        folders_to_create = list(set([
            files.destination_folder_name,
            *list(map(lambda a:a[1], files.file_destination_pairs)),
            files.undo_move_destination_folder,
        ]))
        
        for folder_name in folders_to_create:
            cls.higher_actions.create_folder_action(folder_name)

        plain_toast(
            f"Prerequisites for suite {cls.__name__} ready.",
            f"Contains {len(inspect.getmembers(TestfileActions,inspect.isfunction))} testcases, starting now.",
        )

    @classmethod
    def teardown_class(cls):
        # FIRST SUBCLASS TEARDOWN LOGIC
        super(cls, TestfileActions).teardown_class()  # THEN SUPERCLASS TEARDOWN

    @pytest.mark.GROUPA
    @toast_testcase_name
    def test_rename_file(self):
        old_file_name = files.file_name
        new_file_name = files.renamed_file_name
        self.higher_actions.rename_action(old_file_name, new_file_name)
        result = self.higher_actions.rename_verification(old_file_name, new_file_name)
        assert result, "Rename failed"

    @pytest.mark.GROUPA
    @toast_testcase_name
    def test_undo_rename_file(self):
        old_file_name = files.undo_rename
        new_file_name = files.renamed_undo_rename
        self.higher_actions.undo_rename_action(old_file_name, new_file_name)
        self.higher_actions.undo_rename_verification(old_file_name, new_file_name)

    @pytest.mark.GROUPA
    @toast_testcase_name
    def test_get_filenames(self):
        no_of_files = self.higher_actions.get_file_names_action()
        assert no_of_files > 0

    @pytest.mark.GROUPA
    @toast_testcase_name
    def test_upload_file(self):  # this file is present in User folder
        self.higher_actions.upload_file_action(files.FILE_TO_UPLOAD)
        self.higher_actions.wait_for_element(
            locators.file_selector(files.FILE_TO_UPLOAD)
        )
        ground_truth_hash = None
        with open(
            os.path.join("C:\\Users", os.getlogin(), files.FILE_TO_UPLOAD), "rb"
        ) as ground_truth_file:

            ground_truth_hash = hashlib.file_digest(
                ground_truth_file, "md5"
            ).hexdigest()
        self.higher_actions.select_item(files.FILE_TO_UPLOAD)
        download_button = self.higher_actions.wait_for_element(
            locators.action_bar_button_selector("Download")
        )
        download_button.click()
        downloaded_file_path = os.path.join(
            "C:\\Users", os.getlogin(), "Downloads", files.FILE_TO_UPLOAD
        )
        if autoGUIutils.wait_for_file(
            downloaded_file_path, timeout=16
        ):  # this will skip hash checking if file not downloaded before timeout
            downloaded_file_hash = None
            with open(downloaded_file_path, "rb") as downloaded_file:
                downloaded_file_hash = hashlib.file_digest(
                    downloaded_file, "md5"
                ).hexdigest()
            assert downloaded_file_hash == ground_truth_hash, "Checksum mismatch"
        else:
            assert False

    @pytest.mark.GROUPA
    @toast_testcase_name
    def test_download_file(self):
        self.higher_actions.select_item(files.file_name_for_download)
        download_button = self.higher_actions.wait_for_element(
            locators.action_bar_button_selector("Download")
        )
        download_button.click()
        file_download_directory = os.path.join("C:\\Users", os.getlogin(), "Downloads")
        autoGUIutils.wait_for_file(
            os.path.join(file_download_directory, files.file_name_for_download), timeout=18
        )

        assert files.file_name_for_download in os.listdir(file_download_directory)

    @pytest.mark.GROUPA
    @toast_testcase_name
    def test_copy_file(self):
        copied_file_element = self.higher_actions.copy_file_action(
            files.file_name_for_copy
        )
        self.higher_actions.verify_copy_file_action(
            copied_file_element, files.file_name_for_copy
        )

    @pytest.mark.GROUPA
    @toast_testcase_name
    def test_search_for_file_by_name(self):
        self.higher_actions.search_by_name_action(files.file_to_be_searched)

    @pytest.mark.GROUPA
    @toast_testcase_name
    def test_search_for_file_by_type(self):
        no_of_files = self.higher_actions.search_by_type_action()
        assert no_of_files > 0

    @pytest.mark.GROUPB
    @toast_testcase_name
    def test_move_file(self):
        filename = files.file_move_name
        destination_folder = files.destination_folder_name
        self.higher_actions.navigate_to("My Drive")
        self.higher_actions.move_action(filename, destination_folder)
        self.higher_actions.verify_file_in_destination(filename, destination_folder)
        autoGUIutils.go_back_esc()

    @pytest.mark.GROUPB
    @toast_testcase_name
    def test_undo_move_file(self):
        filename = files.undo_file_move
        folder = files.undo_move_destination_folder
        self.higher_actions.navigate_to("My Drive")
        self.higher_actions.undo_move_action(filename, folder)
        self.higher_actions.verify_undo_move_action(filename, folder)

    @pytest.mark.GROUPB
    @toast_testcase_name
    def test_move_multiple_files(self):
        self.higher_actions.navigate_to("My Drive")
        
        for filename, destination_folder in (files.file_destination_pairs):
            try:
                self.higher_actions.move_action(
                    filename, destination_folder
                )
                self.higher_actions.verify_file_in_destination(
                    filename, destination_folder
                )
                self.higher_actions.navigate_to("My Drive")
                assert not self.higher_actions.wait_for_element(
                    locators.file_selector(filename)
                )
            except Exception as e:
                print(
                    f"Move failed for '{filename}' with error : {e}"
                )
                # Continue to next move even if current move fails
                assert False

    @pytest.mark.GROUPB
    @toast_testcase_name
    def test_remove_file(self):
        file_name = files.file_to_be_deleted
        self.higher_actions.remove_file_action(file_name)

    @pytest.mark.GROUPB
    @toast_testcase_name
    def test_remove_multiple_files(self):
        self.higher_actions.navigate_to("Home")
        for file in files.remove_multiple_files:
            try:
                self.higher_actions.remove_file_action(file)
            except FileNotFoundError as e:
                assert False, repr(e)

    @pytest.mark.GROUPB
    @toast_testcase_name
    def test_delete_file_permanently(self):
        result = self.higher_actions.delete_permanently_action(
            files.delete_forever_file_name
        )
        assert result

    @pytest.mark.GROUPB
    @toast_testcase_name
    def test_undo_delete_action(self):
        file_name_to_retrieve = files.file_to_be_restored
        self.higher_actions.undo_delete_action(file_name_to_retrieve)

    @pytest.mark.GROUPB
    @toast_testcase_name
    def test_capacity_after_upload(self):
        self.higher_actions.navigate_to("My Drive")
        file_name_to_upload = files.capacity_file
        initial_storage = self.higher_actions.get_storage_used()
        self.higher_actions.upload_file_action(file_name_to_upload)
        final_storage = self.higher_actions.get_storage_used()
        storage_units = {"KB": 1024, "MB": 1024**2, "GB": 1024**3}
        capacity, unit = (
            float(files.capacity_file_size.split(" ")[0]),
            files.capacity_file_size.split(" ")[1],
        )
        assert final_storage - initial_storage == capacity * storage_units.get(unit, 1)

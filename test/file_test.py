from test.base_class import Base, get_num_selected_testcases
from test.base_class import toast_testcase_name, plain_toast
from test.base_class import is_selected

import pytest

from infrastructure import locators
import files
from infrastructure import autoGUIutils
import hashlib
import os

prereq_mapping_files = {
    "test_remove_multiple_files": files.remove_multiple_files,
    "test_upload_file": files.FILE_TO_UPLOAD,
    "test_move_file": files.file_move_name,
    "test_rename_file": files.file_name,
    "test_undo_rename_file": files.undo_rename,
    "test_search_for_files_by_types": files.filelist_search_by_type,
    "test_copy_file": files.file_name_for_copy,
    "test_undo_move_file": files.undo_file_move,
    "test_search_for_file_by_name": files.file_to_be_searched,
    "test_download_file": files.file_name_for_download,
    "test_capacity_after_upload": files.capacity_file,
    "test_move_multiple_files": files.move_multiple_fnames,
    "test_remove_file": files.file_to_be_deleted,
    "test_delete_file_permanently": files.delete_forever_file_name,
    "test_undo_delete_action": files.file_to_be_restored
}
prereq_mapping_folders = {
    "test_move_file": files.destination_folder_name,
    "test_undo_move_file": files.undo_move_destination_folder,
    "test_move_multiple_files": files.move_multiple_destinations
}


class TestfileActions(Base):
    @classmethod
    def setup_class(cls):
        super(cls, TestfileActions).setup_class()  # FIRST SUPER CLASS
        # THEN SUBCLASS SETUP
        prereqs = []
        for key in prereq_mapping_files:
            if is_selected(key):
                val = prereq_mapping_files[key]
                if type(val) == list:
                    prereqs.extend(val)
                else:
                    prereqs.append(val)
        print(prereqs, "Being uploaded as prerequisites.")
        file_list_to_upload = " ".join(list(map(lambda a: f'"{a}"', prereqs)))
        cls.higher_actions.click_on_new_button()
        upload_button = cls.higher_actions.wait_to_click(
            locators.new_menu_button_locator("File upload")
        )
        upload_button.click()
        autoGUIutils.type_into_dialogue_box(file_list_to_upload)
        cls.higher_actions.deal_duplicate_and_await_upload()
        cls.higher_actions.navigate_to("My Drive")
        cls.higher_actions.select_item(prereqs[0])
        autoGUIutils.cut_selection()
        autoGUIutils.paste_clipboard()
        autoGUIutils.n_tabs_shift_focus(2)
        autoGUIutils.press_space()

        folders_to_create = []
        for key in prereq_mapping_folders:
            if is_selected(key):
                val = prereq_mapping_folders[key]
                if type(val) == list:
                    folders_to_create.extend(val)
                else:
                    folders_to_create.append(val)
        folders_to_create = list(set(folders_to_create))
        print(folders_to_create, "Folders being created as prerequisites.")

        for folder_name in folders_to_create:
            cls.higher_actions.create_folder_action(folder_name)

        n_testcases = get_num_selected_testcases()
        plain_toast(
            f"Prerequisites for suite {cls.__name__} ready.",
            f"Contains {n_testcases} testcases, starting now.",
        )

    @classmethod
    def teardown_class(cls):
        # FIRST SUBCLASS TEARDOWN LOGIC
        super(cls, TestfileActions).teardown_class()

    @pytest.mark.GROUPA
    @toast_testcase_name
    def test_rename_file(self):
        old_fname = files.file_name
        new_fname = files.renamed_file_name
        self.higher_actions.rename_action(old_fname, new_fname)
        result = self.higher_actions.rename_verification(old_fname, new_fname)
        assert result, "Rename failed"

    @pytest.mark.GROUPA
    @toast_testcase_name
    def test_undo_rename_file(self):
        old_fname = files.undo_rename
        new_fname = files.renamed_undo_rename
        self.higher_actions.undo_rename_action(old_fname, new_fname)
        self.higher_actions.undo_rename_verification(old_fname, new_fname)

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
        user_dir = os.path.expanduser("~")
        with open(
            os.path.join(user_dir, files.FILE_TO_UPLOAD), "rb"
        ) as ground_truth_file:

            ground_truth_hash = hashlib.md5(
                ground_truth_file.read()
            ).hexdigest()
        self.higher_actions.select_item(files.FILE_TO_UPLOAD)
        download_button = self.higher_actions.wait_for_element(
            locators.action_bar_button_selector("Download")
        )
        download_button.click()
        downloaded_file_path = os.path.join(
            os.path.expanduser("~"), "Downloads", files.FILE_TO_UPLOAD
        )
        if autoGUIutils.wait_for_file(
            downloaded_file_path, timeout=16
        ):  # skip hash checking if file not downloaded before timeout
            downloaded_file_hash = None
            with open(downloaded_file_path, "rb") as downloaded_file:
                downloaded_file_hash = hashlib.md5(
                    downloaded_file.read()
                    ).hexdigest()
            condition = downloaded_file_hash == ground_truth_hash
            assert condition, "Checksum mismatch"
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
        download_dir = os.path.join(os.path.expanduser("~"), "Downloads")
        autoGUIutils.wait_for_file(
            os.path.join(download_dir, files.file_name_for_download),
            timeout=18
        )
        assert files.file_name_for_download in os.listdir(download_dir)

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
    def test_search_for_files_by_types(self):
        # Test case to search for files by multiple types
        for file_type in files.filelist_types:
            file_names = self.higher_actions.search_by_type_action(file_type)

            # Check if files were found for the type
            assert len(file_names) > 0, f"No files found for type: {file_type}"

            # Check if text file was created for the type
            file_name = f"debug_file_names_{file_type}.log"
            assert os.path.isfile(file_name), f"Failed to create {file_name}"

    @pytest.mark.GROUPB
    @toast_testcase_name
    def test_move_file(self):
        filename = files.file_move_name
        dst_folder = files.destination_folder_name
        self.higher_actions.navigate_to("My Drive")
        self.higher_actions.move_action(filename, dst_folder)
        self.higher_actions.verify_file_in_destination(filename, dst_folder)
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
        for filename, destination_folder in zip(files.move_multiple_fnames, files.move_multiple_destinations):
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
        capacity_res = capacity * storage_units.get(unit, 1)
        cond = final_storage - initial_storage == capacity_res
        assert cond

from test.base_class import Base, get_number_of_testcases
from test.base_class import toast_testcase_name, plain_toast

from infrastructure import locators
import files
from infrastructure import autoGUIutils


class TestMiscellaneousActions(Base):
    @classmethod
    def setup_class(cls):

        super(cls, TestMiscellaneousActions).setup_class()
        prereqs = [files.view_info_file_name, files.share_file]
        file_list_to_upload = " ".join(list(map(lambda a: f'"{a}"', prereqs)))
        cls.higher_actions.click_on_new_button()
        upload_button = cls.higher_actions.wait_to_click(
            locators.new_menu_button_locator("File upload")
        )
        upload_button.click()
        autoGUIutils.type_into_dialogue_box(file_list_to_upload)
        cls.higher_actions.deal_duplicate_and_await_upload()

        # Creating path structure for navigate testcase.
        for folder_name in files.initial_path.split("/"):
            cls.higher_actions.create_folder_action(folder_name)

            folder_element = cls.higher_actions.select_item(folder_name)
            cls.higher_actions.double_click_element(folder_element)

        cls.higher_actions.navigate_to("My Drive")
        # For creating final path
        folder_element = cls.higher_actions.select_item("A")
        cls.higher_actions.double_click_element(folder_element)
        cls.higher_actions.create_folder_action("D")
        cls.higher_actions.navigate_to("My Drive")
        n_testcases = get_number_of_testcases(TestMiscellaneousActions)
        plain_toast(
            f"Prerequisites for suite {cls.__name__} ready.",
            f"Contains {n_testcases} testcases, starting now.",)

    @classmethod
    def teardown_class(cls):
        super(
            cls, TestMiscellaneousActions
        ).teardown_class()  # THEN SUPERCLASS TEARDOWN

    @toast_testcase_name
    def test_share_via_link(self):
        self.higher_actions.share_via_link(files.share_file)
        self.higher_actions.verify_copied_link()

    @toast_testcase_name
    def test_share_file_to_friend(self):
        file_to_be_shared = files.share_file
        frn_email = files.email
        # username=files.username
        self.higher_actions.share_link_to_friend(file_to_be_shared, frn_email)
        self.higher_actions.verify_share_link_to_friend(files.share_file, frn_email)

    @toast_testcase_name
    def test_view_file_info(self):
        self.higher_actions.select_item(files.view_info_file_name)
        autoGUIutils.view_shortcut()
        dlg_box_loc = locators.file_info_dialog_loc
        element = self.higher_actions.wait_to_click(dlg_box_loc)
        if not element:
            assert (
                False
            ), f"File info for {files.view_info_file_name} is not visible"
        else:
            self.higher_actions.click_on_close_button()
            assert True

    @toast_testcase_name
    def test_verify_tooltip_text(self):
        verification_result = self.higher_actions.verify_button_tooltips(
            files.button_names_and_tooltips
        )
        if verification_result:
            assert True

    @toast_testcase_name
    def test_verify_file_tooltip(self):
        verification_result = self.higher_actions.verify_file_tooltips()
        if verification_result:
            assert True

    @toast_testcase_name
    def test_navigate_to_path(self):
        self.higher_actions.traverse_path(files.initial_path, from_home=True)
        self.higher_actions.navigate_to_path(files.initial_path, files.final_path)

import sys

sys.path.append(r'C:\HPE_CTY_Project1_ClusterStor')
from infrastructure import locators

import files
from infrastructure import autoGUIutils


from base_class import BaseTest,toast_testcase_name

class TestMiscellaneousActions(BaseTest):
    @classmethod
    def setup_class(cls):
        super(cls, TestMiscellaneousActions).setup_class()#FIRST SUPER CLASS
        prereqs = [files.view_info_file_name, files.share_file]
        file_list_to_upload = " ".join(list(map(lambda a: f'"{a}"', prereqs)))
        cls.higher_actions.click_on_new_button()
        upload_button = cls.higher_actions.wait_to_click(locators.new_menu_button_locator("File upload"))
        upload_button.click()
        autoGUIutils.type_into_dialogue_box(file_list_to_upload)
        cls.higher_actions.deal_duplicate_and_await_upload()
        cls.higher_actions.refresh_and_wait_to_settle()
    
    @classmethod
    def teardown_class(cls):
        #FIRST SUBCLASS TEARDOWN LOGIC
        files_to_clean = [files.share_file , files.view_info_file_name]
        for filename in files_to_clean:
            cls.higher_actions.remove_file_action(filename)

        super(cls, TestMiscellaneousActions).teardown_class()#THEN SUPERCLASS TEARDOWN
    
    
    @toast_testcase_name
    def test_share_via_link(self ):
        self.higher_actions.open_share_window(files.share_file)
        autoGUIutils.n_tabs_shift_focus(3)
        autoGUIutils.press_enter()
        autoGUIutils.go_back_esc()
        self.higher_actions.verify_copied_link()

    @toast_testcase_name
    def test_share_file_to_friend(self):
        file_to_be_shared=files.share_file
        friend_email=files.email
        #username=files.username
        self.higher_actions.share_link_to_friend(file_to_be_shared,friend_email)
        res=self.higher_actions.verify_share_link_to_friend(files.share_file,friend_email)
        assert res, f"Friend's email {friend_email} not found in list"
    
    @toast_testcase_name
    def test_view_file_info(self):
        self.higher_actions.select_item(files.view_info_file_name)
        autoGUIutils.view_shortcut()
        element = self.higher_actions.wait_to_click(locators.file_info_dialog_locator)
        if not element:
            assert False, f"File info dialog for {files.view_info_file_name} is not visible"
        else:
            self.higher_actions.click_element(element)
            autoGUIutils.go_back_esc()
            assert True

    @toast_testcase_name
    def test_verify_tooltip_text(self):
        verification_result = self.higher_actions.verify_button_tooltips(files.button_names_and_tooltips)
        if verification_result:
            assert True

    @toast_testcase_name
    def test_verify_file_tooltip(self):
        verification_result = self.higher_actions.verify_file_tooltips()
        if verification_result:
            assert True

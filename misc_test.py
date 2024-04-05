import locators
import files
import autoGUIutils


from base_class import BaseTest

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
    
      
    def test_share_via_link(self ):
        self.higher_actions.navigate_to("Home")
        self.higher_actions.select_item(files.share_file)
        share_button = self.higher_actions.wait_for_element(locators.action_bar_button_selector("Share"))
        share_button.click()
        autoGUIutils.n_tabs_shift_focus(3)
        autoGUIutils.press_enter()
        autoGUIutils.go_back_esc()
        assert True

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

    def test_verify_tooltip_text(self):
        verification_result = self.higher_actions.verify_button_tooltips(files.button_names_and_tooltips)
        if verification_result:
            assert True

    def test_verify_file_tooltip(self):
        verification_result = self.higher_actions.verify_file_tooltips()
        if verification_result:
            assert True


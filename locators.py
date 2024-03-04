from selenium.webdriver.common.by import By

import files

welcome_span = (By.XPATH, "//span[contains(text(), 'Welcome')]")
sign_in_link = (By.LINK_TEXT, "Sign in")

new_button_selector = (By.CSS_SELECTOR, "button.brbsPe.Ss7qXc.a-qb-d")

def new_menu_button_locator (button_text):
    return (
    By.CSS_SELECTOR, f"div[data-tooltip='{button_text}'].a-v-T")
file_selector_ = (By.CSS_SELECTOR, "div.tyTrke.M3pype")

upload_complete_text = (
    By.XPATH, "//span[contains(text(), 'upload') and contains(text(), 'complete')]")
file_already_present_text = (By.CSS_SELECTOR, "div#EJL26d")
file_name_containerdiv = (By.CSS_SELECTOR, "div.KL4NAf")


ok_button_locator = (
    By.XPATH, '//button[@name="ok" and contains(@class, "h-De-Vb h-De-Y")]',)

show_more_files = (By.CSS_SELECTOR, 'button.UywwFc-d.UywwFc-d-Qu-dgl2Hf')


def file_selector(file_name): return (
    By.XPATH, f'//div[@class="uXB7xe" and contains(@aria-label,"{file_name}" )]')


folders_button_locator = (By.CSS_SELECTOR, 'button[name="T5ycX"]')
folder_locator = (
    By.XPATH, f'//div[@class="uXB7xe" and contains(@aria-label,"{files.folder_name}" )]',)
delete_confirm_button_locator = (
    By.XPATH,
    "//button[contains(@jsname, 'moQGCc') and contains(@jsaction, 'click:cOuCgd')]/span[text()='Delete forever']"
)

file_move_locator = (
    By.CSS_SELECTOR, f'div.uXB7xe[aria-label*="{files.file_move_name}"]')

copied_file_locator = (
    By.CSS_SELECTOR, f'div.uXB7xe[aria-label*="{files.expected_copied_file_name}"]')
make_a_copy_element_locator = (
    By.CSS_SELECTOR, 'div[aria-label="Make a copy"]')


input_field_locator=(By.CLASS_NAME, "LUNIy")
file_info_dialog_locator = (By.CSS_SELECTOR,"div.wbg7nb")

user_profile_button_locator = (By.CSS_SELECTOR, 'a.gb_d[aria-label*="Google Account"]')
sign_out_button_locator = (By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div/div/div/div[2]/div/div[2]/div[2]/span/span[2]') 

def action_bar_button_selector(aria_label):
    return (By.CSS_SELECTOR , f"div[aria-label='{aria_label}'][role='button'][aria-hidden='false'][aria-disabled='false']" )

def left_menu_page_selector(aria_label):
    return (By.CSS_SELECTOR , f"div[aria-label='{aria_label}']")

def span_with_text(text):
    return (By.XPATH, f"//span[contains(text(), {text})]")


search_bar_locator = (By.CSS_SELECTOR, 'input[aria-label="Search in Drive"]')
type_button_locator = (By.CSS_SELECTOR, 'div[aria-label="Type"]')
my_drive_button_locator = (By.CSS_SELECTOR, 'div[aria-label="My Drive"]')
type_of_file_locator = (By.CSS_SELECTOR, f'li[role="menuitemcheckbox"][name="{files.type}"]')

folders_button_locator = (By.CSS_SELECTOR, 'button[name="T5ycX"]')
move_to_trash_button_locator = (By.CSS_SELECTOR, 'div[aria-label="Move to trash"]')

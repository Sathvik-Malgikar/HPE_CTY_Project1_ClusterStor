from selenium.webdriver.common.by import By

import files


new_button_selector = (By.CSS_SELECTOR, "button.brbsPe.Ss7qXc.a-qb-d")

file_upload_button_selector = (
    By.CSS_SELECTOR, "div[data-tooltip='File upload'].a-v-T")
file_selector_ = (By.CSS_SELECTOR, "div.tyTrke.M3pype")
download_file_selector = (By.CSS_SELECTOR, "div[aria-label='Download']")
upload_complete_text = (
    By.CSS_SELECTOR, "span[aria-label='1 upload complete'].af-V")
file_already_present_text = (By.CSS_SELECTOR, "div#EJL26d")
file_name_containerdiv = (By.CSS_SELECTOR, "div.KL4NAf")


ok_button_locator = (
    By.XPATH, '//button[@name="ok" and contains(@class, "h-De-Vb h-De-Y")]',)
file_name_selector = (
    By.XPATH, f'//div[@class="uXB7xe" and contains(@aria-label,"{files.file_name}" )]',)
renamed_file_name_selector = (
    By.XPATH, f'//div[@class="uXB7xe" and contains(@aria-label,"{files.renamed_file_name}" )]',)

trash_button_locator = (By.XPATH, '//div[@aria-label="Trash"]')
trashed_file_locator = (
    By.XPATH, f'//div[@class="uXB7xe" and contains(@aria-label,"{files.file_to_be_restored}" )]',)
home_button_locator = (By.XPATH, '//div[@aria-label="Home"]')
restored_file_locator = (
    By.XPATH, f'//div[@class="uXB7xe" and contains(@aria-label,"{files.file_to_be_restored}" )]',)
# restore_from_trash_button_locator = (By.XPATH, '//div[@aria-label="Restore from trash"]')
restore_from_trash_button_locator = (
    By.CSS_SELECTOR, 'div.h-sb-Ic.h-R-d.a-c-d.a-s-Ba-d-Mr-Be-nAm6yf[aria-label="Restore from trash"]')


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
destination_folder_element_locator = (
    By.XPATH, f'//div[contains(@aria-label, "{files.destination_folder_name}")]')
my_drive_button_locator = By.CSS_SELECTOR, 'span.a-s-T[aria-label="My Drive"][jsname="KSzLFd"]'

copied_file_locator = (
    By.CSS_SELECTOR, f'div.uXB7xe[aria-label*="{files.expected_copied_file_name}"]')
make_a_copy_element_locator = (
    By.CSS_SELECTOR, 'div[aria-label="Make a copy"]')

    
new_btn_locator=(By.CLASS_NAME,'jYPt8c',)
new_folder_option_locator=(By.CSS_SELECTOR, "div.a-v-T[data-tooltip='New folder']")
input_field_locator=(By.CLASS_NAME, "LUNIy")
delete_forever_button_locator = (By.XPATH, "//div[@aria-label='Delete forever']")
file_info_dialog_locator = (By.CSS_SELECTOR,"div.wbg7nb")
trash_button_locator=(By.XPATH, "//span[text()='Trash']")
user_profile_button_locator = (By.CSS_SELECTOR, 'a.gb_d[aria-label*="Google Account"]')
sign_out_button_locator = (By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div/div/div/div[2]/div/div[2]/div[2]/span/span[2]') 


search_bar_locator = (By.CSS_SELECTOR, 'input[aria-label="Search in Drive"]')
type_button_locator = (By.CSS_SELECTOR, 'div[aria-label="Type"]')
my_drive_button_locator = (By.CSS_SELECTOR, 'div[aria-label="My Drive"]')
type_of_file_locator = (By.CSS_SELECTOR, f'li[role="menuitemcheckbox"][name="{files.type}"]')
file_to_be_searched_locator = (By.XPATH, f'//div[@class="uXB7xe" and contains(@aria-label,"{files.file_to_be_searched}" )]')
file_to_be_searched_by_type_locator = (By.XPATH, f'//div[@class="uXB7xe" and contains(@aria-label,"{files.file_to_be_searched_by_type}" )]')

folders_button_locator = (By.CSS_SELECTOR, 'button[name="T5ycX"]')
move_to_trash_button_locator = (By.CSS_SELECTOR, 'div[aria-label="Move to trash"]')

def folder_selector(folder_name): return (
    By.XPATH, f'//div[@class="uXB7xe" and contains(@aria-label,"{files.folder_name_to_be_removed}" )]')


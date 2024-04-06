from selenium.webdriver.common.by import By

import files

welcome_span = (By.XPATH, "//span[contains(text(), 'Welcome')]")
sign_in_link = (By.LINK_TEXT, "Sign in")

new_button_selector = (By.CSS_SELECTOR, "button.brbsPe.Ss7qXc.a-qb-d")
send_button_selector = (By.CSS_SELECTOR,"button:contains('Send')")
access_info_selector = (By.CLASS_NAME, "ZvUowc")
def new_menu_button_locator (button_text):
    return (
    By.CSS_SELECTOR, f"div[data-tooltip='{button_text}'].a-v-T")
file_selector_ = (By.CSS_SELECTOR, "div.tyTrke.M3pype")

upload_complete_text = (
    By.XPATH, "//span[contains(text(), 'upload') and contains(text(), 'complete')]")
file_already_present_text = (By.CSS_SELECTOR, "div#EJL26d")
file_name_containerdiv = (By.CSS_SELECTOR, "div.KL4NAf")


ok_button_locator = (By.CSS_SELECTOR, "button[name='ok'].h-De-Vb.h-De-Y[tabindex='0']")

show_more_files = ( By.XPATH, "//span[contains(text(), 'Show more files')]")


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


sign_in_account_locator= (By.CSS_SELECTOR , "div[data-authuser='-1']")


add_button_locator = (By.CSS_SELECTOR, 'button.VfPpkd-LgbsSe.VfPpkd-LgbsSe-OWXEXe-k8QpJ.VfPpkd-LgbsSe-OWXEXe-dgl2Hf.nCP5yc.AjY5Oe.DuMIQc.LQeN7.xFWpbf.CZCFtc-bMElCd.sj692e.RCmsv.jbArdc.oWBWHf.MKuq5e-LgbsSe')

# all_locations_button_locator = (By.CSS_SELECTOR, '#all_locations')

all_locations_button_locator = (By.CSS_SELECTOR, 'button.VfPpkd-AznF2e.VfPpkd-AznF2e-OWXEXe-jJNx8e-QBLLGd.WbUJNb.FEsNhd.VCOGmd.u4B0v[role="tab"][aria-selected="false"][id="all_locations"]')

shortcut_folder_button_locator = (By.CSS_SELECTOR, 'td[aria-label="ShortcutFolder"]')

manage_access_button_selector = (By.XPATH, "//span[text()='Manage access']")

access_list=(By.XPATH, "//div[@class='fSFQ2']//div[@class='fOEalf']//div[@class='EDtwUe']")

access_section=(By.XPATH,"//section[@class='ZvUowc']")
email_selector=(By.CSS_SELECTOR, f'div.fOEalf[data-hovercard-id="{files.email}"] div.Jw4Ike')
     
undo_button_selector=(By.CSS_SELECTOR, "span.la-Y-A.kc-A[data-target='undo']")

error_message_selector=((By.CLASS_NAME, "errorMessage"))


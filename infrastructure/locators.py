from selenium.webdriver.common.by import By

import files


def span_with_text(text):
    """
    Text can be a single word , will be checked if it is present in the text as a substring
    If text is multiple words it has to be a valid XPATH expression like: sign or in and logout
    Cannot be like: sign in or upload completed (no whitespaces allowed)
    """

    return (By.XPATH, f'//span[contains(text(), "{text}")]')


sign_in_link = (By.LINK_TEXT, "Sign in")
password_input = (By.CSS_SELECTOR, "input[name='Passwd']")

new_button_selector = (By.CSS_SELECTOR, "button.brbsPe.Ss7qXc.a-qb-d")
send_button_selector = (By.CSS_SELECTOR, "button:contains('Send')")
access_info_selector = (By.CLASS_NAME, "ZvUowc")


def new_menu_button_locator(button_text):
    return (By.CSS_SELECTOR, f"div[data-tooltip='{button_text}'].a-v-T")


file_selector_ = (By.CSS_SELECTOR, "div.tyTrke.M3pype")

file_already_present_text = (By.CSS_SELECTOR, "div#EJL26d")
fname_div = (By.CSS_SELECTOR, "div.KL4NAf")

ok_button_locator = (By.CSS_SELECTOR, "button[name='ok'].h-De-Vb.h-De-Y[tabindex='0']")

show_more_files = (By.XPATH, "//span[contains(text(), 'Show more files')]")


def file_selector(file_name):
    return (
        By.XPATH,
        f'//div[@class="uXB7xe" and contains(@aria-label,"{file_name}" )]',
    )


folders_button_locator = (By.CSS_SELECTOR, 'button[name="T5ycX"]')
folder_locator = (
    By.XPATH,
    f'//div[@class="uXB7xe" and contains(@aria-label,"{files.folder_name}" )]',
)
delete_confirm_button_locator = (
    By.XPATH,
    "//button[contains(@jsname, 'moQGCc') and contains(@jsaction, 'click:cOuCgd')]/span[text()='Delete forever']",
)

upload_status_span = (By.CSS_SELECTOR, "span.af-V")

file_move_locator = (
    By.CSS_SELECTOR,
    f'div.uXB7xe[aria-label*="{files.file_move_name}"]',
)

make_a_copy_element_locator = (By.CSS_SELECTOR, 'div[aria-label="Make a copy"]')

input_field_locator = (By.CLASS_NAME, "LUNIy")
file_info_dialog_loc = (By.CSS_SELECTOR, "div.wbg7nb")

user_profile_button_locator = (By.CSS_SELECTOR, 'a.gb_d[aria-label*="Google Account"]')
sign_out_button_locator = (
    By.XPATH,
    '//*[@id="yDmH0d"]/c-wiz/div/div/div/div/div[2]/div/div[2]/div[2]/span/span[2]',
)


def action_bar_button_selector(aria_label):
    return (
        By.CSS_SELECTOR,
        f"div[aria-label='{aria_label}'][role='button'][aria-hidden='false'][aria-disabled='false']",
    )


def left_menu_page_selector(aria_label):
    return (By.CSS_SELECTOR, f"div[aria-label='{aria_label}']")


search_bar_locator = (By.CSS_SELECTOR, 'input[aria-label="Search in Drive"]')
type_button_locator = (By.CSS_SELECTOR, 'div[aria-label="Type"]')
my_drive_button_locator = (By.CSS_SELECTOR, 'div[aria-label="My Drive"]')


def type_of_file_selector(file_type):
    return (
        By.CSS_SELECTOR,
        f'li[role="menuitemcheckbox"][name="{files.filelist_types[file_type]}"]',
    )


folders_button_locator = (By.CSS_SELECTOR, 'button[name="T5ycX"]')
move_to_trash_button_locator = (By.CSS_SELECTOR, 'div[aria-label="Move to trash"]')

sign_in_account_locator = (By.CSS_SELECTOR, "div[data-authuser='-1']")

add_button_locator = (
    By.CSS_SELECTOR,
    "button.VfPpkd-LgbsSe.VfPpkd-LgbsSe-OWXEXe-k8QpJ.VfPpkd-LgbsSe-OWXEXe-dgl2Hf.nCP5yc.AjY5Oe.DuMIQc.LQeN7.xFWpbf.CZCFtc-bMElCd.sj692e.RCmsv.jbArdc.oWBWHf.MKuq5e-LgbsSe",
)

# all_locations_button_locator = (By.CSS_SELECTOR, '#all_locations')

all_locations_button_locator = (
    By.CSS_SELECTOR,
    'button.VfPpkd-AznF2e.VfPpkd-AznF2e-OWXEXe-jJNx8e-QBLLGd.WbUJNb.FEsNhd.VCOGmd.u4B0v[role="tab"][aria-selected="false"][id="all_locations"]',
)

email_selector = (By.CSS_SELECTOR, "div[aria-label='sravnihm2021@gmail.com']")
storage_selector = (By.CSS_SELECTOR, '[data-target="quota"]')
undo_button_selector = (By.CSS_SELECTOR, "span.la-Y-A.kc-A[data-target='undo']")

error_message_selector = (By.CLASS_NAME, "errorMessage")

empty_trash_btn = (By.CSS_SELECTOR, "span.VfPpkd-vQzf8d")

close_details_button = (
    By.CSS_SELECTOR,
    "div[data-target='hideDetails'][role='button']",
)

navigation_bar_items = (By.CSS_SELECTOR, ".o-Yc-o")

from selenium.webdriver.common.by import By

import files


new_button_selector = (By.CSS_SELECTOR,"button.brbsPe.Ss7qXc.a-qb-d")
file_upload_button_selector = (By.CSS_SELECTOR,"div[data-tooltip='File upload'].a-v-T")
file_selector = (By.CSS_SELECTOR,"div.tyTrke.M3pype")
download_file_selector = (By.CSS_SELECTOR,"div[aria-label='Download'].pc7nUb.kXQBpc.Dk9rmd")
upload_complete_text = (By.CSS_SELECTOR,"span[aria-label='1 upload complete'].af-V")
file_already_present_text = (By.CSS_SELECTOR,"div#EJL26d")
file_name_containerdiv = (By.CSS_SELECTOR,"div.KL4NAf")



ok_button_locator = (By.XPATH,'//button[@name="ok" and contains(@class, "h-De-Vb h-De-Y")]',)
file_name_selector = (By.XPATH, f'//div[@class="uXB7xe" and contains(@aria-label,"{files.file_name}" )]',)
renamed_file_name_selector = (By.XPATH, f'//div[@class="uXB7xe" and contains(@aria-label,"{files.renamed_file_name}" )]',)


trash_button_locator = (By.XPATH, '//div[@aria-label="Trash"]')
trashed_file_locator = (By.XPATH, f'//div[@class="uXB7xe" and contains(@aria-label,"{files.trashed_file_name}" )]',)
home_button_locator = (By.XPATH, '//div[@aria-label="Home"]')
restored_file_locator = (By.XPATH, f'//div[@class="uXB7xe" and contains(@aria-label,"{files.trashed_file_name}" )]',)
restore_from_trash_button_locator = (By.XPATH, '//div[@aria-label="Restore from trash"]')

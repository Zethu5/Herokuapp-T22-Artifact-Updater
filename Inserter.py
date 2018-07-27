import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Change if the artifact number goes up
number_of_artifacts = 78

# Optimizer URL
url = 'https://tt2-optimizer.herokuapp.com/'

# Get path of the 'SequenceTT2' import and export key file
import_key_file_path = input('Key file path: ')
files_directory = re.search(r'\\\w+\.\w+$', import_key_file_path)

if files_directory:
    file_name = files_directory.group()

export_key_file_path = import_key_file_path.replace(file_name, '')
export_key_file_path += '\Export_Key.txt'

# Get path of the 'SequenceTT2' artifacts file
artifacts_file_path = input('Artifacts file path: ')

# Variable to save import key
import_key = ''

# Set import_key data
with open(import_key_file_path) as file:
    for line in file.readlines():
        import_key += line

# Variable to save all artifacts levels
artifact_levels = []

# Set all variable levels to artifacts_levels variable
with open(artifacts_file_path) as file:
    for line in file.readlines():
        result = re.search(r'\d+$', line)

        if result:
            artifact_levels.append(result.group())

# Open Herokuapp TT2 Optimizer
driver = webdriver.Chrome()
driver.get(url)

try:
    element = WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable((By.ID, 'import'))
    )
finally:
    None

# Click 'Import Data' and send the import_key
import_data = driver.find_element_by_id('import')
import_data.click()
import_data.send_keys(import_key)

try:
    element = WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="import_wrap"]/div[3]/button'))
    )
finally:
    None

# Click 'Start Import'
start_import = driver.find_element_by_xpath('//*[@id="import_wrap"]/div[3]/button')
start_import.click()

try:
    element = WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable((By.ID, 'artifacts-tab'))
    )
finally:
    None

# Go to the artifacts tab
artifacts_tab = driver.find_element_by_id('artifacts-tab')
artifacts_tab.click()

try:
    element = WebDriverWait(driver, 3).until(
        EC.visibility_of_any_elements_located((By.XPATH, '//*[@placeholder="0"]'))
    )
finally:
    None

# Get all the inputs in the tab
all_inputs_in_page = driver.find_elements_by_xpath('//*[@placeholder="0"]')

# Set values of the artifact inputs - as the length of the number of artifacts
# Change 'number_of_artifacts' parameter as needed in future distributions
for i in range(number_of_artifacts):
    all_inputs_in_page[i].clear()
    all_inputs_in_page[i].send_keys(artifact_levels[i])

try:
    element = WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable((By.ID, 'style-tab'))
    )
finally:
    None

# Got to style tab
style_tab = driver.find_element_by_id('style-tab')
style_tab.click()

try:
    element = WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="style"]/button[1]'))
    )
finally:
    None


# Click on 'Export Data'
start_export = driver.find_element_by_xpath('//*[@id="style"]/button[1]')
start_export.click()

try:
    element = WebDriverWait(driver, 3).until(
        EC.visibility_of_element_located((By.ID, 'export'))
    )
finally:
    None

# Get the key generated
export_data = driver.find_element_by_id('export')

# Write key to a file
with open(export_key_file_path, 'w') as file:
    file.write(export_data.text)
    file.close()

# Close driver
driver.quit()
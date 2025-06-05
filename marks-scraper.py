from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

# Setup browser
options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

# Open the site
driver.get("https://crce-students.contineo.in/parents/index.php")

# Wait helper
wait = WebDriverWait(driver, 10)

# Wait and fill PRN number
prn_input = wait.until(EC.presence_of_element_located((By.ID, "username")))
prn_input.send_keys("2022016402259731")

# Wait for dropdowns
day_select = Select(wait.until(EC.presence_of_element_located((By.ID, "dd"))))
month_select = Select(driver.find_element(By.ID, "mm"))
year_select = Select(driver.find_element(By.ID, "yyyy"))

# Select DOB values (note: space in value "16 ")
day_select.select_by_value("16 ")
month_select.select_by_value("04")
year_select.select_by_value("2004")

# Wait for and click Login button via JS to avoid interception
submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit']")))
driver.execute_script("arguments[0].click();", submit_button)

# Optional: wait for redirection to dashboard
time.sleep(5)

# Optional: take screenshot to confirm login
driver.save_screenshot("after_login.png")

# Optional: continue scraping marks...

# Keep browser open or close when done
# driver.quit()

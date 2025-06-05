from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re
import time

# Setup Chrome driver
driver = webdriver.Chrome()
driver.get("https://crce-students.contineo.in/parents/index.php")

wait = WebDriverWait(driver, 10)

# Fill login form
prn_input = wait.until(EC.presence_of_element_located((By.ID, "username")))
prn_input.send_keys("2022016402259731")

# Select DOB
Select(driver.find_element(By.ID, "dd")).select_by_value("16 ")
Select(driver.find_element(By.ID, "mm")).select_by_value("04")
Select(driver.find_element(By.ID, "yyyy")).select_by_value("2004")

# Click login button using JavaScript to avoid click interception
submit_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
driver.execute_script("arguments[0].click();", submit_button)

# Wait for dashboard to load
time.sleep(5)

# Get full page source
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# Extract scripts
scripts = soup.find_all("script")

# Initialize holders
cie_marks = {}
attendance = {}

for script in scripts:
    if "columns" in script.text:
        # CIE Marks
        if '"MSE"' in script.text and "stackedBarChart_1" in script.text:
            cie_data = re.findall(r'\["(.*?)",(.*?)\]', script.text)
            for entry in cie_data:
                label = entry[0]
                values = [v.strip('"') if v != "null" else None for v in entry[1].split(',')]
                cie_marks[label] = values

        # Attendance
        elif '"CSC601"' in script.text and "gaugeTypeMulti" in script.text:
            att_data = re.findall(r'\["(.*?)",(\d+)\]', script.text)
            for subject, percent in att_data:
                attendance[subject] = int(percent)

# Output results
print("\n CIE Marks:")
for label, marks in cie_marks.items():
    print(f"{label}: {marks}")

print("\n Attendance:")
for subject, percent in attendance.items():
    print(f"{subject}: {percent}%")

driver.quit()

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re
import time
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import pandas as pd 
import json

# Setup Chrome driver
driver = webdriver.Chrome()
driver.get("https://crce-students.contineo.in/parents/index.php")

wait = WebDriverWait(driver, 10)

# Fill login form
prn_input = wait.until(EC.presence_of_element_located((By.ID, "username")))
prn_input.send_keys("your-prn-number")

Select(driver.find_element(By.ID, "dd")).select_by_value("13 ")
Select(driver.find_element(By.ID, "mm")).select_by_value("12")
Select(driver.find_element(By.ID, "yyyy")).select_by_value("2004")

submit_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
driver.execute_script("arguments[0].click();", submit_button)

# Wait for dashboard to load
time.sleep(5)

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
scripts = soup.find_all("script")

cie_marks = {}
attendance = {}

# Subjects as per chart
subjects = ["CSC601", "CSC602", "CSC603", "CSC604", "CSL601", "CSL602", "CSL603", "CSL604", "CSL605", "CSM601", "CSDL06013"]

for script in scripts:
    text = script.text.strip()

    # === Extract CIE Marks ===
    if "stackedBarChart_1" in text and "columns" in text:
        try:
            match = re.search(r'columns\s*:\s*(\[\[.*?\]\])', text, re.DOTALL)
            if match:
                raw_json = match.group(1)

                # Fix JS-style quotes and nulls
                json_ready = raw_json.replace("'", '"').replace("null", "null")
                cie_list = json.loads(json_ready)

                for row in cie_list:
                    label = row[0]
                    values = [float(v) if v is not None else None for v in row[1:]]
                    cie_marks[label] = values
        except Exception as e:
            print("Error parsing CIE JSON:", e)

    # === Extract Attendance ===
    elif "gaugeTypeMulti" in text and "columns" in text:
        att_data = re.findall(r'\["(.*?)",(\d+)\]', text)
        for subject, percent in att_data:
            attendance[subject] = int(percent)

driver.quit()

# === Create DataFrames ===
cie_df = pd.DataFrame({"Subject": subjects})
for label, scores in cie_marks.items():
    padded = (scores + [None] * len(subjects))[:len(subjects)]
    cie_df[label] = padded

# Drop any column with all NaNs
cie_df = cie_df.dropna(axis=1, how='all')

att_df = pd.DataFrame(list(attendance.items()), columns=["Subject", "Attendance (%)"])

# === Save to PDF ===
pdf_path = "marks_and_attendance.pdf"
with PdfPages(pdf_path) as pdf:
    # Plot CIE Table
    if cie_df.shape[1] > 1:
        fig1, ax1 = plt.subplots(figsize=(12, 6))
        ax1.axis('off')
        cie_cleaned = cie_df.fillna("").astype(str)  # Replace NaN with ""
        cie_table = ax1.table(cellText=cie_cleaned.values,
                              colLabels=cie_cleaned.columns,
                              cellLoc='center',
                              loc='center')
        cie_table.auto_set_font_size(False)
        cie_table.set_fontsize(10)
        cie_table.scale(1.2, 1.2)
        plt.title("CIE Marks", fontsize=14)
        pdf.savefig(fig1, bbox_inches='tight')
        plt.close(fig1)
    else:
        print("No CIE data to plot.")

    # Plot Attendance Table
    if not att_df.empty:
        fig2, ax2 = plt.subplots(figsize=(8, 4))
        ax2.axis('off')
        att_cleaned = att_df.fillna("").astype(str)
        att_table = ax2.table(cellText=att_cleaned.values,
                              colLabels=att_cleaned.columns,
                              cellLoc='center',
                              loc='center')
        att_table.auto_set_font_size(False)
        att_table.set_fontsize(10)
        att_table.scale(1.2, 1.2)
        plt.title("Attendance (%)", fontsize=14)
        pdf.savefig(fig2, bbox_inches='tight')
        plt.close(fig2)
    else:
        print("No Attendance data to plot.")

print(f"\n Data saved to: '{pdf_path}'")

# Contineo Marks & Attendance Scraper

This Python script uses **Selenium** and **BeautifulSoup** to automatically log in to the CRCE Contineo Portal and extract your **CIE marks** and **attendance** data. It generates a clean, printable **PDF report** with tables using **Matplotlib**.

---

## Features

- Automated login using PRN and Date of Birth
- Extracts:
  - CIE (Continuous Internal Evaluation) Marks
  - Subject-wise Attendance Percentages
- Outputs data into a formatted **PDF report**
- Easy to customize for any CRCE student

---

## Requirements

- Python 3.7+
- Google Chrome installed
- Matching version of [ChromeDriver](https://googlechromelabs.github.io/chrome-for-testing/#stable)

---

## Installation

1. **Clone this repository**
   ```bash
   git clone https://github.com/your-username/contineo-marks-scraper.git
   cd marks-scraper
   python -m venv venv
   venv\Scripts\activate          # For Windows
---
   
2. **Install dependencies**
   ```bash
   pip install selenium beautifulsoup4 matplotlib pandas
---

3. **Download ChromeDriver**
- Check your current Google Chrome version (go to chrome://settings/help).
- Visit the official Chrome to download the matching ChromeDriver from: https://googlechromelabs.github.io/chrome-for-testing/#stable
- Extract the chromedriver.exe file.
- Place it in the project folder or add its location to your system PATH.

4. **Setup**
   1. Open marks-scraper.py in any code editor.
      
   2. Update your credentials:
      ```bash
      prn_input.send_keys("YOUR_PRN_NUMBER")
      Select(driver.find_element(By.ID, "dd")).select_by_value("DD ")   # Day (e.g. "05 ") Note the space after the number
      Select(driver.find_element(By.ID, "mm")).select_by_value("MM")    # Month (e.g. "06")
      Select(driver.find_element(By.ID, "yyyy")).select_by_value("YYYY")# Year (e.g. "2003")

   3. Update the subject list if your subjects differ:
      ```bash
      subjects = ["CSC601", "CSC602", ..., "CSDL06013"]

5. **Running the Script**
   ```bash
   python marks-scraper.py
  After a few seconds, a file called marks_and_attendance.pdf will be generated in the same directory. It contains your CIE Marks and Attendance tables.
  ```bash
   marks_and_attendance.pdf


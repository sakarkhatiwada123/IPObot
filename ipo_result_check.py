from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


# Function to read credentials from a file
def read_credentials(file_path):
    credentials_list = []
    with open(file_path, "r") as file:
        for line in file:
            parts = line.strip().split(";")  # Split using semicolon (;)
            if len(parts) >= 6:
                user_id, username, password, crn, pin, name = parts[:6]
                credentials_list.append({
                    "id": user_id,
                    "username": username,
                    "password": password,
                    "crn": crn,
                    "pin": pin,
                    "name": name
                })
    return credentials_list


credentials = read_credentials("credentials.txt")  # Read credentials

# Selenium setup
options = Options()
options.add_argument("--headless")  # Headless mode
options.add_argument("--disable-gpu")  # Stability for headless mode

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://meroshare.cdsc.com.np/#/login")
driver.maximize_window()

selected_ipo_name = ""
first_user = True  # To track if it's the first user

for user_cred in credentials:
    user_id = user_cred["id"]
    username_text = user_cred["username"]
    password_text = user_cred["password"]
    crn_text = user_cred["crn"]
    pin_text = user_cred["pin"]
    name_text = user_cred["name"]

    dpid_dropdown = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'select2-selection__rendered')]"))
    )
    dpid_dropdown.click()

    dpid_option = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, f"//li[contains(text(), '{user_id}')]"))
    )
    dpid_option.click()

    username = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="username"]'))
    )
    username.send_keys(username_text)

    password = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="password"]'))
    )
    password.send_keys(password_text)

    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Login')]"))
    )
    login_button.click()

    my_asba = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="sideBar"]/nav/ul/li[8]/a'))
    )
    my_asba.click()

    application_report = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/div/app-asba/div/div[1]/div/div/ul/li[3]/a/span'))
    )
    application_report.click()

    application_report_elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//div[@class='company-list']"))
    )

    if first_user:
        print("Select the number of the IPO for status check")
        for i, ipo in enumerate(application_report_elements[:10]):
            company_name = ipo.find_element(By.XPATH, ".//span[@tooltip='Company Name']").text
            issue_details = ipo.find_element(By.XPATH, ".//span[@tooltip='Sub Group']").text
            share_type = ipo.find_element(By.XPATH, ".//span[@class='share-of-type']").text
            print(f"{i + 1}. {company_name} ({issue_details}) - {share_type}")

        while True:
            try:
                choice = int(input("Enter the number of the IPO you want to check status for: "))
                if 1 <= choice <= len(application_report_elements):
                    selected_ipo_name = application_report_elements[choice - 1].find_element(
                        By.XPATH, ".//span[@tooltip='Company Name']").text
                    break
                else:
                    print("Invalid choice. Please enter a number from the list.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        print(f"Selected IPO: {selected_ipo_name}")
        first_user = False  # Don't ask again

    # Find IPO in application list
    ipo_found = False
    for ipo in application_report_elements:
        company_name = ipo.find_element(By.XPATH, ".//span[@tooltip='Company Name']").text
        if company_name == selected_ipo_name:
            apply_button = ipo.find_element(By.XPATH, './/button[contains(@class, "btn-issue")]')
            apply_button.click()
            print(f"Selected IPO is: {company_name}")
            ipo_found = True
            break

    if not ipo_found:
        print(f"\033[91m❌ Could not find the application for: {selected_ipo_name} (User: {name_text})\033[0m")
    else:
        time.sleep(1)
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//app-application-report"))
            )
            visible_elements = driver.find_elements(By.XPATH, "//app-application-report//*[text()[normalize-space()]]")
            page_lines = [element.text.strip() for element in visible_elements if element.text.strip()]
            if page_lines:
                print(f'{page_lines[-3]} for {name_text}')
            else:
                print("No visible text found.")
        except Exception as e:
            print(f"Error reading status for {name_text}: {e}")

    logout = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/app-dashboard/header/div[2]/div/div/div/ul/li[1]'))
    )
    logout.click()
    WebDriverWait(driver, 10)

driver.quit()

from flask import Flask, render_template, request, redirect, url_for
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

app = Flask(__name__)

# Global variable to store logs and IPO names
logs = []
ipo_names = []
selected_ipo_name = None
cached_user_data = {}  # Store credentials for reuse

# Utility to log messages to the browser
def log(message):
    print(message)
    logs.append(message)

# Core IPO fetching function
def fetch_ipo_list(user_id, username_text, password_text, crn_text, pin_text, name_text):
    global cached_user_data, selected_ipo_name
    logs.clear()
    ipo_names.clear()
    selected_ipo_name = None
    cached_user_data = {
        "id": user_id,
        "username": username_text,
        "password": password_text,
        "crn": crn_text,
        "pin": pin_text,
        "name": name_text
    }

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://meroshare.cdsc.com.np/#/login")
    driver.maximize_window()

    try:
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

        for i, ipo in enumerate(application_report_elements[:10]):
            company_name = ipo.find_element(By.XPATH, ".//span[@tooltip='Company Name']").text
            ipo_names.append(company_name)
            log(f"{i + 1}. {company_name}")

        driver.quit()

    except Exception as e:
        log(f"❌ Error during IPO fetch: {str(e)}")
        driver.quit()

# Function to check selected IPO status
def check_selected_ipo(index):
    global cached_user_data, selected_ipo_name

    if index < 0 or index >= len(ipo_names):
        log("Invalid IPO selection.")
        return

    selected_ipo_name = ipo_names[index]
    user_id = cached_user_data["id"]
    username_text = cached_user_data["username"]
    password_text = cached_user_data["password"]
    crn_text = cached_user_data["crn"]
    pin_text = cached_user_data["pin"]
    name_text = cached_user_data["name"]

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://meroshare.cdsc.com.np/#/login")
    driver.maximize_window()

    try:
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

        for ipo in application_report_elements:
            company_name = ipo.find_element(By.XPATH, ".//span[@tooltip='Company Name']").text
            if company_name == selected_ipo_name:
                apply_button = ipo.find_element(By.XPATH, './/button[contains(@class, "btn-issue")]')
                apply_button.click()
                log(f"Selected IPO: {company_name} (User: {name_text})")

                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//app-application-report"))
                )
                visible_elements = driver.find_elements(By.XPATH, "//app-application-report//*[text()[normalize-space()]]")
                page_lines = [element.text.strip() for element in visible_elements if element.text.strip()]

                if page_lines:
                    log(f"Status Line 1: {page_lines[-2]}")
                    log(f"Status Line 2: {page_lines[-3]}")
                else:
                    log("No visible IPO status found.")
                break

        time.sleep(2)
        driver.quit()

    except Exception as e:
        log(f"❌ Error checking IPO status: {str(e)}")
        driver.quit()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_id = request.form['id']
        username = request.form['username']
        password = request.form['password']
        crn = request.form['crn']
        pin = request.form['pin']
        name = request.form['name']

        fetch_ipo_list(user_id, username, password, crn, pin, name)
        return redirect(url_for('select_ipo'))

    return '''
    <h2>IPO Fetch Form</h2>
    <form method="post">
      ID: <input name="id"><br>
      Username: <input name="username"><br>
      Password: <input name="password" type="password"><br>
      CRN: <input name="crn"><br>
      PIN: <input name="pin"><br>
      Name: <input name="name"><br>
      <input type="submit" value="Fetch IPO List">
    </form>
    '''

@app.route("/select", methods=["GET", "POST"])
def select_ipo():
    if request.method == "POST":
        try:
            index = int(request.form['ipo_index']) - 1
            check_selected_ipo(index)
        except Exception as e:
            log(f"Error in IPO selection: {str(e)}")
        return redirect(url_for('result'))

    ipo_options = "<br>".join([f"{i+1}. {name}" for i, name in enumerate(ipo_names)])
    return f'''
    <h2>Select IPO to Check</h2>
    <form method="post">
      {ipo_options}<br><br>
      IPO Number: <input name="ipo_index"><br>
      <input type="submit" value="Check IPO Status">
    </form>
    '''

@app.route("/result")
def result():
    return "<h2>IPO Status Result</h2>" + "<br>".join(logs) + '<br><br><a href="/">Start Over</a>'

if __name__ == "__main__":
    app.run(debug=True)
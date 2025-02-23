from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


quantity = input("Enter the quantity to be applied for all of the users: ") 

# Function to read credentials from a file
def read_credentials(file_path):
    credentials_list = []
    with open(file_path, "r") as file:
        for line in file:
            parts = line.strip().split(";")  # Split using semicolon (;)
            if len(parts) >= 5: 
                user_id, username, password, crn, pin = parts[:5]
                credentials_list.append({"id": user_id, "username": username, "password": password, "crn": crn, "pin": pin})
    return credentials_list


credentials = read_credentials("credentials.txt")   # Read credentials

# Selenium setup
options = Options()
<<<<<<< HEAD
options.add_experimental_option("detach", True)
=======
#options.add_experimental_option("detach", True)
options.add_argument("--headless")  #headless mode
options.add_argument("--disable-gpu")   #stability for headless mode
>>>>>>> 1c38537 (Updated main.py)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://meroshare.cdsc.com.np/#/login")
driver.maximize_window()

for user_cred in credentials:
    user_id = user_cred["id"]
    username_text = user_cred["username"]
    password_text = user_cred["password"]
    crn_text = user_cred["crn"]
    pin_text = user_cred["pin"]

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

<<<<<<< HEAD
    print(f"✅ Successfully logged in with ID: {username_text}")
=======
    #print(f"✅ Successfully logged in with ID: {username_text}")
    print(f"\033[94m✅ Successfully logged in with ID: {username_text}\033[0m")
>>>>>>> 1c38537 (Updated main.py)

    my_asba = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="sideBar"]/nav/ul/li[8]/a'))
    )
    my_asba.click()
    
    ipo_elements = WebDriverWait(driver, 10).until(     # Get all IPO elements
        EC.presence_of_all_elements_located((By.XPATH, "//div[@class='company-list']"))
    )
      
    print("Available IPOs:")    # Display IPOs with numbers
    for i, ipo in enumerate(ipo_elements):
        company_name = ipo.find_element(By.XPATH, ".//span[@tooltip='Company Name']").text
        issue_details = ipo.find_element(By.XPATH, ".//span[@tooltip='Sub Group']").text
        share_type = ipo.find_element(By.XPATH, ".//span[@class='share-of-type']").text
        print(f"{i+1}. {company_name} ({issue_details}) - {share_type}")  # Display index, company name, and issue type


    
    while True:  # Loop until valid input
        try:
            choice = int(input("Enter the number of the IPO you want to apply for: "))
            if 1 <= choice <= len(ipo_elements):
                break  # Valid input, exit loop
            else:
                print("Invalid choice. Please enter a number from the list.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    
    selected_ipo = ipo_elements[choice - 1] # Click the selected IPO
    
    apply_button = selected_ipo.find_element(By.XPATH, './/button[contains(@class, "btn-issue")]')
    apply_button.click()

    print(f" Selected IPO is: {company_name}")

    bank_dropdown = WebDriverWait(driver, 10).until(        #click on bank dropdown
        EC.element_to_be_clickable((By.XPATH, '//*[@id="selectBank"]'))
    )
    bank_dropdown.click()

    bank_select = WebDriverWait(driver, 10).until(        #click to select bank
        EC.element_to_be_clickable((By.XPATH, '//*[@id="selectBank"]/option[2]'))
    )
    bank_select.click()

    account_number_dropdown = WebDriverWait(driver, 10).until(        #click on account number dropdown
        EC.element_to_be_clickable((By.XPATH, '//*[@id="accountNumber"]'))
    )
    account_number_dropdown.click()

    account_number_select = WebDriverWait(driver, 10).until(        #click to select account number
        EC.element_to_be_clickable((By.XPATH, '//*[@id="accountNumber"]/option[2]'))
    )
    account_number_select.click()

    ipo_quantity_select = WebDriverWait(driver, 10).until(        #click on ipo quantity
        EC.element_to_be_clickable((By.XPATH, '//*[@id="appliedKitta"]'))
    )
    ipo_quantity_select.send_keys(quantity)

    crn_select = WebDriverWait(driver, 10).until(        #click on crn quantity
        EC.element_to_be_clickable((By.XPATH, '//*[@id="crnNumber"]'))
    )
    crn_select.send_keys(crn_text)
    
    checkbox = WebDriverWait(driver, 10).until(        #click on checkbox
        EC.element_to_be_clickable((By.XPATH, '//*[@id="disclaimer"]'))
    )
    checkbox.click()

    proceed = WebDriverWait(driver, 10).until(        #click on proceed
        EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/div/app-issue/div/wizard/div/wizard-step[1]/form/div[2]/div/div[5]/div[2]/div/button[1]'))
    )
    proceed.click()

    pin_select = WebDriverWait(driver, 10).until(        #click on pin select
        EC.element_to_be_clickable((By.XPATH, '//*[@id="transactionPIN"]'))
    )
    pin_select.send_keys(pin_text)

<<<<<<< HEAD
    final_apply = WebDriverWait(driver, 10).until(        #click on final apply
        EC.element_to_be_clickable((By.XPATH, '//*[@id="transactionPIN"] //*[@id="main"]/div/app-issue/div/wizard/div/wizard-step[2]/div[2]/div/form/div[2]/div/div/div/button[1]'))
    )
    final_apply.click()

    print(f"✅ Successfully applied for {company_name} IPO with {quantity} kitta for {username_text}")
=======
    final_apply = WebDriverWait(driver, 10).until(        #click on final apply //*[@id="main"]/div/app-issue/div/wizard/div/wizard-step[2]/div[2]/div/form/div[2]/div/div/div/button[1]
       EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/div/app-issue/div/wizard/div/wizard-step[2]/div[2]/div/form/div[2]/div/div/div/button[1]'))
    )
    final_apply.click()

    #print(f"✅ Successfully applied for {company_name} IPO with {quantity} kitta for {username_text}")
    print(f"\033[92m✅ Successfully applied for {company_name} IPO with {quantity} kitta for {username_text}\033[0m")
>>>>>>> 1c38537 (Updated main.py)
    
    logout = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-dashboard/header/div[2]/div/div/div/ul/li[1]'))
    )
    logout.click()
    wait = WebDriverWait(driver, 10)
driver.quit()
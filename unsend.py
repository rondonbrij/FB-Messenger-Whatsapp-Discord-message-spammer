import platform
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Path to Chrome WebDriver executable
chrome_driver_path = "chromedriver.exe"

# Delay between actions (in seconds)
DELAY = 5

# Chat URL
chat_url = "https://www.messenger.com/e2ee/t/7286582084744021"

# Main function
def remove_messages():
    print("Opening Chrome")
    if platform.system() == "Windows":
        chrome_options = Options()
        chrome_options.add_argument("user-data-dir=C:/Users/CUSTOMER/AppData/Local/Google/Chrome/User Data/")  # Replace with the actual path
        # Add proxy settings if needed
        # chrome_options.add_argument('--proxy-server=http://proxy:port')
        service = Service(chrome_driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
    else:
        driver = webdriver.Chrome()

    # Navigate to the chat URL using JavaScript injection
    driver.execute_script(f"window.location.href = '{chat_url}';")
    time.sleep(DELAY)  # Wait for the page to load

    # Add your logic here for removing messages
    try:
        while True:
            # Wait for the "More" button to be present
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[aria-label='More']")))
            element = driver.find_element(By.CSS_SELECTOR, "[aria-label='More']")
            actions = webdriver.ActionChains(driver)
            actions.move_to_element(element).perform()
            time.sleep(DELAY)
            element = driver.find_element(By.XPATH, "//span[text()='Remove']")
            element.click()
            time.sleep(DELAY)
            element = driver.find_element(By.CSS_SELECTOR, "[aria-label='Delete']")
            element.click()
            time.sleep(DELAY)
    except Exception as e:
        print("Error:", e)

    driver.quit()

if __name__ == "__main__":
    remove_messages()

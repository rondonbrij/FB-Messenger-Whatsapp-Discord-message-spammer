from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import settings
import platform
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

def start_unsend():
    # Checks if on Mac or Windows
    print("Opening Chrome")
    if platform.system() == "Windows":
        chrome_options = Options()
        chrome_options.add_argument("user-data-dir=C:/Users/CUSTOMER/AppData/Local/Google/Chrome/User Data/")  # Replace with the actual path
        service = Service('chromedriver.exe')
        driver = webdriver.Chrome(service=service, options=chrome_options)
    else:
        driver = webdriver.Chrome()

    # Opens Facebook Messenger
    print("Navigating to Messenger....")
    try:
        driver.get('https://www.messenger.com/')
    except WebDriverException as e:
        print(f"Error navigating to Messenger: {e}")
        driver.quit()
        return

    sleep(5)

    # Waits for the page to load
    wait = WebDriverWait(driver, 20)  # Increased wait time

    # Finds user in DM list
    try:
        print(f"Looking for friend: {settings.friend_name}")
        friend_name_xpath = f"//span[contains(text(), '{settings.friend_name}')]"
        friend_name_element = wait.until(EC.presence_of_element_located((By.XPATH, friend_name_xpath)))
        friend_name_element.click()
    except TimeoutException as e:
        print(f"Error finding friend: {e}")
        driver.quit()
        return

    driver.refresh()
    sleep(5)

    # Start unsending messages
    print("Starting to unsend messages...")

    try:
        # Locate messages sent by you
        your_messages_xpath = "//div[contains(@data-testid, 'message-out')]"
        your_messages = wait.until(EC.presence_of_all_elements_located((By.XPATH, your_messages_xpath)))

        print(f"Found {len(your_messages)} messages to unsend.")
        
        for message in your_messages:
            try:
                # Right-click on the message
                actions = ActionChains(driver)
                actions.context_click(message).perform()
                sleep(1)

                # Find and click the "Remove" option
                remove_option_xpath = "//span[text()='Remove' or text()='Delete']"  # Updated to include 'Delete'
                remove_option = wait.until(EC.presence_of_element_located((By.XPATH, remove_option_xpath)))
                remove_option.click()
                sleep(1)

                # Click the "Unsend for Everyone" button
                unsend_button_xpath = "//span[text()='Unsend for Everyone' or text()='Unsend']"  # Updated to include 'Unsend'
                unsend_button = wait.until(EC.presence_of_element_located((By.XPATH, unsend_button_xpath)))
                unsend_button.click()
                sleep(1)

                print("Message unsent")
            except Exception as e:
                print(f"Error unsending message: {e}")

    except TimeoutException as e:
        print(f"Error locating your messages: {e}")

    # Close the browser
    driver.quit()

# Example usage:
if __name__ == "__main__":
    start_unsend()

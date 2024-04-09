from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time



def initialize_driver():
    # Initialize and return a new WebDriver instance
    return webdriver.Chrome()

def url_matches_pattern(driver, pattern):
    return re.search(pattern, driver.current_url) is not None

def run_test_case(test_case_function):
    driver = initialize_driver()
    try:
        test_case_function(driver)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

def test_case_1(driver):
    driver.get("https://www.united.com/en-us/flights-from-chicago")
    search_box = driver.find_element(By.ID, "flights-booking-id-2-input")
    search_box.clear()
    search_box.send_keys("San Francisco")
    search_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Search flights')]")
    search_button.click()
    pattern = r"https://www\.united\.com/en/us/fsr/choose-flights\?taxng=1&.*f=ORD&t=SFO.*"

    WebDriverWait(driver, 20).until(lambda driver: url_matches_pattern(driver, pattern))

    recommended_flight_label = driver.find_elements(By.XPATH, "//label[contains(@class, 'atm-c-label') and contains(text(), 'RECOMMENDED FLIGHT')]")
    assert len(recommended_flight_label) > 0, "RECOMMENDED FLIGHT label not found on the results page."
    print("TC1 Passed: Valid city name search executed and RECOMMENDED FLIGHT label found.")

# Running all test cases
run_test_case(test_case_1)

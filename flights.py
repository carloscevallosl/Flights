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

    # Find the search box UI element 
    search_box = driver.find_element(By.ID, "flights-booking-id-2-input")
    search_box.clear()
    search_box.send_keys("San Francisco")
    search_box.send_keys(Keys.ENTER)
    time.sleep(2) 

    search_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Search flights')]")
    search_button.click()

    pattern = r"https://www\.united\.com/en/us/fsr/choose-flights\?taxng=1&.*f=ORD&t=SFO.*"
    WebDriverWait(driver, 20).until(lambda driver: url_matches_pattern(driver, pattern))
    assert url_matches_pattern(driver, pattern), "Final search results page not reached."
    print("Test 1 Passed: Final search results page was successfully reached.")

def test_case_2(driver):
    driver.get("https://www.united.com/en-us/flights-from-chicago")
    search_box = driver.find_element(By.ID, "flights-booking-id-2-input")
    search_box.clear()
    search_box.send_keys("InvalidCity123")
    search_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Search flights')]")
    search_button.click()

    try:
        # Wait for the error message to be visible on the page
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="flights-booking-id-2-error"]')))
        print("Test 2 Passed: Incorrect Destination Location message shown correctly.")
    except:
        print("Test 2 failed, Incorrect Destination Location message not shown.")



def test_case_3(driver):
    driver.get("https://www.united.com/en-us/flights-from-chicago")
    search_box = driver.find_element(By.ID, "flights-booking-id-2-input")
    search_box.clear()
    search_box.send_keys("!@#$%^&*()")
    search_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Search flights')]")
    search_button.click()

    try:
        # Wait for the error message to be visible on the page
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="flights-booking-id-2-error"]')))
        print("Test 3 Passed: Incorrect Destination Location message shown correctly.")
    except:
        print("Test 3 failed, Incorrect Destination Location message not shown.")

def test_case_4(driver):
    driver.get("https://www.united.com/en-us/flights-from-chicago")
    to_box = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "flights-booking-id-2-input")))
    
    # Tab through the page to simulate accessibility
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.TAB)
    
    to_box.send_keys("San Francisco")
    to_box.send_keys(Keys.ENTER)

    search_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Search flights')]")))
    for i in range(4):
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.TAB)
    
    search_button.send_keys(Keys.ENTER)
    
    pattern = r"https://www\.united\.com/en/us/fsr/choose-flights\?taxng=1&.*f=ORD&t=SFO.*"
    WebDriverWait(driver, 20).until(lambda driver: url_matches_pattern(driver, pattern))
    assert url_matches_pattern(driver, pattern), "Final search results page not reached."
    print("Test 4 Passed: Final search results page was successfully reached.")


# Running all test cases
run_test_case(test_case_1)
run_test_case(test_case_2)
run_test_case(test_case_3)
run_test_case(test_case_4)

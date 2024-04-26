from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import os

def check_element_presence(css_selector, description, timeout=10):
    """Check presence of an element with a specific CSS selector."""
    end_time = time.time() + timeout
    results = {}
    while True:
        try:
            element = driver.find_element(By.CSS_SELECTOR, css_selector)
            results[description] = "PASS: Element is present."
            return element, results
        except Exception as e:
            if time.time() > end_time:
                results[description] = f"FAIL: Element is not present - {str(e)}"
                return None, results
        time.sleep(1)

def check_text_in_element(css_selector, expected_text, description):
    """Check if the expected text is in the specified element, handling nested elements."""
    element, results = check_element_presence(css_selector, description)
    if element:
        actual_text = element.get_attribute('innerText')  # This retrieves all text, including nested
        actual_text = " ".join(actual_text.split())  # Normalize whitespace
        print(f"DEBUG: Found text '{actual_text}' in {description}")
        if expected_text in actual_text:
            results[description] += f" | PASS: Contains the text '{expected_text}'."
        else:
            results[description] += f" | FAIL: Does not contain the text '{expected_text}'."
    return results

service = Service(executable_path='./chromedriver-win64/chromedriver.exe')
driver = webdriver.Chrome(service=service)
wait = WebDriverWait(driver, 10)

def test_homelab_page():
    driver.get('http://codesculpt.xyz/homelab')  # Adjust URL as necessary
    all_results = {}

    # Check for header, footer, and logos
    results = check_element_presence('header', 'Header')
    all_results.update(results[1])

    results = check_element_presence('footer', 'Footer')
    all_results.update(results[1])

    results = check_element_presence('.discord-logo', 'Homelab Logo')
    all_results.update(results[1])

    # Checking for titles and services descriptions
    results = check_text_in_element('.homelab-title', 'Agni, A Homelab Setup', 'Homelab Title')
    all_results.update(results)

    # Update the JSON file
    file_path = 'test_results.json'
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            existing_data = json.load(file)
            existing_data['homelab_page'] = all_results
    else:
        existing_data = {'homelab_page': all_results}

    with open(file_path, 'w') as file:
        json.dump(existing_data, file, indent=4)

try:
    test_homelab_page()
finally:
    driver.quit()

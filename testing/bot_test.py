from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
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
    """Check if the expected text is in the specified element."""
    element, results = check_element_presence(css_selector, description)
    if element and expected_text in element.text:
        results[description] += f" | PASS: Contains the text '{expected_text}'."
    else:
        results[description] += f" | FAIL: Does not contain the text '{expected_text}'."
    return results

service = Service(executable_path='./chromedriver-win64/chromedriver.exe')
driver = webdriver.Chrome(service=service)

def test_home_page():
    driver.get('http://codesculpt.xyz/')
    time.sleep(2)
    all_results = {}

    # Check for elements and text
    results = check_element_presence('.page-content', 'Page Content')
    all_results.update(results[1])

    results = check_element_presence('.cyberpunk-button', 'Resume Button')
    all_results.update(results[1])

    results = check_text_in_element('.title', 'Full Stack', 'Page Title')
    all_results.update(results)

    # Manage JSON file for results
    file_path = 'test_results.json'
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            existing_data = json.load(file)
            existing_data['home_page'] = all_results
    else:
        existing_data = {'home_page': all_results}

    with open(file_path, 'w') as file:
        json.dump(existing_data, file, indent=4)

try:
    test_home_page()
finally:
    driver.quit()

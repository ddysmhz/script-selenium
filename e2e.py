import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor

driver = webdriver.Chrome()

gpt_url = "yourdomain.com"

CONCURRENT_INSTANCES = 1
TOTAL_ROUNDS = 5

def process_prompt(prompt):
    driver.get(gpt_url)

    try:
        text_area = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'css_selector'))
        )

        text_area.send_keys(prompt)
        text_area.send_keys(Keys.RETURN)  

        response_indicator = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'css_selector'))
        )

        start_time = time.time()

        WebDriverWait(driver, 20).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, 'css_selector'))
        )

        end_time = time.time()

        response_time = end_time - start_time

        return response_time

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

    finally:
        driver.quit()

def run_prompts():
    prompts = [
        "your_prompt"
    ]
    results = []

    with ThreadPoolExecutor(max_workers=CONCURRENT_INSTANCES) as executor:
        for _ in range(TOTAL_ROUNDS):
            results.extend(executor.map(process_prompt, prompts))

    return [result for result in results if result is not None]

if __name__ == "__main__":
    response_times = run_prompts()

    if response_times:
        average_response_time = sum(response_times) / len(response_times)
        print(f"Response Times: {response_times}")
        print(f"Average Response Time: {average_response_time} seconds")
    else:
        print("No valid responses received.")
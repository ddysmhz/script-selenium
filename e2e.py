import json
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor

driver = webdriver.Chrome()

gpt_url = "yourdomain"

with open("data.txt", "r") as txt_file:
    prompts = txt_file.read().splitlines()

concurrent_requests = 5

max_prompts = 10

def process_prompt(prompt):
    driver.get(gpt_url)

    try:
        text_area = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.css_selector'))
        )

        text_area.send_keys(prompt)
        text_area.send_keys(Keys.RETURN)  

        start_time = time.time()

        time.sleep(2)  

        end_time = time.time()

        
        response_time = end_time - start_time

        return response_time

    finally:
        pass

def run_prompts(prompts):
    results = []
    with ThreadPoolExecutor(max_workers=concurrent_requests) as executor:
        for _ in range(min(len(prompts), max_prompts)):
            prompt = prompts.pop(0)
            future = executor.submit(process_prompt, prompt)
            results.append(future)
    return [future.result() for future in results]

response_times = run_prompts(prompts)

average_response_time = sum(response_times) / len(response_times)

print(f"Response Times: {response_times}")
print(f"Average Response Time: {average_response_time} seconds")

driver.quit()
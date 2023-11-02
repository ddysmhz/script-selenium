import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor

gpt_url = "https://example.com"

# Define the number of concurrent instances and total rounds
CONCURRENT_INSTANCES = 2
TOTAL_ROUNDS = 5

def process_prompt(prompt):
    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(gpt_url)
        text_area = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'css'))
        )

        text_area.send_keys(prompt)
        text_area.send_keys(Keys.RETURN)  

        response_indicator = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'css'))
        )

        start_time = time.time()

        WebDriverWait(driver, 20).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, 'css'))
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
        "Article 51 The following are causes for termination of the employment relationship, without liability for the employee:I. The employer or, as the case may be, the employer's group, when proposing the work, deceived him/her with respect to the conditions thereof. This cause of termination shall cease to have effect after thirty days of rendering services to the employee;II. The employer, his family members or any of his representatives, within the service, in a c t s o f dishonesty or dishonesty, acts of violence, threats, insults, harassment and/or sexual harassment, bad treatment or other similar acts against the employee, spouse, parents, children or siblings;"
    ]
    results = []

    with ThreadPoolExecutor(max_workers=CONCURRENT_INSTANCES) as executor:
        for _ in range(TOTAL_ROUNDS):
            for prompt in prompts:
                result = executor.submit(process_prompt, prompt)
                results.append(result)

    return [result.result() for result in results if result.result() is not None]

if __name__ == "__main__":
    response_times = run_prompts()

    if response_times:
        average_response_time = sum(response_times) / len(response_times)
        print(f"Response Times: {response_times}")
        print(f"Average Response Time: {average_response_time} seconds")
    else:
        print("No valid responses received.")
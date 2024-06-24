
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Setup WebDriver
driver = webdriver.Chrome()

try:
    # Open the first page
    driver.get("http://127.0.0.1:8090/")
    time.sleep(2)

    # Find elements and interact with them
    username_input = driver.find_element(By.ID, "username")
    username_input.send_keys("admin")
    time.sleep(1)

    password_input = driver.find_element(By.ID, "password")
    password_input.send_keys("admin123")
    time.sleep(1)

    login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    login_button.click()
    time.sleep(2)

    # Open the second page
    driver.get("http://127.0.0.1:8090/data_entry.html")
    time.sleep(2)

    # Find elements and interact with them
    regd_input = driver.find_element(By.ID, "data1")
    regd_input.send_keys("123456")
    time.sleep(1)

    sem_input = driver.find_element(By.ID, "data2")
    sem_input.send_keys("Spring 2022")
    time.sleep(1)

    submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    submit_button.click()
    time.sleep(2)

except Exception as e:
    print(e)

finally:
    # Close the browser
    driver.quit()

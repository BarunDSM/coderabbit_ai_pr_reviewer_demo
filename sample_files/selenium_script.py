from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize the WebDriver
driver = webdriver.Chrome()

try:
    # Open the first page
    url1 = "http://127.0.0.1:8090/"
    driver.get(url1)

    # Wait until the username input is present and interact with it
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "username"))
    ).send_keys("admin")

    # Interact with the password input
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "password"))
    ).send_keys("password")

    # Click the login button
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
    ).click()

    # Wait for the next page to load (if necessary)
    WebDriverWait(driver, 10).until(
        EC.url_changes(url1)
    )

    # Open the second page
    url2 = "http://127.0.0.1:8090/data_entry.html"
    driver.get(url2)

    # Interact with the regd_input field
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "data1"))
    ).send_keys("123456")

    # Interact with the sem_input field
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "data2"))
    ).send_keys("Spring 2022")

    # Click the submit button
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
    ).click()

    # Optionally, wait for some confirmation or result after submitting the form
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "success_message"))  # Adjust the locator as per your page
    )

except Exception as e:
    print(e)

finally:
    # Close the WebDriver
    driver.quit()

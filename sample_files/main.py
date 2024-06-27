import os
import time
import logging
import requests
from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from requests.exceptions import RequestException
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from utils import sanitize_output, read_urls, html_scrapper
from sys_prompts import system_prompt
from logs.logger import logger  # Assuming this is a custom logger instance

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Fetch API key
api_key = os.getenv('OPENAI_API_KEY')

if not api_key:
    logger.error("OPENAI_API_KEY environment variable not found")
    raise EnvironmentError("OPENAI_API_KEY environment variable not found")

# Initialize OpenAI Chat model
llm = ChatOpenAI(temperature=0.8, api_key=api_key)

def get_webdriver():
    """
    Initialize Chrome WebDriver using WebDriver Manager.
    """
    try:
        return webdriver.Chrome(ChromeDriverManager().install())
    except WebDriverException as e:
        logger.error(f"Failed to initialize WebDriver: {e}")
        raise

def check_chain_interactions(chain_results, urls):
    """
    Check interactions with Selenium WebDriver.

    Args:
        chain_results (list): Results from the chain execution.
        urls (list): List of URLs to check.

    Returns:
        bool: True if all interactions are successful, False otherwise.
    """
    for url in urls:
        try:
            driver = get_webdriver()
            driver.get(url)
            for result in chain_results:
                try:
                    element = driver.find_element(By.XPATH, f"//*[contains(text(), '{result}')]")
                except NoSuchElementException:
                    logger.error(f"Element {result} not found on the webpage {url}")
                    driver.quit()
                    return False
            driver.quit()
        except WebDriverException as e:
            logger.error(f"Selenium WebDriver error: {e}")
            return False
    return True

def execute_chain(urls, max_attempts=5, attempt=1):
    """
    Execute the chain process with retries.

    Args:
        urls (list): List of URLs to process.
        max_attempts (int): Maximum number of attempts.
        attempt (int): Current attempt number.
    """
    if attempt > max_attempts:
        logger.error("Max attempts reached. Exiting.")
        return

    try:
        response = requests.get(urls[0])
        response.raise_for_status()

        logger.info("Starting chain execution...")
        chain_results = llm.invoke({"urls": read_urls(urls)})  # Assuming llm.invoke is the correct call
        time.sleep(2)
        logger.info("Chain execution successful.")

        if not check_chain_interactions(chain_results, urls):
            raise RuntimeError("Selenium process did not execute properly")

    except (RequestException, ValueError, RuntimeError) as e:
        logger.error(f"Error occurred: {e}")
        logger.info(f"Retrying... Attempt {attempt}/{max_attempts}")
        time.sleep(3)
        execute_chain(urls, max_attempts, attempt + 1)

if __name__ == '__main__':
    urls = ["http://example.com"]  # Replace with actual URLs
    execute_chain(urls)

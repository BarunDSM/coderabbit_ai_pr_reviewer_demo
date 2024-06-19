# Utility functions
from langchain_community.document_loaders import AsyncChromiumLoader, AsyncHtmlLoader
from configs.read_config import Read_Configs

def sanitize_output(text: str) -> str:
    """
    Sanitizes the output by extracting the Python code block content.

    Args:
        text (str): Response text containing Python code block.

    Returns:
        str: Sanitized Python code from the text.
    """
    _, after = text.split("```python")
    return after.split("```")[0]


def read_urls(list_of_urls: list) -> str:
    """
    Converts a list of URLs into a comma-separated string.

    Args:
        list_of_urls (list): List of URLs.

    Returns:
        str: Comma-separated string of URLs.
    """
    return ", ".join(list_of_urls)


def html_scraper(urls: list) -> str:
    """
    Scrapes HTML content from multiple URLs.

    Args:
        urls (list): List of URLs to scrape.

    Returns:
        str: Combined HTML content from all URLs separated by '#next page'.
    """
    src = []
    loader = AsyncHtmlLoader(urls)
    docs = loader.load()
    for doc in docs:
        src.append(doc.page_content)
    return '\n#next page\n'.join(src)


def html_scraper_for_liveserver(urls: list) -> str:
    """
    Scrapes HTML content from multiple URLs using a live server.

    Args:
        urls (list): List of URLs to scrape.

    Returns:
        str: Combined HTML content from all URLs with live server comments removed,
             separated by '#next page'.
    """
    combined = []
    for url in urls:
        loader = AsyncChromiumLoader(urls)
        html = loader.load()
        src = (html[0].page_content).split("<!-- Code injected by live-server -->")[0]
        combined.append(''.join(src))
    return '\n#next page\n'.join(combined)


def html_file_reader(file_paths: list) -> str:
    """
    Reads content from multiple HTML files and concatenates their content.

    Args:
        file_paths (list): List of file paths to HTML files.

    Returns:
        str: Combined content of all HTML files separated by '#next page'.
    """
    combined_contents = []
    for file_path in file_paths:
        try:
            with open(file_path, 'r') as file:
                file_contents = file.read()
                combined_contents.append(file_contents)
        except FileNotFoundError:
            print(f"File '{file_path}' not found.")
        except Exception as e:
            print(f"Error occurred while reading file '{file_path}': {e}")

    return '\n#next page\n\n'.join(combined_contents)

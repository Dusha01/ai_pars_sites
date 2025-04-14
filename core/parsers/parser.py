from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HtmlParser:
    @staticmethod
    def parse(url: str, timeout: int = 10000) -> str:
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page()
                page.goto(url, timeout=timeout)
                content = page.content()
                browser.close()

                soup = BeautifulSoup(content, 'html.parser')

                for el in soup.find_all(['script', 'style', 'nav', 'footer', 'header', 'aside']):
                    el.decompose()

                return ' '.join(soup.stripped_strings)
        except Exception as e:
            logger.error(f"Error parsing URL {url}: {e}")
            return ""


if __name__ == "__main__":
    url = "https://pypi.org/project/lxml/"
    text_content = HtmlParser.parse(url)
    print(text_content)
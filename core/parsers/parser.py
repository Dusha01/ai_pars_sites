from bs4 import BeautifulSoup
import requests
class HTMLParser:
    def __init__(self, url):
        self.url = url
        self.html = self.fetch_html(url)
        self.soup = self.clean_html(self.html)
    def fetch_html(self, url):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # Проверка на ошибки HTTP
            return response.text
        except requests.RequestException as e:
            print(f"Ошибка при загрузке страницы: {e}")
            return None
    def clean_html(self, html):
        if not html:
            return None

        soup = BeautifulSoup(html, 'lxml')
        for element in soup.select('header, footer, nav, aside, [class*="ad"], [id*="ad"], .navbar, .menu, .sidebar'):
            element.decompose()
        return soup.find('main') or soup.body

    def get_text(self):
        if not self.soup:
            return "HTML-код не был загружен или очищен."

        return self.soup.get_text(separator='\n', strip=True)
if __name__ == "__main__":
    url = "https://ru.wikipedia.org/wiki/Список_серий_аниме_One_Piece"
    parser = HTMLParser(url)
    clean_text = parser.get_text()

    if clean_text and clean_text != "HTML-код не был загружен или очищен.":
        print(clean_text)

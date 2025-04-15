import requests
from bs4 import BeautifulSoup

class Parser:
    def __init__(self, url):
        self.url = url
        self.soup = None
    def fetch_html(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            self.html = response.text
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при получении HTML: {e}")
            self.html = None
    def remove_elements(self):
        if self.soup:
            for selector in ["footer", "#footer", ".footer", "nav", "#nav", ".nav", "script", "#script", ".script", "style", "#style", ".style"]:
                for element in self.soup.select(selector):
                    element.decompose()

    def parse(self):
        self.fetch_html()
        if self.html is None:
            return None

        self.soup = BeautifulSoup(self.html, 'html.parser')
        self.remove_elements()
        text = self.soup.get_text(separator='\n', strip=True)
        return text

if __name__ == '__main__':
    url = "https://ru.wikipedia.org/wiki/Хорватия"
    parser = Parser(url)
    text = parser.parse()

    if text:
        print("Извлеченный текст:\n")
        print(text)
    else:
        print("Не удалось извлечь текст.")
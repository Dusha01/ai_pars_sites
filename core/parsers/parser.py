from bs4 import BeautifulSoup
import requests
import os
from urllib.parse import urljoin
import json

class HTMLParser:
    def __init__(self, url):
        self.url = url
        self.html = self.fetch_html(url)
        self.soup = self.clean_html(self.html) if self.html else None
        
        # Временные хранилища данных
        self.temp_data = {
            'main_text': None,
            'tables': [],
            'images': [],
            'documents': []
        }

    def fetch_html(self, url):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Ошибка при загрузке страницы: {e}")
            return None
        
    def clean_html(self, html):
        soup = BeautifulSoup(html, 'lxml')
        for element in soup.select('header, footer, nav, aside, [class*="ad"], [id*="ad"], .navbar, .menu, .sidebar'):
            element.decompose()
        return soup.find('main') or soup.body

    def extract_main_text(self):
        """Извлечение основного текста страницы"""
        if self.soup:
            self.temp_data['main_text'] = self.soup.get_text(separator='\n', strip=True)

    def extract_tables(self):
        """Извлекает таблицы во временное хранилище"""
        if not self.soup:
            return

        for table in self.soup.find_all('table'):
            table_data = []
            headers = [th.get_text(strip=True) for th in table.find_all('th')]
            if headers:
                table_data.append(headers)
            
            for row in table.find_all('tr'):
                cells = [td.get_text(strip=True) for td in row.find_all('td')]
                if cells:
                    table_data.append(cells)
            
            self.temp_data['tables'].append(table_data)
            
    def extract_images(self):
        if not self.soup:
            return
        
        for img in self.soup.find_all('img'):
            img_src = img.get('src')
            if img_src:
                self.temp_data['images'].append({
                    'url': urljoin(self.url, img_src),
                    'alt': img.get('alt', ''),
                    'title': img.get('title', ''),
                    'dimensions': (img.get('width'), img.get('height'))
                })

    def extract_documents(self):
        """Извлекает ссылки на документы во временное хранилище"""
        if not self.soup:
            return

        for a in self.soup.find_all('a', href=True):
            href = a['href'].lower()
            if href.endswith(('.pdf', '.json')):
                self.temp_data['documents'].append({
                    'url': urljoin(self.url, a['href']),
                    'type': 'pdf' if href.endswith('.pdf') else 'json',
                    'title': a.get_text(strip=True) or f"Документ {len(self.temp_data['documents']) + 1}"
                })
                
    def collect_all_data(self):
        """Основной метод сбора данных во временное хранилище"""
        if not self.soup:
            return False

        self.extract_main_text()
        self.extract_tables()
        self.extract_images()
        self.extract_documents()
        return True

    def get_raw_data(self):
        """Возвращает собранные данные для последующей обработки"""
        return self.temp_data

    def get_structured_data(self):
        """Возвращает данные в структурированном формате"""
        return {
            'source_url': self.url,
            'content': {
                'text': self.temp_data['main_text'],
                'elements': {
                    'tables_count': len(self.temp_data['tables']),
                    'images_count': len(self.temp_data['images']),
                    'documents_count': len(self.temp_data['documents'])
                },
                'tables': self.temp_data['tables'],
                'images': self.temp_data['images'],
                'documents': self.temp_data['documents']
            }
        }
        
if __name__ == "__main__":
    url = "https://dvgups.ru/"
    parser = HTMLParser(url)
    
    if parser.collect_all_data():
        raw_data = parser.get_raw_data()
        structured_data = parser.get_structured_data()
        
        # Пример структуры собранных данных
        print("Основной текст")
        print(f"Основной текст ({len(raw_data['main_text'])} символов):")
        print(raw_data['main_text'])
        
        print("=== Собранные таблицы ===")
        for i, table in enumerate(raw_data['tables'], 1):
            print(f"Таблица {i}: {len(table)} строк")
        
        print("\n=== Собранные изображения ===")
        for i, img in enumerate(raw_data['images'], 1):
            print(f"Изображение {i}: {img['url']}")
            
        print("\n=== Собранные документы ===")
        for i, doc in enumerate(raw_data['documents'], 1):
            print(f"Документ {i}: {doc['type']} - {doc['url']}")
    else:
        print("Не удалось собрать данные")

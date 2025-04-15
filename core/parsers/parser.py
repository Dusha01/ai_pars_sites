# core/parsers/advanced_parser.py
from lxml import html
import requests
from urllib.parse import urljoin
import logging
from typing import Dict, List, Optional
import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AdvancedParser:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def parse_page(self, url: str) -> Optional[Dict]:
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            tree = html.fromstring(response.content)
            
            result = {
                'text_content': self._extract_text(tree),
                'images': self._extract_images(tree, url),
                'tables': self._extract_tables(tree),
                'files': self._extract_files(tree, url),
                'links': self._extract_links(tree, url)
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Error parsing {url}: {str(e)}")
            return None

    def _extract_text(self, tree) -> str:
        for elem in tree.xpath('//script|//style|//nav|//footer|//header|//aside'):
            elem.drop_tree()
            
        text = ' '.join(tree.xpath('//text()[normalize-space()]')).strip()
        return text

    def _extract_images(self, tree, base_url) -> List[Dict]:
        images = []
        for img in tree.xpath('//img'):
            src = img.get('src', '').strip()
            if src:
                full_url = urljoin(base_url, src)
                images.append({
                    'url': full_url,
                    'alt': img.get('alt', ''),
                    'width': img.get('width'),
                    'height': img.get('height')
                })
        return images

    def _extract_tables(self, tree) -> List[Dict]:
        tables = []
        for table in tree.xpath('//table'):
            try:
                df = pd.read_html(html.tostring(table))[0]
                tables.append({
                    'html': html.tostring(table, encoding='unicode'),
                    'data': df.to_dict('records')
                })
            except:
                continue
        return tables

    def _extract_files(self, tree, base_url) -> List[Dict]:
        file_types = ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx']
        files = []
        
        for link in tree.xpath('//a[@href]'):
            href = link.get('href', '').strip()
            if any(href.lower().endswith(ext) for ext in file_types):
                full_url = urljoin(base_url, href)
                files.append({
                    'url': full_url,
                    'text': link.text_content().strip(),
                    'type': href.split('.')[-1].lower()
                })
        return files

    def _extract_links(self, tree, base_url) -> List[Dict]:
        links = []
        for link in tree.xpath('//a[@href]'):
            href = link.get('href', '').strip()
            if href.startswith(('http://', 'https://')):
                links.append({
                    'url': href,
                    'text': link.text_content().strip(),
                    'is_external': not href.startswith(self.base_url)
                })
        return links
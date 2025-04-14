# services/batch_processor.py
import json
from typing import List, Dict, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

from core.parsers.parser import AdvancedParser
from core.ai.llm_handlers import LLMHandler

class BatchProcessor:
    def __init__(self):
        self.llm = LLMHandler()
    
    def load_input(self, filepath: str) -> Dict:
        with open(filepath, "r", encoding='utf-8') as f:
            return json.load(f)
        
    def process_from_file(self, input_file: str) -> None:
        data = self.load_input(input_file)
        results = self.process_batch(data['sites'], data['question'])
        self.print_results(results)

    def process_batch(self, urls: List[str], question: str) -> List[Dict]:
        results = []
        
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = []
            
            for url in urls:
                parser = AdvancedParser(url) 
                futures.append(
                    executor.submit(
                        self.process_single,
                        parser,
                        url,
                        question
                    )
                )
            
            for future in as_completed(futures):
                result = future.result()
                if result:
                    results.append(result)
            
        return results
        
    def process_single(self, parser: AdvancedParser, url: str, question: str) -> Optional[Dict]:
        try:
            parsed_data = parser.parse_page(url)
            if not parsed_data or not parsed_data['text_content']:
                print(f'Не удалось загрузить {url}')
                return None
            
            answer = self.llm.generate_answer(parsed_data['text_content'], question)
            
            return {
                "url": url,
                'question': question,
                'answer': answer.strip(),
                'metadata': {
                    'images_count': len(parsed_data['images']),
                    'tables_count': len(parsed_data['tables']),
                    'files_count': len(parsed_data['files'])
                }
            }
        except Exception as e:
            print(f'Ошибка при обработке {url}: {str(e)}')
            return None
    
    def print_results(self, results: List[Dict]) -> None:
        print('\n== Результаты ==')
        for item in results:
            print(f'\nСайт: {item["url"]}')
            print(f'Вопрос: {item["question"]}')
            print(f'Ответ: {item["answer"]}')
            print(f'Метаданные: {item["metadata"]}')
            print("-"*50)
# core/ai/llm_handlers.py
from openai import OpenAI
from config.settings import Setting
import time
from typing import Dict, Any

class LLMHandler:
    def __init__(self):
        if not Setting.API.DEEPSEEK:
            raise ValueError("API key not provided")
        
        self.client = OpenAI(
            api_key=Setting.API.DEEPSEEK,
            base_url=Setting.BASE_URL
        )
        
    def generate_answer(self, context: str, question: str, metadata: Dict[str, Any] = None) -> str:
        if not context:
            return 'Не удалось загрузить содержимое'

        start_time = time.time()

        try:
            prompt = (
                f"Контекст: {context[:3000]}\n\n"
                f"Метаданные: {str(metadata)}\n\n"
                f"Вопрос: {question}\n\n"
                "Ответ:"
            )
            
            response = self.client.chat.completions.create(
                model=Setting.LLM_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.4,
                max_tokens=Setting.MAX_TOKENS
            )
            
            result = response.choices[0].message.content
            return result if result else "Информация отсутствует"
        
        except Exception as e: 
            print(f"Error in AI: {str(e)}")
            return f"Error: {str(e)}"
        
        finally:
            elapsed = time.time() - start_time
            if elapsed > 10:
                print(f"Запрос выполняется {elapsed:.2f} сек")
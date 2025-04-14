from dotenv import load_dotenv
import os

load_dotenv()

class Setting:
    LLM_MODEL = "deepseek-chat-v3-0324"
    MAX_TOKENS = 3000
    CACHE_SIZE = 5
    BASE_URL = "https://llm.drakesoft.ru/api/v1"

    class API:
        DEEPSEEK = os.getenv("DEEPSEEK_API_KEY") 
    
from dotenv import load_dotenv
import os

load_dotenv()

class Setting:
    LLM_MODEL = "gpt-4o-mini"
    MAX_TOKENS = 1000
    CACHE_SIZE = 5
    BASE_URL = "https://api.aitunnel.ru/v1/"

    class API:
        AI = os.getenv("API_KEY")
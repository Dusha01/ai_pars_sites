from dotenv import load_dotenv
import os

class Setting:
    LLM_MODEL = "deepseek-chat-v3-0324"
    MAX_TOKENS = 3000
    REQUEST_TIMEOUT = 10
    CACHE_SIZE = 5

    class API:
        DEEPSEEK = os.getenv("DEEPSEEK_API_KEY")

    class URL:
        BASE_URL = os.getenv("BASE_URL")
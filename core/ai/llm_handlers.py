from openai import OpenAI
from config.settings import Setting

client = OpenAI(
    api_key=Setting.API.DEEPSEEK
    base_url=Setting.URL.BASE_URL
)
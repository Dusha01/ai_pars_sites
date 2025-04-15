from openai import OpenAI

# Инициализация клиента (API ключ можно задать здесь или через переменную окружения)
client = OpenAI(api_key="ваш_api_ключ_openai")

def ask_gpt(prompt, model="gpt-4-turbo"):  # или "gpt-3.5-turbo"
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Ошибка: {str(e)}"

# Пример использования
question = "Кратко опиши сюжет аниме 'One Piece'"
answer = ask_gpt(question)
print(answer)
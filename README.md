# Запуск кода
Для запуска кода в setting.py следует указать языковую модель
Также в .env указать ключ 

# Запрос
Форма запроса реализована в JSON документе:
    В массив с sites пишутся ссылки на сайты
    В массив с question пишутся вопросы

# Запуск программы
1) Установка зависимостей pip install pip.txt
2) Точка входа в программу main.py. Из корня дирриктории python main.py
# AI-Powered Website Parser

A Python tool for parsing websites using AI techniques to extract and process data efficiently.

## Features
- Web scraping with AI-enhanced data extraction
- Support for dynamic content (JavaScript-rendered pages)
- Customizable parsing rules
- Data cleaning and transformation
- Export to multiple formats (CSV, JSON, etc.)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Dusha01/ai_pars_sites.git
cd ai_pars_sites

2. Install dependencies:
pip install -r pip.txt


Usage
Basic example:

python .\main.py
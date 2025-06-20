# Conway's Game of Life

Учебный проект Flask, реализующий клеточный автомат "Игра Жизнь"

## Запуск проекта

1. Создайте виртуальное окружение:
   ```bash
   python -m venv .venv
   ```

2. Активируйте окружение:
   ```bash
   # Windows
   .venv\Scripts\activate
   
   # macOS/Linux
   source .venv/bin/activate
   ```

3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

4. Запустите приложение:
   ```bash
   flask run
   ```

5. Откройте в браузере: http://127.0.0.1:5000

## Структура проекта
```
├── .venv/          # Виртуальное окружение (не коммитится)
├── .gitignore
├── README.md        # Этот файл
├── app.py           # Главный файл приложения
├── requirements.txt # Зависимости
├── static/
│   └── styles.css   # Стили
└── templates/       # HTML-шаблоны
    ├── base.html
    ├── index.html
    └── live.html
```

## Технологии
- Python 3.12
- Flask 3.1
- HTML5/CSS3
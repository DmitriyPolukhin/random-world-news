# Random World News 🌍

> Telegram Mini App для получения случайных новостей со всего мира с переводом на русский

![Random World News](https://img.shields.io/badge/Telegram-Mini_App-blue?logo=telegram)
![Python](https://img.shields.io/badge/Python-3.11+-green?logo=python)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Особенности

- 🎲 **Максимальная рандомность** — новости из 200+ стран на 40+ языках
- 🇯🇵🇧🇷🇩🇪 **Со всего мира** — Япония, Бразилия, Мексика, Германия, Малайзия...
- 🌐 **Автоперевод** — все новости переводятся на русский (DeepL/Google)
- 🎨 **iOS-like дизайн** — Liquid Glass эффект, плавные анимации
- 📊 **Статистика** — счётчик прочитанных новостей и посещённых стран

## 🚀 Быстрый старт

### 1. Клонирование

```bash
cd /Users/dmitriypoluhin/ai-coding-framework/random-world-news
```

### 2. Установка зависимостей

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

### 3. Настройка

Скопируй `.env.example` в `.env` и заполни API ключи:

```bash
cp ../.env.example ../.env
```

Получи бесплатные ключи:
- **GNews**: https://gnews.io (100 req/day)
- **WorldNewsAPI**: https://worldnewsapi.com (100 req/day)
- **Telegram Bot**: @BotFather в Telegram

### 4. Запуск

**Backend (API сервер):**
```bash
cd backend
python main.py
# Сервер запустится на http://localhost:8000
```

**Telegram Bot:**
```bash
cd bot
python telegram_bot.py
```

**Webapp (для разработки):**
```bash
# Открой webapp/index.html в браузере
# Или используй Live Server в VS Code
```

## 📁 Структура проекта

```
random-world-news/
├── backend/
│   ├── main.py              # FastAPI сервер
│   ├── news_fetcher.py      # Агрегатор новостей (рандомизация)
│   ├── translator.py        # Модуль перевода (DeepL/Google)
│   ├── country_data.py      # Флаги и названия стран
│   └── requirements.txt     # Python зависимости
├── webapp/
│   ├── index.html           # Telegram Mini App
│   ├── styles.css           # Liquid Glass стили
│   └── app.js               # Логика приложения
├── bot/
│   └── telegram_bot.py      # Telegram бот
├── .env.example             # Шаблон переменных окружения
└── README.md
```

## 🔑 API эндпоинты

| Endpoint | Method | Описание |
|----------|--------|----------|
| `/` | GET | Информация об API |
| `/api/health` | GET | Health check |
| `/api/random-news` | GET | Получить случайную новость |
| `/api/stats` | GET | Глобальная статистика |

### Пример ответа `/api/random-news`:

```json
{
  "success": true,
  "news": {
    "title": "Переведённый заголовок",
    "description": "Переведённое описание...",
    "url": "https://source.com/article",
    "image": "https://...",
    "source": "Tokyo News"
  },
  "metadata": {
    "country": {
      "flag": "🇯🇵",
      "name": "Япония"
    },
    "language": {
      "code": "ja",
      "name": "Японский"
    }
  }
}
```

## 🎨 Дизайн

Приложение использует **Liquid Glass** эффект в стиле iOS 18:

- `backdrop-filter: blur(20px) saturate(180%)`
- Градиентный фон с мягкими переходами
- Плавные анимации (slide up, pulse, spin)
- Поддержка светлой и тёмной темы Telegram

## 🛠️ Деплой

### Вариант 1: Railway (рекомендуется)

1. Создай проект на [railway.app](https://railway.app)
2. Подключи GitHub репозиторий
3. Добавь переменные окружения
4. Backend задеплоится автоматически

### Вариант 2: Render

1. Создай Web Service на [render.com](https://render.com)
2. Укажи `backend/` как корневую директорию
3. Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Вариант 3: VPS

```bash
# Nginx + Gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## 📄 Лицензия

MIT License

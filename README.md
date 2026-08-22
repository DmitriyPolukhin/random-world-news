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
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Настройка

Скопируй `.env.example` в `.env`:

```bash
cp .env.example .env
```

Для локального WebApp ключи новостных API не нужны: приложение использует RSS. Необязательные GNews, NewsAPI, WorldNewsAPI и DeepL можно подключить позже.

Для запуска Telegram-бота отдельно укажи:

- `TELEGRAM_BOT_TOKEN` — новый токен от @BotFather;
- `WEBAPP_URL` — `http://localhost:8000/app/` для браузерной проверки или публичный HTTPS URL для Telegram.

Файл `.env` локальный и игнорируется Git. Никогда не добавляй его в коммиты.

### 4. Запуск

**Backend (API сервер):**
```bash
source venv/bin/activate
python backend/main.py
# WebApp: http://localhost:8000/app/
# API health: http://localhost:8000/api/health
```

**Telegram Bot:**
```bash
source venv/bin/activate
python -m bot.telegram_bot
```

**Проверка:**
```bash
source venv/bin/activate
python -m unittest discover -s tests -v
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
| `/` | GET | Переход в Mini App |
| `/app/` | GET | Mini App |
| `/api` | GET | Информация об API |
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

Перед публикацией обязательно:

1. перевыпусти ранее опубликованные GNews, NewsAPI и WorldNewsAPI ключи;
2. удали `.env` из истории Git и сделай force-push только после резервной копии;
3. добавь новые ключи в секреты хостинга, а не в файлы репозитория;
4. укажи публичный HTTPS `WEBAPP_URL` и новый `TELEGRAM_BOT_TOKEN`.

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

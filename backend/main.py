"""
Random World News - FastAPI Backend
Главный сервер для Telegram Mini App.
"""

import os
import json
from datetime import datetime
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from dotenv import load_dotenv

from news_fetcher import get_fetcher, NewsFetcher
from translator import get_translator
from country_data import get_language_name

# Загрузка переменных окружения (из родительской директории)
env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(env_path)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager для приложения."""
    # Startup
    print("🚀 Random World News starting...")
    yield
    # Shutdown
    fetcher = get_fetcher()
    await fetcher.close()
    print("👋 Random World News stopped")


app = FastAPI(
    title="Random World News",
    description="API для получения рандомных новостей со всего мира",
    version="1.0.0",
    lifespan=lifespan
)

# CORS для Telegram Mini App
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Telegram может открывать с разных доменов
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Глобальный счётчик новостей
global_news_count = 0


@app.get("/")
async def root():
    """Корневой эндпоинт."""
    return {
        "app": "Random World News",
        "version": "1.0.0",
        "description": "Telegram Mini App для рандомных новостей со всего мира",
        "endpoints": {
            "random_news": "/api/random-news",
            "health": "/api/health",
            "stats": "/api/stats"
        }
    }


@app.get("/api/health")
async def health():
    """Health check."""
    return {"status": "ok", "timestamp": datetime.now().isoformat()}


@app.get("/api/stats")
async def stats():
    """Статистика приложения."""
    return {
        "global_news_count": global_news_count,
        "timestamp": datetime.now().isoformat()
    }


@app.get("/api/random-news")
async def get_random_news():
    """
    Получить случайную новость со всего мира.
    
    Returns:
        JSON с переведённой новостью и метаданными.
    """
    global global_news_count
    
    try:
        # Получаем случайную новость
        fetcher = get_fetcher()
        news = await fetcher.fetch_random_news()
        
        if not news:
            raise HTTPException(status_code=503, detail="Could not fetch news")
        
        # Переводим на русский
        translator = get_translator()
        translated = translator.translate_news(
            title=news["title"],
            description=news["description"],
            source_lang=news.get("language")
        )
        
        # Увеличиваем глобальный счётчик
        global_news_count += 1
        
        # Формируем ответ
        response = {
            "success": True,
            "news": {
                "title": translated["title"],
                "description": translated["description"],
                "original_title": translated["original_title"],
                "original_description": translated["original_description"],
                "url": news["url"],
                "image": news.get("image", ""),
                "source": news["source"],
                "published_at": news.get("published_at", ""),
            },
            "metadata": {
                "country": news["country"],
                "language": {
                    "code": news.get("language", "unknown"),
                    "name": get_language_name(news.get("language", ""))
                },
                "translation_provider": translated["provider"],
                "api_source": news.get("api_source", "unknown")
            },
            "stats": {
                "global_count": global_news_count
            }
        }
        
        return JSONResponse(content=response)
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in get_random_news: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Статические файлы для webapp
webapp_path = os.path.join(os.path.dirname(__file__), "..", "webapp")
if os.path.exists(webapp_path):
    # Serve webapp at /app path
    app.mount("/app", StaticFiles(directory=webapp_path, html=True), name="webapp")
    
    @app.get("/")
    async def root_redirect():
        """Redirect root to webapp."""
        from starlette.responses import RedirectResponse
        return RedirectResponse(url="/app/")
    
    @app.get("/webapp")
    async def serve_webapp():
        """Serve the Mini App."""
        return FileResponse(os.path.join(webapp_path, "index.html"))


if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    debug = os.getenv("DEBUG", "false").lower() == "true"
    
    print(f"🌍 Starting Random World News on {host}:{port}")
    uvicorn.run("main:app", host=host, port=port, reload=debug)


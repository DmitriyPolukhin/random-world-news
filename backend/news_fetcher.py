"""
News Fetcher module - агрегатор рандомных новостей со всего мира.
Максимальная рандомность: случайная страна, случайный язык, случайный источник.
"""

import os
import random
import httpx
from datetime import datetime, timedelta
from typing import Optional
from cachetools import TTLCache
from country_data import get_country_data, get_country_by_language, get_all_country_codes, LANGUAGE_TO_COUNTRY
from rss_fetcher import get_rss_fetcher

# Кеш для новостей (5 минут TTL, максимум 100 элементов)
news_cache = TTLCache(maxsize=100, ttl=300)


class NewsFetcher:
    """Агрегатор новостей с максимальной рандомностью."""
    
    # Доступные категории для рандомизации
    CATEGORIES = [
        "general", "world", "nation", "business", "technology", 
        "entertainment", "sports", "science", "health"
    ]
    
    # Языки для GNews API
    GNEWS_LANGUAGES = [
        "ar", "zh", "nl", "en", "fr", "de", "el", "he", "hi", "it",
        "ja", "ml", "mr", "no", "pt", "ro", "ru", "es", "sv", "ta",
        "te", "uk"
    ]
    
    # Страны для GNews API  
    GNEWS_COUNTRIES = [
        "au", "br", "ca", "cn", "eg", "fr", "de", "gr", "hk", "in",
        "ie", "il", "it", "jp", "nl", "no", "pk", "pe", "ph", "pt",
        "ro", "ru", "sg", "es", "se", "ch", "tw", "ua", "gb", "us"
    ]
    
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=15.0)
        # Счётчик запросов для дебага
        self.request_count = 0
    
    @property
    def gnews_key(self):
        """Lazy load GNews API key."""
        return os.getenv("GNEWS_API_KEY")
    
    @property
    def worldnews_key(self):
        """Lazy load WorldNews API key."""
        return os.getenv("WORLDNEWS_API_KEY")
    
    @property
    def newsapi_key(self):
        """Lazy load NewsAPI key."""
        return os.getenv("NEWSAPI_KEY")
    
    async def fetch_random_news(self) -> Optional[dict]:
        """
        Получить случайную новость со всего мира.
        
        Returns:
            dict: {
                "title": str,
                "description": str,
                "url": str,
                "image": str,
                "source": str,
                "published_at": str,
                "country": dict,  # {flag, name, name_en}
                "language": str,
                "api_source": str  # какой API использовался
            }
        """
        # Проверяем доступные API (приоритет: RSS > GNews > NewsAPI > WorldNews)
        apis = []
        
        # RSS всегда доступен (бесплатно и безлимитно)
        apis.append("rss")
        print(f"✓ RSS feeds available (unlimited)")
        
        if self.gnews_key and self.gnews_key not in ("", "your_gnews_api_key_here"):
            apis.append("gnews")
            print(f"✓ GNews API key found")
        if self.newsapi_key and self.newsapi_key not in ("", "your_newsapi_key_here"):
            apis.append("newsapi")
            print(f"✓ NewsAPI key found")
        if self.worldnews_key and self.worldnews_key not in ("", "your_worldnews_api_key_here"):
            apis.append("worldnews")
            print(f"✓ WorldNews API key found")
        
        if not apis:
            print("⚠ No API keys found, using demo mode")
            return await self._get_demo_news()
        
        # Рандомный выбор API
        random.shuffle(apis)
        
        for api in apis:
            try:
                print(f"→ Trying {api}...")
                if api == "rss":
                    rss_fetcher = get_rss_fetcher()
                    result = await rss_fetcher.fetch_random_news()
                elif api == "gnews":
                    result = await self._fetch_from_gnews()
                elif api == "newsapi":
                    result = await self._fetch_from_newsapi()
                elif api == "worldnews":
                    result = await self._fetch_from_worldnews()
                
                if result:
                    print(f"✓ Got news from {api}")
                    return result
            except Exception as e:
                print(f"✗ Error fetching from {api}: {e}")
                continue
        
        # Fallback на демо
        print("⚠ All APIs failed, using demo")
        return await self._get_demo_news()
    
    async def _fetch_from_gnews(self) -> Optional[dict]:
        """Получить новость из GNews API."""
        # Рандомные параметры
        country = random.choice(self.GNEWS_COUNTRIES)
        language = random.choice(self.GNEWS_LANGUAGES)
        category = random.choice(self.CATEGORIES)
        
        # Иногда ищем без категории для большей рандомности
        use_category = random.choice([True, False])
        
        # Фильтр по дате - только за последние 2 дня
        from_date = (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%dT00:00:00Z")
        
        url = "https://gnews.io/api/v4/top-headlines"
        params = {
            "token": self.gnews_key,
            "country": country,
            "lang": language,
            "max": 10,
            "from": from_date,
        }
        
        if use_category:
            params["topic"] = category
        
        try:
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            articles = data.get("articles", [])
            if not articles:
                return None
            
            # Выбираем случайную статью
            article = random.choice(articles)
            
            return {
                "title": article.get("title", ""),
                "description": article.get("description", "") or article.get("content", ""),
                "url": article.get("url", ""),
                "image": article.get("image", ""),
                "source": article.get("source", {}).get("name", "Unknown"),
                "published_at": article.get("publishedAt", ""),
                "country": get_country_data(country),
                "language": language,
                "api_source": "gnews"
            }
        except Exception as e:
            print(f"GNews error: {e}")
            return None
    
    async def _fetch_from_newsapi(self) -> Optional[dict]:
        """Получить новость из NewsAPI.org."""
        # Страны, поддерживаемые NewsAPI
        countries = ["ae", "ar", "at", "au", "be", "bg", "br", "ca", "ch", "cn",
                     "co", "cu", "cz", "de", "eg", "fr", "gb", "gr", "hk", "hu",
                     "id", "ie", "il", "in", "it", "jp", "kr", "lt", "lv", "ma",
                     "mx", "my", "ng", "nl", "no", "nz", "ph", "pl", "pt", "ro",
                     "rs", "ru", "sa", "se", "sg", "si", "sk", "th", "tr", "tw",
                     "ua", "us", "ve", "za"]
        
        categories = ["business", "entertainment", "general", "health", "science", "sports", "technology"]
        
        country = random.choice(countries)
        category = random.choice(categories)
        
        url = "https://newsapi.org/v2/top-headlines"
        params = {
            "apiKey": self.newsapi_key,
            "country": country,
            "category": category,
            "pageSize": 10
        }
        
        try:
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            articles = data.get("articles", [])
            if not articles:
                return None
            
            # Выбираем случайную статью
            article = random.choice(articles)
            
            # Определяем язык по стране
            country_to_lang = {
                "us": "en", "gb": "en", "au": "en", "ca": "en", "ie": "en", "nz": "en",
                "de": "de", "at": "de", "ch": "de",
                "fr": "fr", "be": "fr",
                "es": "es", "mx": "es", "ar": "es", "co": "es", "ve": "es",
                "pt": "pt", "br": "pt",
                "it": "it",
                "ru": "ru", "ua": "ru",
                "jp": "ja",
                "cn": "zh", "tw": "zh", "hk": "zh",
                "kr": "ko",
                "nl": "nl",
                "pl": "pl",
                "tr": "tr",
                "ae": "ar", "eg": "ar", "sa": "ar", "ma": "ar",
                "in": "hi",
                "id": "id",
                "my": "ms",
                "th": "th",
                "ph": "tl",
                "il": "he",
                "gr": "el"
            }
            lang = country_to_lang.get(country, "en")
            
            return {
                "title": article.get("title", ""),
                "description": article.get("description", "") or article.get("content", ""),
                "url": article.get("url", ""),
                "image": article.get("urlToImage", ""),
                "source": article.get("source", {}).get("name", "Unknown"),
                "published_at": article.get("publishedAt", ""),
                "country": get_country_data(country),
                "language": lang,
                "api_source": "newsapi"
            }
        except Exception as e:
            print(f"NewsAPI error: {e}")
            return None
    
    async def _fetch_from_worldnews(self) -> Optional[dict]:
        """Получить новость из WorldNewsAPI."""
        # Рандомные параметры
        languages = list(LANGUAGE_TO_COUNTRY.keys())
        language = random.choice(languages)
        
        # Случайное смещение для разнообразия
        offset = random.randint(0, 50)
        
        url = "https://api.worldnewsapi.com/search-news"
        params = {
            "api-key": self.worldnews_key,
            "language": language,
            "number": 10,
            "offset": offset,
        }
        
        try:
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            articles = data.get("news", [])
            if not articles:
                return None
            
            # Выбираем случайную статью
            article = random.choice(articles)
            
            # Определяем страну по языку или источнику
            country_code = article.get("country", "")
            if country_code:
                country = get_country_data(country_code)
            else:
                country = get_country_by_language(language)
            
            return {
                "title": article.get("title", ""),
                "description": article.get("text", "")[:500] if article.get("text") else "",
                "url": article.get("url", ""),
                "image": article.get("image", ""),
                "source": article.get("source", {}).get("name", "") or article.get("author", "Unknown"),
                "published_at": article.get("publish_date", ""),
                "country": country,
                "language": language,
                "api_source": "worldnews"
            }
        except Exception as e:
            print(f"WorldNews error: {e}")
            return None
    
    async def _get_demo_news(self) -> dict:
        """Демо-новость когда нет API ключей."""
        demo_news = [
            {
                "title": "Добро пожаловать в Random World News!",
                "description": "Это демо-режим. Чтобы получать реальные новости со всего мира, добавьте API ключи в файл .env. Получите бесплатные ключи на gnews.io (100 запросов/день) и worldnewsapi.com (100 запросов/день).",
                "url": "https://gnews.io",
                "image": "",
                "source": "Random World News",
                "published_at": datetime.now().isoformat(),
                "country": {"flag": "🇺🇸", "name": "США", "name_en": "United States"},
                "language": "en",
                "api_source": "demo"
            },
            {
                "title": "日本の桜の季節が始まりました",
                "description": "Демо: Так будет выглядеть японская новость. Заголовок и описание автоматически переводятся на русский язык через DeepL или Google Translate.",
                "url": "https://example.com",
                "image": "",
                "source": "Tokyo News",
                "published_at": datetime.now().isoformat(),
                "country": {"flag": "🇯🇵", "name": "Япония", "name_en": "Japan"},
                "language": "ja",
                "api_source": "demo"
            },
            {
                "title": "Carnaval do Rio atrai milhões de turistas",
                "description": "Демо: Это пример бразильской новости на португальском. Приложение поддерживает более 40 языков и 200 стран мира.",
                "url": "https://example.com",
                "image": "",
                "source": "O Globo",
                "published_at": datetime.now().isoformat(),
                "country": {"flag": "🇧🇷", "name": "Бразилия", "name_en": "Brazil"},
                "language": "pt",
                "api_source": "demo"
            },
            {
                "title": "Технологический прорыв в Германии",
                "description": "Демо: Немецкие учёные разработали новый тип аккумуляторов. Это пример того, как выглядят новости из Европы в приложении.",
                "url": "https://example.com",
                "image": "",
                "source": "Der Spiegel",
                "published_at": datetime.now().isoformat(),
                "country": {"flag": "🇩🇪", "name": "Германия", "name_en": "Germany"},
                "language": "de",
                "api_source": "demo"
            }
        ]
        return random.choice(demo_news)
    
    async def close(self):
        """Закрыть HTTP клиент."""
        await self.client.aclose()


# Singleton instance
_fetcher = None


def get_fetcher() -> NewsFetcher:
    """Получить экземпляр фетчера."""
    global _fetcher
    if _fetcher is None:
        _fetcher = NewsFetcher()
    return _fetcher

"""
Translator module - перевод новостей на русский язык.
Использует deep-translator с несколькими провайдерами.
"""

import os
from functools import lru_cache
from deep_translator import GoogleTranslator, DeeplTranslator
from deep_translator.exceptions import TranslationNotFound, RequestError


class NewsTranslator:
    """Переводчик новостей с fallback между провайдерами."""
    
    def __init__(self):
        self.deepl_key = os.getenv("DEEPL_API_KEY")
        self._google = GoogleTranslator(source='auto', target='ru')
        self._deepl = None
        
        if self.deepl_key and self.deepl_key != "your_deepl_api_key_here":
            try:
                self._deepl = DeeplTranslator(
                    api_key=self.deepl_key,
                    source='auto',
                    target='ru'
                )
            except Exception:
                self._deepl = None
    
    def translate(self, text: str, source_lang: str = None) -> dict:
        """
        Перевести текст на русский.
        
        Returns:
            dict: {
                "original": str,
                "translated": str,
                "source_lang": str,
                "provider": str
            }
        """
        if not text or not text.strip():
            return {
                "original": text,
                "translated": text,
                "source_lang": source_lang or "unknown",
                "provider": "none"
            }
        
        # Если текст уже на русском, не переводим
        if source_lang and source_lang.lower().startswith("ru"):
            return {
                "original": text,
                "translated": text,
                "source_lang": "ru",
                "provider": "none"
            }
        
        translated = None
        provider = None
        
        # Пробуем DeepL (лучшее качество)
        if self._deepl:
            try:
                translated = self._deepl.translate(text[:5000])  # Лимит на текст
                provider = "deepl"
            except Exception:
                pass
        
        # Fallback на Google Translate
        if not translated:
            try:
                translated = self._google.translate(text[:5000])
                provider = "google"
            except (TranslationNotFound, RequestError, Exception) as e:
                # Если перевод не удался, возвращаем оригинал
                return {
                    "original": text,
                    "translated": text,
                    "source_lang": source_lang or "unknown",
                    "provider": "failed",
                    "error": str(e)
                }
        
        return {
            "original": text,
            "translated": translated,
            "source_lang": source_lang or "auto-detected",
            "provider": provider
        }
    
    def translate_news(self, title: str, description: str, source_lang: str = None) -> dict:
        """
        Перевести заголовок и описание новости.
        
        Returns:
            dict: {
                "title": str,
                "description": str,
                "original_title": str,
                "original_description": str,
                "source_lang": str,
                "provider": str
            }
        """
        title_result = self.translate(title, source_lang)
        desc_result = self.translate(description, source_lang)
        
        return {
            "title": title_result["translated"],
            "description": desc_result["translated"],
            "original_title": title,
            "original_description": description,
            "source_lang": title_result["source_lang"],
            "provider": title_result["provider"]
        }


# Singleton instance
_translator = None


def get_translator() -> NewsTranslator:
    """Получить экземпляр переводчика."""
    global _translator
    if _translator is None:
        _translator = NewsTranslator()
    return _translator

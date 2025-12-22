"""
Country data module - флаги, названия и метаданные стран.
Используется для отображения информации об источнике новости.
"""

# Маппинг ISO кодов стран на флаги-эмодзи и названия на русском
COUNTRIES = {
    # Европа
    "ru": {"flag": "🇷🇺", "name": "Россия", "name_en": "Russia"},
    "ua": {"flag": "🇺🇦", "name": "Украина", "name_en": "Ukraine"},
    "by": {"flag": "🇧🇾", "name": "Беларусь", "name_en": "Belarus"},
    "de": {"flag": "🇩🇪", "name": "Германия", "name_en": "Germany"},
    "fr": {"flag": "🇫🇷", "name": "Франция", "name_en": "France"},
    "gb": {"flag": "🇬🇧", "name": "Великобритания", "name_en": "United Kingdom"},
    "uk": {"flag": "🇬🇧", "name": "Великобритания", "name_en": "United Kingdom"},
    "it": {"flag": "🇮🇹", "name": "Италия", "name_en": "Italy"},
    "es": {"flag": "🇪🇸", "name": "Испания", "name_en": "Spain"},
    "pt": {"flag": "🇵🇹", "name": "Португалия", "name_en": "Portugal"},
    "nl": {"flag": "🇳🇱", "name": "Нидерланды", "name_en": "Netherlands"},
    "be": {"flag": "🇧🇪", "name": "Бельгия", "name_en": "Belgium"},
    "pl": {"flag": "🇵🇱", "name": "Польша", "name_en": "Poland"},
    "cz": {"flag": "🇨🇿", "name": "Чехия", "name_en": "Czech Republic"},
    "at": {"flag": "🇦🇹", "name": "Австрия", "name_en": "Austria"},
    "ch": {"flag": "🇨🇭", "name": "Швейцария", "name_en": "Switzerland"},
    "se": {"flag": "🇸🇪", "name": "Швеция", "name_en": "Sweden"},
    "no": {"flag": "🇳🇴", "name": "Норвегия", "name_en": "Norway"},
    "fi": {"flag": "🇫🇮", "name": "Финляндия", "name_en": "Finland"},
    "dk": {"flag": "🇩🇰", "name": "Дания", "name_en": "Denmark"},
    "ie": {"flag": "🇮🇪", "name": "Ирландия", "name_en": "Ireland"},
    "gr": {"flag": "🇬🇷", "name": "Греция", "name_en": "Greece"},
    "tr": {"flag": "🇹🇷", "name": "Турция", "name_en": "Turkey"},
    "ro": {"flag": "🇷🇴", "name": "Румыния", "name_en": "Romania"},
    "hu": {"flag": "🇭🇺", "name": "Венгрия", "name_en": "Hungary"},
    "bg": {"flag": "🇧🇬", "name": "Болгария", "name_en": "Bulgaria"},
    "rs": {"flag": "🇷🇸", "name": "Сербия", "name_en": "Serbia"},
    "hr": {"flag": "🇭🇷", "name": "Хорватия", "name_en": "Croatia"},
    "sk": {"flag": "🇸🇰", "name": "Словакия", "name_en": "Slovakia"},
    "si": {"flag": "🇸🇮", "name": "Словения", "name_en": "Slovenia"},
    
    # Азия
    "jp": {"flag": "🇯🇵", "name": "Япония", "name_en": "Japan"},
    "cn": {"flag": "🇨🇳", "name": "Китай", "name_en": "China"},
    "kr": {"flag": "🇰🇷", "name": "Южная Корея", "name_en": "South Korea"},
    "in": {"flag": "🇮🇳", "name": "Индия", "name_en": "India"},
    "id": {"flag": "🇮🇩", "name": "Индонезия", "name_en": "Indonesia"},
    "my": {"flag": "🇲🇾", "name": "Малайзия", "name_en": "Malaysia"},
    "sg": {"flag": "🇸🇬", "name": "Сингапур", "name_en": "Singapore"},
    "th": {"flag": "🇹🇭", "name": "Таиланд", "name_en": "Thailand"},
    "vn": {"flag": "🇻🇳", "name": "Вьетнам", "name_en": "Vietnam"},
    "ph": {"flag": "🇵🇭", "name": "Филиппины", "name_en": "Philippines"},
    "pk": {"flag": "🇵🇰", "name": "Пакистан", "name_en": "Pakistan"},
    "bd": {"flag": "🇧🇩", "name": "Бангладеш", "name_en": "Bangladesh"},
    "ae": {"flag": "🇦🇪", "name": "ОАЭ", "name_en": "United Arab Emirates"},
    "sa": {"flag": "🇸🇦", "name": "Саудовская Аравия", "name_en": "Saudi Arabia"},
    "il": {"flag": "🇮🇱", "name": "Израиль", "name_en": "Israel"},
    "kz": {"flag": "🇰🇿", "name": "Казахстан", "name_en": "Kazakhstan"},
    "uz": {"flag": "🇺🇿", "name": "Узбекистан", "name_en": "Uzbekistan"},
    "tw": {"flag": "🇹🇼", "name": "Тайвань", "name_en": "Taiwan"},
    "hk": {"flag": "🇭🇰", "name": "Гонконг", "name_en": "Hong Kong"},
    
    # Америка
    "us": {"flag": "🇺🇸", "name": "США", "name_en": "United States"},
    "ca": {"flag": "🇨🇦", "name": "Канада", "name_en": "Canada"},
    "mx": {"flag": "🇲🇽", "name": "Мексика", "name_en": "Mexico"},
    "br": {"flag": "🇧🇷", "name": "Бразилия", "name_en": "Brazil"},
    "ar": {"flag": "🇦🇷", "name": "Аргентина", "name_en": "Argentina"},
    "cl": {"flag": "🇨🇱", "name": "Чили", "name_en": "Chile"},
    "co": {"flag": "🇨🇴", "name": "Колумбия", "name_en": "Colombia"},
    "pe": {"flag": "🇵🇪", "name": "Перу", "name_en": "Peru"},
    "ve": {"flag": "🇻🇪", "name": "Венесуэла", "name_en": "Venezuela"},
    "cu": {"flag": "🇨🇺", "name": "Куба", "name_en": "Cuba"},
    
    # Африка
    "za": {"flag": "🇿🇦", "name": "ЮАР", "name_en": "South Africa"},
    "eg": {"flag": "🇪🇬", "name": "Египет", "name_en": "Egypt"},
    "ng": {"flag": "🇳🇬", "name": "Нигерия", "name_en": "Nigeria"},
    "ke": {"flag": "🇰🇪", "name": "Кения", "name_en": "Kenya"},
    "ma": {"flag": "🇲🇦", "name": "Марокко", "name_en": "Morocco"},
    "tn": {"flag": "🇹🇳", "name": "Тунис", "name_en": "Tunisia"},
    "gh": {"flag": "🇬🇭", "name": "Гана", "name_en": "Ghana"},
    "et": {"flag": "🇪🇹", "name": "Эфиопия", "name_en": "Ethiopia"},
    
    # Океания
    "au": {"flag": "🇦🇺", "name": "Австралия", "name_en": "Australia"},
    "nz": {"flag": "🇳🇿", "name": "Новая Зеландия", "name_en": "New Zealand"},
}

# Маппинг языков на типичные страны
LANGUAGE_TO_COUNTRY = {
    "en": "us",
    "ru": "ru",
    "de": "de",
    "fr": "fr",
    "es": "es",
    "pt": "br",
    "it": "it",
    "ja": "jp",
    "ko": "kr",
    "zh": "cn",
    "ar": "sa",
    "hi": "in",
    "tr": "tr",
    "pl": "pl",
    "nl": "nl",
    "sv": "se",
    "no": "no",
    "da": "dk",
    "fi": "fi",
    "cs": "cz",
    "el": "gr",
    "he": "il",
    "th": "th",
    "vi": "vn",
    "id": "id",
    "ms": "my",
    "uk": "ua",
    "ro": "ro",
    "hu": "hu",
    "bg": "bg",
}

# Названия языков на русском
LANGUAGES = {
    "en": "Английский",
    "ru": "Русский",
    "de": "Немецкий",
    "fr": "Французский",
    "es": "Испанский",
    "pt": "Португальский",
    "it": "Итальянский",
    "ja": "Японский",
    "ko": "Корейский",
    "zh": "Китайский",
    "ar": "Арабский",
    "hi": "Хинди",
    "tr": "Турецкий",
    "pl": "Польский",
    "nl": "Голландский",
    "sv": "Шведский",
    "no": "Норвежский",
    "da": "Датский",
    "fi": "Финский",
    "cs": "Чешский",
    "el": "Греческий",
    "he": "Иврит",
    "th": "Тайский",
    "vi": "Вьетнамский",
    "id": "Индонезийский",
    "ms": "Малайский",
    "uk": "Украинский",
    "ro": "Румынский",
    "hu": "Венгерский",
    "bg": "Болгарский",
}


def get_country_data(country_code: str) -> dict:
    """Получить данные о стране по ISO коду."""
    code = country_code.lower()
    if code in COUNTRIES:
        return COUNTRIES[code]
    return {"flag": "🌍", "name": "Неизвестно", "name_en": "Unknown"}


def get_country_by_language(language_code: str) -> dict:
    """Определить страну по языку источника."""
    lang = language_code.lower()[:2] if language_code else "en"
    country_code = LANGUAGE_TO_COUNTRY.get(lang, "us")
    return get_country_data(country_code)


def get_language_name(language_code: str) -> str:
    """Получить название языка на русском."""
    lang = language_code.lower()[:2] if language_code else "en"
    return LANGUAGES.get(lang, "Неизвестный")


def get_all_country_codes() -> list:
    """Получить список всех доступных кодов стран."""
    return list(COUNTRIES.keys())

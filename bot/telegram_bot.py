"""
Random World News - Telegram Bot
Бот для запуска Mini App и интеграции с Telegram.
"""

import logging
from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

try:
    from .settings import BotConfigError, load_bot_settings
except ImportError:
    from settings import BotConfigError, load_bot_settings

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

WEBAPP_URL = ""


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start."""
    user = update.effective_user
    
    # Кнопка для открытия Mini App
    keyboard = [
        [InlineKeyboardButton(
            text="🌍 Открыть Random World News",
            web_app=WebAppInfo(url=WEBAPP_URL)
        )]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_message = (
        f"Привет, {user.first_name}! 👋\n\n"
        "Добро пожаловать в **Random World News** — приложение для получения "
        "случайных новостей со всего мира!\n\n"
        "🇯🇵 Япония • 🇧🇷 Бразилия • 🇩🇪 Германия • 🇲🇽 Мексика\n"
        "...и ещё 200+ стран!\n\n"
        "Каждая новость уникальна и переведена на русский язык.\n\n"
        "Нажми кнопку ниже, чтобы начать! 👇"
    )
    
    await update.message.reply_text(
        welcome_message,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /help."""
    help_text = (
        "**Random World News** — бот для случайных новостей\n\n"
        "📰 **Как пользоваться:**\n"
        "1. Нажми кнопку 'Открыть Random World News'\n"
        "2. В приложении нажми 'Погнали!'\n"
        "3. Получи случайную новость из любой точки мира!\n\n"
        "🔄 Каждая новость абсолютно случайна — может быть из Японии, "
        "Мексики, Германии или любой другой страны.\n\n"
        "🌐 Все новости автоматически переводятся на русский.\n\n"
        "**Команды:**\n"
        "/start — Запустить бота\n"
        "/help — Показать эту справку\n"
        "/stats — Показать статистику"
    )
    
    await update.message.reply_text(help_text, parse_mode="Markdown")


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /stats."""
    # Здесь можно добавить реальную статистику из базы данных
    stats_text = (
        "📊 **Статистика Random World News**\n\n"
        "🌍 Страны: 200+\n"
        "📰 Источники: 60,000+\n"
        "🌐 Языки: 40+\n\n"
        "_Открой приложение, чтобы увидеть свою личную статистику!_"
    )
    
    keyboard = [
        [InlineKeyboardButton(
            text="📊 Моя статистика",
            web_app=WebAppInfo(url=WEBAPP_URL)
        )]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        stats_text,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик текстовых сообщений."""
    keyboard = [
        [InlineKeyboardButton(
            text="🌍 Получить случайную новость",
            web_app=WebAppInfo(url=WEBAPP_URL)
        )]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Нажми кнопку, чтобы получить случайную новость! 👇",
        reply_markup=reply_markup
    )


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик ошибок."""
    logger.error(f"Exception while handling an update: {context.error}")


def main() -> int:
    """Запуск бота."""
    global WEBAPP_URL

    try:
        settings = load_bot_settings()
    except BotConfigError as error:
        logger.error("Configuration error: %s", error)
        return 2

    WEBAPP_URL = settings.webapp_url
    
    print("🤖 Starting Random World News Bot...")
    
    # Создание приложения
    application = Application.builder().token(settings.token).build()
    
    # Регистрация обработчиков
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Обработчик ошибок
    application.add_error_handler(error_handler)
    
    # Запуск бота
    print("✅ Bot started! Press Ctrl+C to stop.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

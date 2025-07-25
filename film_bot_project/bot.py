import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

from db.mysql_connector import search_by_keyword
from db.log_writer import log_search

# Загрузка переменных окружения из .env
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# Словарь для хранения состояния пользователя (например, смещение)
user_state = {}

# 🔧 Форматирование списка фильмов
def format_film_list(results, start_index=1):
    lines = []
    for i, film in enumerate(results, start=start_index):
        title = film["title"]
        year = film["release_year"]
        description = film.get("description", "")
        lines.append(f"*{i}. {title}* ({year})\n_{description}_\n")
    return "\n".join(lines)

# 🎬 Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Привет! Введите ключевое слово, чтобы найти фильмы.")

# 🔍 Обработка текстового сообщения (поисковый запрос)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    query = update.message.text.strip()

    # логирование в Mongo + файл
    log_search(user_id, query)

    # поиск фильмов
    results = search_by_keyword(query, offset=0)
    user_state[user_id] = {
        "query": query,
        "offset": 0,
        "results": results,
    }

    if not results:
        await update.message.reply_text("❌ Фильмы не найдены.")
        return

    reply_text = format_film_list(results)
    keyboard = [[InlineKeyboardButton("➡ Далее", callback_data="next_page")]]
    await update.message.reply_text(
        reply_text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


# ⏭ Обработка кнопки "Далее"
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    if user_id not in user_state:
        await query.edit_message_text("🔄 Начните новый поиск.")
        return

    state = user_state[user_id]
    offset = state["offset"] + 10
    new_results = search_by_keyword(state["query"], offset=offset)

    if not new_results:
        await query.edit_message_text("✅ Все фильмы показаны.")
        user_state.pop(user_id)
        return

    user_state[user_id]["offset"] = offset
    user_state[user_id]["results"] = new_results
    reply_text = format_film_list(new_results, start_index=offset + 1)
    keyboard = [[InlineKeyboardButton("➡ Далее", callback_data="next_page")]]

    await query.edit_message_text(
        reply_text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

# 🚀 Запуск бота
if __name__ == "__main__":
    print("✅ Бот запущен.")
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(handle_callback))

    app.run_polling()

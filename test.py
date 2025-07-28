from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# 🔑 Твой токен (убедись, что он от твоего бота!)
TOKEN = "8364215424:AAEC1V_G4P_lSDUchDx2KFLWcnnH6MylxKw"

# 📩 Обработка входящих сообщений
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    print(f"📨 Сообщение от @{update.effective_user.username} ({update.effective_user.id}): {user_message}")
    await update.message.reply_text(f"Вы написали: {user_message}")

# 🚀 Запуск бота
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    print("✅ Тестовый бот запущен. Ожидаем сообщения...")
    app.run_polling()

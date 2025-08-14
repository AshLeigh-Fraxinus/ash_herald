import telebot
from telebot import types
from dotenv import load_dotenv
import os
from tarot_card import setup_tarot_handlers

def configure_bot():
    load_dotenv()
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    if not BOT_TOKEN:
        raise ValueError("Токен бота не найден в переменных окружения")
    return telebot.TeleBot(BOT_TOKEN)

def setup_handlers(bot):
    
    @bot.message_handler(commands=['start'])
    def start(message):
        """Обработчик команды /start"""
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("🔮 Вытащить карту дня")
        markup.add(btn1)
        bot.send_message(
            message.chat.id,
            "Приветствую, путник! \nЧем могу быть тебе полезен?",
            reply_markup=markup
        )
    setup_tarot_handlers(bot)

def main():
    """Основная функция запуска бота"""
    try:
        bot = configure_bot()
        setup_handlers(bot)
        
        print("Бот запущен и ждёт сообщения...")
        bot.polling(none_stop=True, interval=0)
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()
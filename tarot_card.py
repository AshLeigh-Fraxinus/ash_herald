import random
import sqlite3
from telebot import types

def setup_tarot_handlers(bot):
    @bot.message_handler(func=lambda message: True)
    def handle_button(message):
        if message.text == "🔮 Вытащить карту дня" or message.text == "/tarot_card":
            card_id = random.randint(1, 78)
            is_upright = random.choice([True, False])

            conn = sqlite3.connect("tarot.db")
            cursor = conn.cursor()

            cursor.execute("SELECT card_num, name FROM tarot WHERE id = ?", (card_id,))
            card_data = cursor.fetchone()

            if not card_data:
                bot.send_message(message.chat.id, "Будущее слишком туманно, не удалось создать прогноз ☁️")
                conn.close()
                return

            card_num, name = card_data

            if is_upright:
                cursor.execute("SELECT meaning FROM tarot_upright WHERE card_num = ?", (card_num,))
                meaning = cursor.fetchone()[0]
                cursor.execute("SELECT advice FROM advice_upright WHERE card_num = ?", (card_num,))
                advice = cursor.fetchone()[0]
                position = "Прямое положение"
            else:
                cursor.execute("SELECT meaning FROM tarot_reversed WHERE card_num = ?", (card_num,))
                meaning = cursor.fetchone()[0]
                cursor.execute("SELECT advice FROM advice_reversed WHERE card_num = ?", (card_num,))
                advice = cursor.fetchone()[0]
                position = "Перевернутое положение"

            message_text = (
                f"🔮 <b>Карта дня на сегодня:</b>\n\n🃏 <code>{name} - {position}</code>\n\n"
                f"🧿 <b>Что карта говорит о дне:</b> \n\n<code>{meaning}</code>\n\n"
                f"🕯 <b>Совет от карты:</b>\n\n<code>{advice}</code>\n\n"
            )

            bot.send_message(message.chat.id, message_text, parse_mode="HTML")
            conn.close()
        else:
            bot.send_message(message.chat.id, "Не понимаю команду 🤔")
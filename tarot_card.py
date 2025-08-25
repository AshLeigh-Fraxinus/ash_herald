import random
import time
import sqlite3
from telebot import types

def setup_tarot_handlers(bot):
    @bot.message_handler(func=lambda message: True)
    def handle_button(message):
        if message.text == "🔮 Вытащить карту дня" or message.text == "/tarot_card":
            card_id = random.randint(1, 78)
            is_upright = random.choice([True, False])
            if is_upright == True:
                card_position = 'upright' 
            else:
                card_position = 'reversed'

            conn = sqlite3.connect("tarot.db")
            cursor = conn.cursor()

            cursor.execute("SELECT card_num, name FROM tarot_upright WHERE id = ?", (card_id,))
            card_data = cursor.fetchone()

            if not card_data:
                bot.send_message(message.chat.id, "Будущее слишком туманно, не удалось создать прогноз ☁️")
                conn.close()
                return

            card_num, name = card_data

            if is_upright:
                cursor.execute("SELECT meaning FROM tarot_upright WHERE card_num = ?", (card_num,))
                meaning = cursor.fetchone()[0]
                position = "Прямое положение"
            else:
                cursor.execute("SELECT meaning FROM tarot_reversed WHERE card_num = ?", (card_num,))
                meaning = cursor.fetchone()[0]
                position = "Перевернутое положение"
            
            message_text = f"🕯 <i>Зажигаем свечи...</i>"
            bot.send_message(message.chat.id, message_text, parse_mode="HTML")
            time.sleep(1.5)
            
            message_text = f"🧿 <i>Открываем третий глаз...</i>"
            bot.send_message(message.chat.id, message_text, parse_mode="HTML")
            time.sleep(1.5)

            message_text = f"🃏 <b>{name}</b> - <i>{position}</i>\n\n🔮 {meaning}"
            bot.send_message(message.chat.id, message_text, parse_mode="HTML")

            try:
                sticker_path = f"tarot_img/{card_id}_{card_position}.webp"
                with open(sticker_path, 'rb') as sticker:
                    bot.send_sticker(message.chat.id, sticker)
            except FileNotFoundError:
                bot.send_message(message.chat.id, "🃏 Карта найдена, но изображение недоступно")
            except Exception as e:
                bot.send_message(message.chat.id, f"Произошла ошибка при отправке изображения: {str(e)}")
            
        else:
            bot.send_message(message.chat.id, "Не понимаю команду 🤔")
            
from telebot import TeleBot
from config import BOT_TOKEN, CHAT_ID
Token = BOT_TOKEN
chat_id = CHAT_ID
image_path_or_url = ".\\1.0.16_0\\project_logo.jpg"

def send_message_success(number_of_list, mail, status, points):
    try:
        str_send = f'✅ Gradient\n<b>{number_of_list}. {mail}</b>\n<b>Status: {status}</b>\n<b>Points: {points}</b>'
        bot = TeleBot(Token)
        bot.send_message(chat_id, str_send, parse_mode='html', disable_notification=True, disable_web_page_preview=True)
    except Exception as error:
        print(error)


def send_message_error(number_of_list, mail, status, points):
    try:
        str_send = f'❌ Gradient\n<b>{number_of_list}. {mail}</b>\n<b>Status: {status}</b>\n<b>Points: {points}</b>'
        bot = TeleBot(Token)
        bot.send_message(chat_id, str_send, parse_mode='html', disable_web_page_preview=True)
    except Exception as error:
        print(error)


def send_message_warning(number_of_list, mail, status, points):
    try:
        str_send = f'⚠️ Gradient\n<b>{number_of_list}. {mail}</b>\n<b>Status: {status}</b>\n<b>Points: {points}</b>'
        bot = TeleBot(Token)
        bot.send_message(chat_id, str_send, parse_mode='html', disable_web_page_preview=True)
    except Exception as error:
        print(error)


def send_message(text):
    str_send = f'<b>{text}</b>'
    bot = TeleBot(Token)
    bot.send_message(chat_id, str_send, parse_mode='html', disable_notification=True, disable_web_page_preview=True)


def send_message_with_photo():
    bot = TeleBot(Token)

    str_send = f"<b>✖️ PROJECT-X SOFT ✖️\n\n✅ STARTING WORKING ️✅</b>"

    with open(image_path_or_url, 'rb') as photo:
        bot.send_photo(
            chat_id,
            photo=photo,
            caption=str_send,
            parse_mode='HTML',
            disable_notification=True,
        )

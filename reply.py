from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from configs import LANGUAGES as langs


def languages_btn(src=''):
    markup = InlineKeyboardMarkup(row_width=2)
    buttons = []
    for key, value in langs.items():
        btn = InlineKeyboardButton(text=value, callback_data=f'lang_{src}_{key}')
        buttons.append(btn)

    markup.add(*buttons)
    return markup


def contact_btn():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn = KeyboardButton(text='Share contact 📱📞', request_contact=True)
    markup.add(btn)

    return markup

from telebot import TeleBot
from telebot.types import Message, CallbackQuery, ReplyKeyboardRemove
from dotenv import load_dotenv
import os
from reply import languages_btn, langs, contact_btn
from googletrans import Translator
from base import get_user, save_user_data, save_history_data, get_history


load_dotenv()
token = os.getenv('TOKEN')

bot = TeleBot(token)


@bot.message_handler(commands=['start', 'help', 'about', 'history'])
def commands(message: Message):
    chat_id = message.chat.id
    username = message.from_user.username
    if message.text == '/start':
        user = get_user(chat_id)
        if user:
            bot.send_message(chat_id, f'Hello {username}. You are welcome to bot Translator.')
            confirm_src_asc(message)
        else:
            bot.send_message(chat_id, 'Register sharing with your contact to use this bot', reply_markup=contact_btn())
    elif message.text == '/help':
        bot.send_message(chat_id, 'For support contact with developer: @shoksruks')
    elif message.text == '/about':
        bot.send_message(chat_id, 'This bot can translate from English to any languages')
    elif message.text == '/history':
        history = get_history(chat_id)
        if history:
            bot.send_message(chat_id, f'Last 10 histories:\n\n{history}')
        else:
            bot.send_message(chat_id, 'History is empty')


def confirm_src_asc(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Choose the language from which you will translate', reply_markup=languages_btn('src'))


@bot.callback_query_handler(lambda call: 'src' in call.data)
def confirm_dest_asc(call: CallbackQuery):
    chat_id = call.message.chat.id
    text_src = call.data.split('_')[2]
    msg_id = call.message.message_id
    bot.edit_message_text(chat_id=chat_id, message_id=msg_id, text='Choose the language to which you will translate',
                          reply_markup=languages_btn(text_src))


@bot.callback_query_handler(lambda call: 'lang' in call.data)
def get_dest_lang(call: CallbackQuery):
    _, text_src, text_dest = call.data.split('_')
    chat_id = call.message.chat.id
    msg_id = call.message.message_id

    bot.edit_message_text(chat_id=chat_id, message_id=msg_id, text='Enter text for translating')
    bot.register_next_step_handler(call.message, get_text_translate, text_src, text_dest)


def get_text_translate(message: Message, text_src, text_dest):
    chat_id = message.chat.id
    text = message.text
    if text.startswith('/'):
        commands(message)
    else:
        translator = Translator()
        result = translator.translate(text=text, src=text_src, dest=text_dest).text
        bot.send_message(chat_id, result)
        save_history_data(text_src, text_dest, text, result, chat_id)
        bot.send_message(chat_id, f'''Enter text again for translating from {langs[text_src]} to {langs[text_dest]}
or choose another command''')
        bot.register_next_step_handler(message, get_text_translate, text_src, text_dest)


@bot.message_handler(content_types=['contact'])
def get_contact_user(message: Message):
    chat_id = message.chat.id
    username = message.from_user.username
    phone = message.contact.phone_number
    user = get_user(chat_id)
    if not user:
        save_user_data(chat_id, username, phone)
        bot.send_message(chat_id, 'Registration was successefully', reply_markup=ReplyKeyboardRemove())
        confirm_src_asc(message)
    else:
        confirm_src_asc(message)


bot.infinity_polling()

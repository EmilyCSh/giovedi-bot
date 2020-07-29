import telegram.ext
from telegram.ext import Updater
from telegram.ext import CommandHandler
from dotenv import load_dotenv
from pathlib import Path
import os
env_path = Path('.') / 'secret.env'
load_dotenv(dotenv_path=env_path)
TOKEN = os.getenv('TG_TOKEN')
from datetime import datetime
from time import sleep

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher
j = updater.job_queue
CHANNEL = "@egiovedioggi"


def start(update, context):
    print('dbg')
    context.bot.send_message(chat_id=update.effective_chat.id, text='🔫 Lo è sempre stato.')

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)


def day(update, context):
    is_thu = datetime.now().weekday() == 3

    if is_thu:
        print("Sì")
        context.bot.send_message(chat_id=update.effective_chat.id, text="Sì")
    else:
        print("No")
        context.bot.send_message(chat_id=update.effective_chat.id, text="No")

day_handler = CommandHandler('day', day)
dispatcher.add_handler(day_handler)


def callback_thursday(context: telegram.ext.CallbackContext):
    if datetime.now().weekday() == 3:
        print("Sì daily")
        context.bot.send_message(chat_id=CHANNEL, 
                             text='Sì')
    else:
        print("No daily")
        context.bot.send_message(chat_id=CHANNEL, 
                             text='No')

job_daily = j.run_daily(callback_thursday, 1)



updater.start_polling()

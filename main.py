import telegram.ext
from telegram.ext import Updater, CommandHandler
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import InlineQueryHandler
from telegram.utils.helpers import escape_markdown
from dotenv import load_dotenv
from pathlib import Path
import os
from datetime import datetime
from datetime import time
from time import sleep
from uuid import uuid4

# TOKEN
env_path = Path('.') / 'secret.env'
# env_path = Path('.') / 'devel.env'
load_dotenv(dotenv_path=env_path)
TOKEN = os.getenv('TG_TOKEN')
CHANNEL = os.getenv('CHANNEL')

# Implement updater
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher
j = updater.job_queue


# Command /start: starts the bot and returns a nice message
def start(update, context):
    print('dbg')
    context.bot.send_message(chat_id=update.effective_chat.id, text='🔫 Lo è sempre stato.')

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)


# Command /day: returns "Yes" if day is Thursday, else, "No".
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


# Post message to channel every day at midnight
def callback_thursday(context: telegram.ext.CallbackContext):
    if datetime.now().weekday() == 3:
        print("Sì daily")
        context.bot.send_message(chat_id=CHANNEL, 
                             text='Sì')
    else:
        print("No daily")
        context.bot.send_message(chat_id=CHANNEL, 
                             text='No')

midnight = time.fromisoformat('00:00:00')
job_daily = j.run_daily(callback_thursday, time = midnight)


# Inline
def inline_day_eval():
    if datetime.now().weekday() == 3:
        return "Sì"
    else:
        return "No"

def inline_day(update, context):
    results = list()
    results.append(
        InlineQueryResultArticle(
            id=inline_day_eval(),
            title='È giovedì oggi?',
            input_message_content=InputTextMessageContent(inline_day_eval())
        )
    )
    context.bot.answer_inline_query(update.inline_query.id, results)

inline_day_handler = InlineQueryHandler(inline_day)
dispatcher.add_handler(inline_day_handler)

updater.start_polling()

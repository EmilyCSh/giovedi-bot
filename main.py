import telegram.ext
from telegram.ext import Updater, CommandHandler, InlineQueryHandler
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.utils.helpers import escape_markdown
import logging
from dotenv import load_dotenv
from pathlib import Path
import os
from datetime import datetime, time
from time import sleep
from uuid import uuid4


# TOKEN
env_path = Path('.') / 'secret.env'
# env_path = Path('.') / 'devel.env'
load_dotenv(dotenv_path=env_path)
TOKEN = os.getenv('TG_TOKEN')
# CHANNEL
CHANNEL = os.getenv('CHANNEL')


# Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Implement updater
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher
j = updater.job_queue


# Command /start: starts the bot and returns a nice message
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='🔫 Lo è sempre stato.')

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)


# Command /day: returns "Yes" if day is Thursday, else, "No".
def day(update, context):
    is_thu = datetime.now().weekday() == 3

    if is_thu:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Sì")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="No")

day_handler = CommandHandler('day', day)
dispatcher.add_handler(day_handler)


# Post message to channel every day at midnight
def callback_thursday(context: telegram.ext.CallbackContext):
    if datetime.now().weekday() == 3:
        logger.debug("Channel updated with YES")
        context.bot.send_message(chat_id=CHANNEL, 
                             text='Sì')
    else:
        logger.debug("Channel updated with NO")
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

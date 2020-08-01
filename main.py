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


# Implement Logging module for exception handling:
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


# Command /start: starts the bot and returns a nice message:
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='🔫 Lo è sempre stato.')


# Command /day: returns "Yes" if day is Thursday, else, "No":
def day(update, context):
    is_thu = datetime.now().weekday() == 3

    if is_thu:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Sì")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="No")


# Post message to channel every day at midnight:
def callback_thursday(context: telegram.ext.CallbackContext):
    if datetime.now().weekday() == 3:
        logger.debug("Channel updated with YES")
        context.bot.send_message(chat_id=CHANNEL, 
                             text='Sì')
    else:
        logger.debug("Channel updated with NO")
        context.bot.send_message(chat_id=CHANNEL, 
                             text='No')


# Inline:
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


def main():
    print(main)
    # Import env file for external variables:
    env_path = Path('.') / 'secret.env':
    # env_path = Path('.') / 'devel.env'
    load_dotenv(dotenv_path=env_path)
    # Import TOKEN from env:
    TOKEN = os.getenv('TG_TOKEN')
    # Import CHANNEL from env:
    CHANNEL = os.getenv('CHANNEL')

    # Implement updater:
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Implement JobQueue job to be scheduled daily:
    j = updater.job_queue

    # Command /start:
    updater.dispatcher.add_handler(CommandHandler('start', start))

    # Command /day:
    updater.dispatcher.add_handler(CommandHandler('day', day))

    # Run bot inline:
    updater.dispatcher.add_handler(InlineQueryHandler(inline_day))

    # Run and post to channel every day at midnight:
    midnight = time.fromisoformat('00:00:00')
    job_daily = j.run_daily(callback_thursday, time = midnight)

    # Start the bot:
    updater.start_polling()

    # Run bot until it gets stopped manually or receives
    # SIGINT, SIGTERM or SIGABRT:
    updater.idle()


# Entry point:
if __name__ == '__main__':
    main()

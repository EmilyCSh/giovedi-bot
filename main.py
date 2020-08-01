import telegram.ext
from telegram.ext import Updater, CommandHandler, InlineQueryHandler
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.utils.helpers import escape_markdown
import logging
from dotenv import load_dotenv
from pathlib import Path
import os
from datetime import datetime, time, timedelta
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
    context.bot.send_message(update.effective_chat.id, is_thu())

# Command /countdown: how many days until Thursday?
def countdown_core(update, context):
    date = datetime.today()
    for i in range(7):
        date += timedelta(days=1)
        if date.weekday() == 3:
            break
    return "Mancano " + str(i) + " giorni a giovedì"
    
def countdown(update, context):
    countdown_return = countdown_core(update,context)
    context.bot.send_message(update.effective_chat.id, text=countdown_return)


# Post message to channel every day at midnight:
def callback_thursday(context: telegram.ext.CallbackContext):
    logger.info(f"Channel updated with {msg := is_thu()}")
    context.bot.send_message(CHANNEL, msg)


# Inline:
def is_thu():
    return "Sì" if datetime.now().weekday() == 3 else "No"

def inline_day(update, context):
    results = [
        InlineQueryResultArticle(
            id=is_thu(),
            title='È giovedì oggi?',
            input_message_content=InputTextMessageContent(is_thu())
        )]
    context.bot.answer_inline_query(update.inline_query.id, results)

def inline_countdown(update, context):
    results = [
        InlineQueryResultArticle(
            id=countdown_core(),
            title='Quanti giorni mancano a giovedì?',
            input_message_content=InputTextMessageContent(countdown_core())
        )]
    context.bot.answer_inline_query(update.inline_query.id, results)


def main():
    # Import env file for external variables and import TOKEN and CHANNEL:
    load_dotenv(dotenv_path=Path('.') / 'devel.env')
    TOKEN, CHANNEL = os.getenv('TG_TOKEN'), os.getenv('CHANNEL')

    # Implement updater:
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Implement JobQueue job to be scheduled daily:
    j = updater.job_queue

    # Chat commands:
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('day', day))
    updater.dispatcher.add_handler(CommandHandler('countdown', countdown))

    # Inline commands:
    updater.dispatcher.add_handler(InlineQueryHandler(inline_day))
    updater.dispatcher.add_handler(InlineQueryHandler(inline_countdown))

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

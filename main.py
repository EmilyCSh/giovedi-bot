import telegram.ext
from telegram.ext import ApplicationBuilder, CommandHandler, InlineQueryHandler, Defaults
from telegram import InlineQueryResultArticle, InputTextMessageContent
import logging
from dotenv import load_dotenv
from pathlib import Path
import os
from datetime import datetime, time, timedelta
from time import sleep
from uuid import uuid4
from pytz import timezone


# Implement Logging module for exception handling:
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


# Command /start: starts the bot and returns a nice message:
async def start(update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id, text='🔫 Lo è sempre stato.')


# Command /day: returns "Yes" if day is Thursday, else, "No":
async def day(update, context):
    tz = context.bot.defaults.tzinfo
    await context.bot.send_message(update.effective_chat.id, is_thu(tz))

# Command /countdown: how many days until Thursday?
def countdown_core(update, context):
    tz = context.bot.defaults.tzinfo
    w = datetime.now(tz).weekday()
    return f"Mancano {(3 - w + 7) % 7} giorni a giovedì"

async def countdown(update, context):
    countdown_return = countdown_core(update,context)
    await context.bot.send_message(update.effective_chat.id, text=countdown_return)


# Post message to channel every day at midnight:
async def callback_thursday(context: telegram.ext.CallbackContext):
    global CHANNEL
    tz = context.bot.defaults.tzinfo
    msg = is_thu(tz)
    logger.info(f"Channel updated with {msg}")
    await context.bot.send_message(CHANNEL, msg)


# Inline:
def is_thu(tz):
    return "Sì" if datetime.now(tz).weekday() == 3 else "No"

async def inline_day(update, context):
    tz = context.bot.defaults.tzinfo
    results = [
        InlineQueryResultArticle(
            id="is_thu",
            title='È giovedì oggi?',
            input_message_content=InputTextMessageContent(is_thu(tz))
        ),
        InlineQueryResultArticle(
            id="countdown",
            title='Quanti giorni mancano a giovedì?',
            input_message_content=InputTextMessageContent(countdown_core(update, context))
        )
    ]
    await context.bot.answer_inline_query(update.inline_query.id, results)


def main():
    global CHANNEL
    TOKEN = os.getenv('TG_TOKEN')
    CHANNEL = os.getenv('CHANNEL')
    TZ = os.getenv('TZ')

    # Implement updater:
    tz = timezone(TZ)
    defaults = Defaults(tzinfo=tz)
    updater = ApplicationBuilder().token(TOKEN).defaults(defaults).build()

    # Implement JobQueue job to be scheduled daily:
    j = updater.job_queue

    # Chat commands:
    updater.add_handler(CommandHandler('start', start))
    updater.add_handler(CommandHandler('day', day))
    updater.add_handler(CommandHandler('countdown', countdown))

    # Inline commands:
    updater.add_handler(InlineQueryHandler(inline_day))

    # Run and post to channel every day at midnight:
    job_daily = j.run_daily(callback_thursday, time = time(0, 0))

    # Start the bot:
    updater.run_polling()

    # Run bot until it gets stopped manually or receives
    # SIGINT, SIGTERM or SIGABRT:


# Entry point:
if __name__ == '__main__':
    main()

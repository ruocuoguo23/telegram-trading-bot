from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackContext

from utils import ConfigManager
from binance_listing import BinanceListingChecker


listing_checker = BinanceListingChecker()
job_queue = None


async def new_listing(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    await context.bot.send_message(chat_id=chat_id, text="Binance New listing notifier started!")
    job_queue.run_repeating(check_new_listing, interval=60, chat_id=chat_id, name="new_listing")


async def check_new_listing(context: CallbackContext):
    new_listing_item = listing_checker.check()
    # you can trade or notify here
    if new_listing_item:
        await context.bot.send_message(chat_id=context.job.chat_id, text=f"New listing: {new_listing_item}")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a trading bot!")


if __name__ == '__main__':
    # init listing checker
    listing_checker.initialize()

    # load telegram token from config
    cfg = ConfigManager("../config/config.yaml")

    token = cfg.telegram_config.token

    application = ApplicationBuilder().token(token).build()
    job_queue = application.job_queue

    # register /start command
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    # register /newlisting command
    new_listing_handler = CommandHandler('newlisting', new_listing)
    application.add_handler(new_listing_handler)

    application.run_polling()

from telegram.ext import Updater
from config import BOT_TOKEN
from handlers.commands import register_command_handlers
from handlers.callback import register_callback_handlers

def main():
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    register_command_handlers(dispatcher)
    register_callback_handlers(dispatcher)

    updater.start_polling()
    updater.idle()

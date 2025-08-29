from telegram import Update, InlineKeyboardMarkup
from telegram.ext import CallbackContext, CommandHandler
from keyboards.xo_keyboards import start_game_keyboard
from models.database import exit_game, get_user_stats

def xo_command(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    user = update.effective_user
    msg = f"🎮 {user.first_name} wants to start a game!"
    keyboard = start_game_keyboard(user)
    context.bot.send_message(chat_id=chat_id, text=msg, reply_markup=keyboard)

def exit_command(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    exit_game(chat_id)
    context.bot.send_message(chat_id=chat_id, text="❌ Game exited.")

def stats_command(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    stats = get_user_stats(user_id)
    context.bot.send_message(chat_id=update.effective_chat.id, text=stats)

def register_command_handlers(dispatcher):
    dispatcher.add_handler(CommandHandler("xo", xo_command))
    dispatcher.add_handler(CommandHandler("exit", exit_command))
    dispatcher.add_handler(CommandHandler("stats", stats_command))

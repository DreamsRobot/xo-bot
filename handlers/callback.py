from telegram import Update
from telegram.ext import CallbackContext, CallbackQueryHandler
from models.database import join_game, make_move
from utils.xo_engine import format_board, check_winner, is_draw
from keyboards.xo_keyboards import xo_board_keyboard

def callback_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data
    user = query.from_user
    chat_id = query.message.chat_id

    if data == "join_game":
        status, board = join_game(chat_id, user)
        query.edit_message_text(status, reply_markup=xo_board_keyboard(board))
    elif data.startswith("cell_"):
        _, index = data.split("_")
        result, board, winner = make_move(chat_id, user, int(index))
        if winner:
            query.edit_message_text(result)
        elif is_draw(board):
            query.edit_message_text("⚖️ It's a draw!")
        else:
            query.edit_message_text(result, reply_markup=xo_board_keyboard(board))

def register_callback_handlers(dispatcher):
    dispatcher.add_handler(CallbackQueryHandler(callback_handler))

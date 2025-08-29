from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def start_game_keyboard(user):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎮 Join Game", callback_data="join_game")],
        [InlineKeyboardButton(f"Started by {user.first_name}", callback_data="ignore")]
    ])

def xo_board_keyboard(board):
    keyboard = []
    for i in range(0, 9, 3):
        row = [InlineKeyboardButton(board[j] or "⬜", callback_data=f"cell_{j}") for j in range(i, i+3)]
        keyboard.append(row)
    return InlineKeyboardMarkup(keyboard)

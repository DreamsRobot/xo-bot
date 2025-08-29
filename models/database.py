from pymongo import MongoClient
from config import MONGODB_URI

client = MongoClient(MONGODB_URI)
db = client.xo_bot
games = db.games
users = db.users

def create_game(chat_id, user):
    games.replace_one({"chat_id": chat_id}, {
        "chat_id": chat_id,
        "player_x": {"id": user.id, "name": user.first_name},
        "player_o": None,
        "board": [""] * 9,
        "turn": "X",
        "status": "waiting"
    }, upsert=True)

def join_game(chat_id, user):
    game = games.find_one({"chat_id": chat_id})
    if not game or game["status"] != "waiting":
        return "⚠️ No game to join.", None
    if game["player_x"]["id"] == user.id:
        return "⚠️ You can't join your own game.", None

    games.update_one({"chat_id": chat_id}, {
        "$set": {
            "player_o": {"id": user.id, "name": user.first_name},
            "status": "in_progress"
        }
    })
    return "✅ Game started!", [""] * 9

def make_move(chat_id, user, index):
    game = games.find_one({"chat_id": chat_id})
    board = game["board"]
    turn = game["turn"]

    current_player = game["player_x"] if turn == "X" else game["player_o"]
    if current_player["id"] != user.id:
        return "⛔ Not your turn!", board, None
    if board[index] != "":
        return "⛔ Cell already taken!", board, None

    board[index] = turn
    winner = check_winner(board)

    if winner:
        update_user_stats(current_player["id"], "win")
        loser = game["player_o"] if turn == "X" else game["player_x"]
        update_user_stats(loser["id"], "loss")
        games.delete_one({"chat_id": chat_id})
        return f"🎉 {current_player['name']} wins!", board, winner

    games.update_one({"chat_id": chat_id}, {
        "$set": {
            "board": board,
            "turn": "O" if turn == "X" else "X"
        }
    })
    return f"{current_player['name']} moved. Next turn!", board, None

def exit_game(chat_id):
    games.delete_one({"chat_id": chat_id})

def update_user_stats(user_id, result):
    field = {
        "win": "wins",
        "loss": "losses",
        "draw": "draws"
    }.get(result)
    users.update_one({"user_id": user_id}, {
        "$inc": {
            field: 1,
            "games_played": 1
        }
    }, upsert=True)

def get_user_stats(user_id):
    user = users.find_one({"user_id": user_id}) or {}
    return (
        f"📊 Stats:\n"
        f"Games Played: {user.get('games_played', 0)}\n"
        f"Wins: {user.get('wins', 0)}\n"
        f"Losses: {user.get('losses', 0)}\n"
        f"Draws: {user.get('draws', 0)}"
    )

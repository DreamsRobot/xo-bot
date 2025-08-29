def check_winner(board):
    wins = [(0,1,2), (3,4,5), (6,7,8),
            (0,3,6), (1,4,7), (2,5,8),
            (0,4,8), (2,4,6)]
    for a, b, c in wins:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]
    return None

def is_draw(board):
    return all(cell != "" for cell in board)

def format_board(board):
    def get_symbol(cell):
        return cell if cell else "⬜"
    rows = [board[i:i+3] for i in range(0, 9, 3)]
    return "\n".join(" ".join(get_symbol(c) for c in row) for row in rows)

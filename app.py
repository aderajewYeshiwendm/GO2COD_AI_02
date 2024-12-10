from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# Initialize the board
EMPTY = ''
board = [[EMPTY] * 3 for _ in range(3)]

def check_winner(b):
    # Check rows, columns, and diagonals
    for i in range(3):
        if b[i][0] == b[i][1] == b[i][2] != EMPTY:
            return b[i][0]
        if b[0][i] == b[1][i] == b[2][i] != EMPTY:
            return b[0][i]
    if b[0][0] == b[1][1] == b[2][2] != EMPTY:
        return b[0][0]
    if b[0][2] == b[1][1] == b[2][0] != EMPTY:
        return b[0][2]
    return None

def is_draw(b):
    return all(cell != EMPTY for row in b for cell in row)

def minimax(b, is_maximizing):
    winner = check_winner(b)
    if winner == 'O':
        return 1
    if winner == 'X':
        return -1
    if is_draw(b):
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for i in range(3):
            for j in range(3):
                if b[i][j] == EMPTY:
                    b[i][j] = 'O'
                    score = minimax(b, False)
                    b[i][j] = EMPTY
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(3):
            for j in range(3):
                if b[i][j] == EMPTY:
                    b[i][j] = 'X'
                    score = minimax(b, True)
                    b[i][j] = EMPTY
                    best_score = min(score, best_score)
        return best_score

def get_best_move(b):
    best_score = -float('inf')
    move = None
    for i in range(3):
        for j in range(3):
            if b[i][j] == EMPTY:
                b[i][j] = 'O'
                score = minimax(b, False)
                b[i][j] = EMPTY
                if score > best_score:
                    best_score = score
                    move = (i, j)
    return move

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/play', methods=['POST'])
def play():
    global board
    data = request.json
    row, col = data['row'], data['col']
    if board[row][col] != EMPTY:
        return jsonify({'error': 'cell already occupied'}), 400

    board[row][col] = 'X'
    if check_winner(board) == 'X':
        return jsonify({'status': 'win', 'board': board})
    if is_draw(board):
        return jsonify({'status': 'draw', 'board': board})

    ai_move = get_best_move(board)
    board[ai_move[0]][ai_move[1]] = 'O'
    if check_winner(board) == 'O':
        return jsonify({'status': 'loss', 'board': board})
    if is_draw(board):
        return jsonify({'status': 'draw', 'board': board})

    return jsonify({'status': 'continue', 'board': board})

@app.route('/reset', methods=['POST'])
def reset():
    global board
    board = [[EMPTY] * 3 for _ in range(3)]
    return jsonify({'status': 'reset', 'board': board})

if __name__ == '__main__':
    app.run(debug=True)

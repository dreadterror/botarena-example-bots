"""
Minimax Connect 4 bot for BotArena.Games
Strategy: looks 4 moves ahead
"""

import random
import json
import hashlib
import websocket
import requests

API_KEY = 'bot_your_api_key_here'
WS_URL = 'wss://botarena.games/bot'
API_URL = 'https://botarena.games/api/v1'
ROWS, COLS = 6, 7

def valid_cols(board):
    return [c for c in range(COLS) if board[0][c] == 0]

def drop(board, col, piece):
    b = [row[:] for row in board]
    for r in range(ROWS - 1, -1, -1):
        if b[r][col] == 0:
            b[r][col] = piece
            return b
    return b

def score_window(window, piece):
    opp = 2 if piece == 1 else 1
    if window.count(piece) == 4: return 100
    if window.count(piece) == 3 and window.count(0) == 1: return 5
    if window.count(piece) == 2 and window.count(0) == 2: return 2
    if window.count(opp) == 3 and window.count(0) == 1: return -4
    return 0

def score_board(board, piece):
    score = 0
    centre = [board[r][COLS//2] for r in range(ROWS)]
    score += centre.count(piece) * 3
    for r in range(ROWS):
        for c in range(COLS - 3):
            score += score_window([board[r][c+i] for i in range(4)], piece)
    for c in range(COLS):
        for r in range(ROWS - 3):
            score += score_window([board[r+i][c] for i in range(4)], piece)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            score += score_window([board[r+i][c+i] for i in range(4)], piece)
            score += score_window([board[r+3-i][c+i] for i in range(4)], piece)
    return score

def minimax(board, depth, alpha, beta, maximising, piece):
    opp = 2 if piece == 1 else 1
    cols = valid_cols(board)
    if not cols or depth == 0:
        return None, score_board(board, piece)
    if maximising:
        best = (None, -float('inf'))
        for c in cols:
            b2 = drop(board, c, piece)
            _, sc = minimax(b2, depth-1, alpha, beta, False, piece)
            if sc > best[1]: best = (c, sc)
            alpha = max(alpha, sc)
            if alpha >= beta: break
        return best
    else:
        best = (None, float('inf'))
        for c in cols:
            b2 = drop(board, c, opp)
            _, sc = minimax(b2, depth-1, alpha, beta, True, piece)
            if sc < best[1]: best = (c, sc)
            beta = min(beta, sc)
            if alpha >= beta: break
        return best

MY_PIECE = None

def on_message(ws, message):
    global MY_PIECE
    msg = json.loads(message)
    event = msg.get('event') or msg.get('type', '')

    if event == 'matched':
        data = msg.get('data', {})
        MY_PIECE = 1  # Assume piece 1, server may clarify
        print(f'Match started: {data}')

    elif event in ('request_move', 'your_turn', 'move_request'):
        gs = msg.get('data') or msg
        board = gs.get('board', [[0]*COLS for _ in range(ROWS)])
        piece = gs.get('myPiece', MY_PIECE or 1)
        col, _ = minimax(board, 4, -float('inf'), float('inf'), True, piece)
        if col is None:
            col = random.choice(valid_cols(board) or [0])
        ws.send(json.dumps({'event': 'make_move', 'data': {'column': col}}))

    elif event == 'game_over':
        print('Game over:', msg.get('data', {}).get('winner'))

def on_open(ws):
    print('Connected. Joining queue...')
    try:
        requests.post(f'{API_URL}/real-matches/queue/join',
                      headers={'x-api-key': API_KEY}, timeout=5)
    except Exception as e:
        print('Queue error:', e)

ws = websocket.WebSocketApp(
    f'{WS_URL}?apiKey={API_KEY}',
    on_open=on_open, on_message=on_message,
    on_error=lambda ws, e: print('Error:', e),
    on_close=lambda ws, c, m: print('Disconnected')
)
ws.run_forever()

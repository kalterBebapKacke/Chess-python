import chess
from chess import Termination

inf = float('inf')
neg_inf = float('-inf')

def _eval(fen:str):
        board = chess.Board(fen)
        fen = fen.split('/')
        extra = fen[-1].split(' ')
        fen[-1] = extra[0]
        fen = ''.join(fen)
        eval = ''
        outcome = board.outcome()
        if outcome == None:
            black = float((fen.count('r') * 5) + (fen.count('b') * 3) + (fen.count('n') * 3) + (fen.count('q') * 9) + (fen.count('p')))
            white = float((fen.count('R') * 5) + (fen.count('B') * 3) + (fen.count('N') * 3) + (fen.count('Q') * 9) + (fen.count('P')))
            eval = white - black
        elif outcome.termination == Termination.STALEMATE or outcome.termination == Termination.INSUFFICIENT_MATERIAL or outcome.termination == Termination.FIFTY_MOVES:
            eval = 0.0
        elif outcome.termination == Termination.CHECKMATE:
            if outcome.winner == True:
                eval = inf
            if outcome.winner == False:
                eval = neg_inf
        return eval

def fill_moves(workload):
    fen = workload[1]
    b = chess.Board(fen)
    moves = [str(x) for x in b.legal_moves]
    info = list()
    for move in moves:
        b.push_san(move)
        info.append([move, b.fen()])
        b.pop()
    return info

def move_first(fen):
    return ['', fen, []]
         
def min_max():
     pass

# info = [move, fen [[move, fen []], ]]
fen = 'rnbqkbn1/ppppppp1/7r/7p/4P3/8/PPPPKPPP/RNBQ1BNR w q - 2 3'
b = chess.Board(fen)
print([str(x) for x in b.legal_moves])
print(_eval(fen))
print(fill_moves(move_first(fen)))
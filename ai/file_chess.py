import chess
from chess import Termination
import time
import multiprocessing as mp
import cach

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
        info.append([move, b.fen(), 0.0, []])
        b.pop()
    workload[-1] = info
    return workload

def mp_fill_moves(workload):
    fen = workload[1]
    move_list = workload[0]
    depth = workload[2] + 1
    b = chess.Board(fen)
    moves = [str(x) for x in b.legal_moves]
    info = list()
    for move in moves:
        b.push_san(move)
        move_list.append(move)
        info.append([[x for x in move_list], b.fen(), depth, workload[3], 0.0, []])
        del move_list[-1]
        b.pop()
    workload[5] = info
    return workload

def move_first(fen):
    return ['', fen, _eval(fen), []]

def mp_move_first(fen, max_depth):
    return [[], fen, 0, max_depth, _eval(fen), []]

def player_func(player):
    if player:
        return max
    else:
        return min
         
def _min_max(workload, depth, best_eval=None, cur_depth=0, player=True, cache=0):

    if cur_depth == depth:
        workload[2] = _eval(workload[1])
        return workload

    if workload[3] == []:
        workload = fill_moves(workload)

    if workload[3] == []:
        workload[2] = _eval(workload[1])
        return workload

    print(workload)

    func = player_func(player)
    moves = workload[3]
    max_eval = None
    for move in moves:
        cur_eval = _min_max(move, depth, max_eval, cur_depth+1, not player, cache)

        print(cur_eval)
        if max_eval != None:
            max_eval = func((max_eval,  cur_eval), key=lambda x:x[2])
        else:
            max_eval = cur_eval

        if best_eval != None and max_eval != None:
            if player:
                if max_eval[2] < best_eval[2]:
                    workload[3] = max_eval
                    workload[2] = max_eval[2]
                    return workload
            else:
                if max_eval[2] > best_eval[2]:
                    workload[3] = max_eval
                    workload[2] = max_eval[2]
                    return workload

    print(max_eval)

    workload[3] = max_eval
    workload[2] = max_eval[2]

    return workload


def start(fen, depth, process=8):
    start = time.time()

    _f = fen[fen.find(' '):]
    if _f.__contains__('w'):
        player = True
    else:
        player = False
    cache = 0
    func = player_func(player)
    workload = move_first(fen)
    workload = fill_moves(workload)
    moves = workload[3]
    args = [[moves[x], depth, None, 0, not player, cache] for x in range(len(moves))]

    pool = mp.Pool(processes=process)
    res = pool.starmap(_min_max, args)

    res = func(res, key=lambda x:x[2])
    _res = [x for x in res]
    order = list()

    while True:
        order.append(_res[0])
        if _res[3] == []:
            break
        _res = _res[3]

    end = time.time()
    print(end - start)
    return {'moves': order,
            'eval' : res[2],
            'time' : end - start,
            'fen'  : fen,
            'depth': depth,}

def mp_min_max(workload, cache):
    #if cache.get(workload[1]) != []:

    workload = mp_fill_moves(workload)
    if workload[2] == workload[3] or workload[-1] == []:
        workload[4] = _eval(workload[1])
        workload[-1] = []
        return [None, workload]
    return [workload[-1], None]



def mp_controller(fen, max_depth=2, process=4):
    workload = mp_move_first(fen, max_depth)
    workload = mp_fill_moves(workload)
    _queue = workload[-1]
    smm, keys, value, length, _lenght = cach.setup()
    c = cach.cache(None, keys, value, length, _lenght)
    result = list()
    with mp.Pool(process) as pool:
        while _queue != []:
            print(_queue)
            args = [[_queue[x], c] for x in range(len(_queue))]
            res = pool.starmap(mp_min_max, args)
            _queue.clear()
            for x in res:
                if x[0] == None:
                    result.append(x[1])
                else:
                    _queue.append(x[0])
    print(result)





# info = [move, fen [[move, fen []], ]]
fen = 'rnbqkbn1/ppppppp1/7r/7p/4P3/8/PPPPKPPP/RNBQ1BNR w q - 2 3'
fen1 = '8/8/8/8/8/7q/3k4/K7 w - - 0 1'
fen2 = '1q6/8/8/8/8/8/2k5/K7 w - - 0 1'
fen3 = '8/8/8/8/3q4/2k5/8/K7 b - - 0 1'
fen4 = 'r2q3r/pp1bkp2/2pp3R/5P2/2B1P3/2N5/PPP5/2K3R1 w - - 0 1'
fen5 = 'r2q1r2/ppp1k3/1b1p4/3P4/3P1Q2/2P5/PP4P1/R5K1 w - - 0 1'
b = chess.Board(fen)
print([str(x) for x in b.legal_moves])
print(_eval(fen))
workload = move_first(fen1)
print(workload)
print(fill_moves(workload))

if __name__ == '__main__':
    workload = mp_move_first(fen4, 2)
    print(mp_fill_moves(workload))
    mp_controller(fen, 2, 5)
    #print(start(fen4, 3, process=16))


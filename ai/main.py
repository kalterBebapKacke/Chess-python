import chess
from chess import Termination

b = chess.Board('rnbqkbn1/ppppppp1/7r/7p/4P3/8/PPPPKPPP/RNBQ1BNR w q - 2 3')
print([str(x) for x in b.legal_moves])
print(b.outcome())

def split_fen(fen:str):
    fen = fen.split('/')
    extra = fen[-1]
    del fen[-1]
    extra = extra.split(' ')


class chess_ai():

    def __init__(self, fen:str):
        self.fen = fen

    def _eval(self, fen:str):
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
                eval = 0.5
            if outcome.winner == False:
                eval = -0.5
        return eval


    def get_fens(self, workload, fen):
        b = chess.Board(fen)
        lenght = len(workload[0])
        for work_number in range(len(workload)):
            work = workload[work_number]
            for x in work:
                b.push_san(x)
            _work = [xx for xx in work]
            _work.append(str(b.fen()))
            workload[work_number] = _work
            for x in range(lenght):
                b.pop()

    def eval_results(self, results):
        pass


    def _fill_moves(self, tree, depth):
        _l = list()
        for i, x in enumerate(tree):
            print(x)
            if not isinstance(x, list):
                _l.append(f'Zahl: {x}')
            else:
                _l.append(self._fill_moves(x, depth))
        return _l

    def minmax(self ,List, maxPlayer: bool = True):

        if not isinstance(List, list):
            return List

        if maxPlayer:
            eval = list()
            for x in List:
                eval.append(self.minmax(x, False))
            return max(eval)

        else:
            eval = list()
            for x in List:
                eval.append(self.minmax(x, True))
            return min(eval)

    def start(self, fen:str, depth:int=5):
        depth = depth * 2
        tree = [[str(x), fen, 0, []] for x in chess.Board(fen).legal_moves]
        self._fill_moves(tree, depth)
        print(depth)
        print(tree)

f = '8/8/5k1K/8/8/8/8/6r1 b - - 27 48'
c = chess_ai(f)
c.start(f, 1)





















import chess
from chess import Termination

inf = float('inf')
neg_inf = float('-inf')

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
                eval = inf
            if outcome.winner == False:
                eval = neg_inf
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


    def _fill_moves(self, tree, depth, cur_depth=0):
        _l = list()
        if cur_depth == depth:
            return tree
        for i, x in enumerate(tree):
            print(x)
            if not isinstance(x, list):
                b = chess.Board(tree[1])
                b.push_san(tree[0])
                fen = b.fen()
                moves = [[str(x), fen, 0, []] for x in b.legal_moves]
                tree[3] = self._fill_moves(moves, depth, cur_depth+1)
                return tree
            else:
                _l.append(self._fill_moves(x, depth, cur_depth+1))
        return _l

    def minmax(self ,List, maxPlayer: bool = True):
        if len(List)>3:
            if List[3] == []:
                b = chess.Board(List[1])
                b.push_san(List[0])
                fen = b.fen()
                List[1] = fen
                List[2] = self._eval(fen)
                return List

        if maxPlayer:
            eval = list()
            if isinstance(List[0], str):
                eval = self.minmax(List[3], True)
                _l = [xx for xx in List]
                _l[-1] = eval
                _l[2] = eval[2]
                eval = _l
            else:
                for x in List:
                    eval.append(self.minmax(x, False))
                eval = max(eval, key=lambda x: x[2])
            return eval

        else:
            eval = list()
            if isinstance(List[0], str):
                eval = self.minmax(List[3], False)
                _l = [xx for xx in List]
                _l[-1] = eval
                _l[2] = eval[2]
                eval = _l
            else:
                for x in List:
                    eval.append(self.minmax(x, True))
                eval = min(eval, key=lambda x: x[2])
            return eval

    def start(self, fen:str, depth:int=5, player:bool=True): #true is white
        depth = depth * 2
        tree = [[str(x), fen, 0, []] for x in chess.Board(fen).legal_moves]
        self._fill_moves(tree, depth)
        eval = self.minmax(tree, player)
        print(tree)
        print(eval)

    def create_move_list(self, fen):
        tree = [[str(x), fen, 0, []] for x in chess.Board(fen).legal_moves]
        return tree

    def better_minmax(self, List, max_depth, depth=0, maxPlayer: bool = True, best_eval=None):
        if not isinstance(List[0], list) and not List[0]=='':
            b = chess.Board(List[1])
            b.push_san(List[0])
            fen = b.fen()
            List[1] = fen
            del b
            if depth == max_depth:
                List[2] = self._eval(fen)
                return List
            else:
                List[3] = self.create_move_list(fen)
                if List[3] == []:
                    List[2] = self._eval(fen)
                    return List

        if maxPlayer:
            r = list()
            for x in List[3]:
                pas_eval = None
                if r != []:
                    r = [max(r, key=lambda x: x[2])]
                    pas_eval = r[0][2]
                    if best_eval is not None:
                        if pas_eval > best_eval:
                            print('Eingespart')
                            return r[0]
                r.append(self.better_minmax(x, max_depth, depth + 1, False, pas_eval))
            best = max(r, key=lambda x: x[2])
            List[3] = best
            List[2] = best[2]
            return List
        else:
            r = list()
            for x in List[3]:
                pas_eval = None
                if r != []:
                    r = [min(r, key=lambda x: x[2])]
                    pas_eval = r[0][2]
                    if best_eval is not None:
                        if pas_eval < best_eval:
                            print('Eingespart')
                            return r[0]
                r.append(self.better_minmax(x, max_depth, depth + 1, True, pas_eval))
            best = min(r, key=lambda x: x[2])
            List[3] = best
            List[2] = best[2]
            return List

    def better_start(self, fen:str, depth:int, player:bool):
        depth = depth * 2 + 1
        tree = ['', fen, 0, self.create_move_list(fen)]
        print(tree)
        print(self.better_minmax(tree, 5))

r = '8/3q2k1/p3R1p1/1p1n3r/5p2/PPPQ2p1/6B1/6K1 w - - 2 44'
m2 = 'Q2r4/1pk2pp1/2pbp2p/4n2P/1P6/1BPqB3/P4PP1/5NK1 w - - 1 29'
m1 = '5R2/8/5K1k/8/8/8/8/8 w - - 0 1'
c = chess_ai(m1)
c.better_start(r, 3, False)





















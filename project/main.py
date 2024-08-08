import os
from dotenv import load_dotenv
from BasicPackageServerSide import better_SQL as SQL
import chess
import chess.pgn
import io
load_dotenv()

# https://github.com/lichess-org/stockfish.js

class Player_Chess():

    def __init__(self, player_id, sql=None):
        if sql == None:
            self.SQL = SQL.SQL_Class()
            self.SQL.login(os.environ['user'], os.environ['pasw'], 'homeserver', ['chess_info'])
        else:
            self.SQl = sql
        self.player_id = player_id

    def new_game(self, pgn:str, side:str):
        pgn = self.new_import_game(pgn, side)
        print(pgn)
        self.SQL.basic_write(None, player_id=self.player_id, alanyse=str(pgn[0]).replace("'", '"'), side=side, result=pgn[1])

    def pgn_info(self, pgn:str, _from:str, to:str):
        new = pgn[pgn.find(_from)+len(_from):]
        new = new[:new.find(to)]
        return new

    def pgn_start_with(self, start:str, side:str) -> list:
        ids =  self.SQL.basic_read(None, 'id', player_id=self.player_id, side=side)
        games = list()
        for id in ids:
            game = self.SQL.basic_read(None, 'pgn', 'result', player_id=self.player_id, side=side, id=id)
            if str(game[0]).startswith(start):
                games.append(game)
        return games

    def get_games(self, side):
        return self.SQL.basic_read(None, 'alanyse', 'side_played', player_id=self.player_id, side=side, headers={})

    def new_import_game(self, pgn:str, side:str):
        result = self.pgn_info(pgn, '[Result "', '"]')
        print(result)
        if int(result[0]) > int(result[2]):
            if side == 'w':
                result = 'w'
            elif side == 'b':
                result = 'l'
        elif int(result[0]) < int(result[2]) and side == 'b':
            if side == 'b':
                result = 'w'
            elif side == 'w':
                result = 'l'
        print(result)
        pgn = pgn[pgn.find('1.'):]
        print(pgn)
        pgn = list(pgn)
        while pgn.__contains__('('):
            del pgn[pgn.index('('):pgn.index(')') + 1]
        while pgn.__contains__(')'):
            del pgn[pgn.index(')')]
        pgn = ''.join(pgn)
        pgn = pgn.split('.')
        while pgn.__contains__(''):
            del pgn[pgn.index('')]
        print(pgn)
        info = pgn[0]
        print(info)
        del pgn[0]
        for i, x in enumerate(pgn):
            if i == len(pgn) - 1:
                pgn[i] = x.strip()
                break
            else:
                pgn[i] = x[0:-(len(str(i)) + 1)].strip()
        return [pgn, result]

    def import_game(self, pgn:str):
        pgn = list(pgn)
        while pgn.__contains__('('):
            del pgn[pgn.index('('):pgn.index(')')+1]
        while pgn.__contains__(')'):
            del pgn[pgn.index(')')]
        pgn = ''.join(pgn)
        pgn = pgn.split('.')
        while pgn.__contains__(''):
            del pgn[pgn.index('')]
        print(pgn)
        info = pgn[0]
        print(info)
        del pgn[0]
        for i, x in enumerate(pgn):
            if i == len(pgn)-1:
                pgn[i] = x.strip()
                break
            else:
                pgn[i] = x[0:-(len(str(i))+1)].strip()
        print(pgn)
        results = []
        results = self._import(pgn, results)
        return results


    def _import(self, pgn:list, List:list):
        List.append(pgn[0])
        del pgn[0]
        if len(pgn) != 0:
            List.append(self._import(pgn, []))
        return List

pgn = '1. d4 d5 2. c4 dxc4 3. Nf3 Nf6 4. Nc3 e6 5. Bg5 Bb4 6. Bxf6 Qxf6 7.  e3 Bxc3+ 8. bxc3 Nc6 (8... b5 9. a4 c6 10. Ne5 Nd7 11. Nxd7 Bxd7 12. axb5 cxb5 13. Rb1) 9. Bxc4 Qxd4 10. cxd4 Nxd4 11. Ne5 Nf3+ 12. Ke2 Nxh2 13. Ng4 Nxg4 14. Ke1 e5 15. Qd5 Be6 16. Qd3 Bxc4 17. Qxc4 O-O 18. e4 Rfd8 19. Kf1 Rd2 20. f3 Rf2+ 21. Ke1 Rd8 22. Qc2 Rxc2 23. Kf1 Ne3+ 24. Ke1 Rdd2 25. Rd1 (25. Rf1 Rf2 (25... Re2#)) 25... Re2#'
p2 = '1. d4 d5 2. Nf3 (2. c4 e6 3. Nf3 dxc4 4. e3 b5 5. a4 c6 6. b3 cxb3 7. axb5 cxb5 8. Bxb5+ Bd7 9. Qxb3 Bxb5 10. Qxb5+ Nd7 11. O-O) 2... c5'
b_pgn= '''[Event "Live Chess"]
[Site "Chess.com"]
[Date "2024.03.28"]
[Round "?"]
[White "francamatta"]
[Black "N0Id33a"]
[Result "1-0"]
[ECO "B10"]
[WhiteElo "996"]
[BlackElo "954"]
[TimeControl "600"]
[EndTime "14:04:25 PDT"]
[Termination "francamatta won by resignation"]

1. e4 c6 2. Nc3 d5 3. Nf3 Nf6 4. e5 Nfd7 5. d4 c5 6. Bf4 Qa5 7. Bd2 cxd4 8. Nxd4
Nxe5 9. Bb5+ Nbc6 10. O-O Bd7 11. Nxd5 Nxd4 12. Bxa5 Bxb5 13. Nc7+ Kd7 14. Nxa8
Bxf1 15. Qxd4+ Ke6 1-0'''

p = Player_Chess(22)
a = p.pgn_start_with('["e4 c6", "Nc3 d5", ', 'b')
print(a)
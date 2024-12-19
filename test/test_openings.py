import chess
import chess.engine
import chess.pgn
from io import StringIO

pgn_string = "1. e4 e5 2. f4"
engine = chess.engine.SimpleEngine.popen_uci("../Stockfish/stockfish_current_normal.exe")

pgn=open('test_pgn.pgn','r')

game = chess.pgn.read_game(pgn)
game2 = chess.pgn.read_game(StringIO(pgn_string))

print(game.board().fen())
print(game2.board().fen())
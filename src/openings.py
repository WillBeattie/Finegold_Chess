import chess
import chess.engine
import chess.pgn
from io import StringIO
import berserk
import tqdm
import csv

# vanilla_sf = chess.engine.SimpleEngine.popen_uci('../Stockfish/stockfish_current_normal.exe')
# no_f6_sf = chess.engine.SimpleEngine.popen_uci('../Stockfish/stockfish_f6_.exe')

token = open('../token.token')
token = str(token.readline())
session = berserk.TokenSession(token)
client = berserk.Client(session=session)


def get_number_of_masters_games(pgn_string, client=client):
    """
    Asks the lichess db for the prevelance of a particular position
    :param pgn_string: A string representing a game in pgn format, from the beginning
    :return:
    """
    fen = get_fen_from_pgn_string(pgn_string)
    print(fen)
    response = client.opening_explorer.get_masters_games(position=fen)

    return response


def get_fen_from_pgn_string(pgn_string):
    pgn = StringIO(pgn_string)
    board = chess.Board()
    for move in chess.pgn.read_game(pgn).mainline_moves():
        board.push(move)
    return board.fen()


def get_eval(engine, fen=None, pgn_string=None, depth=None, time=None):
    """
    Use a chess engine to evaluate a chess position.  Exactly one method to describe the position must be provided,
    and exactly one end condition for the calculation must be provided
    :param engine: An python-chess.engine SimpleEngine object
    :param fen: Forsythe-Edwards Notation, gives the game state
    :param pgn_string: A list of moves from the start position to reach the game state to be evaluated, in pgn format
    :param depth: Terminating condition, check N moves deep
    :param time: Terminating condition, calculate for T seconds
    :return: An evaluation of the position in pawns.  >0 is good for white, <0 good for black
    """
    if (fen is None) == (pgn_string is None):
        raise ValueError(f"Provide exactly one of fen ({fen}) and pgn_string ({pgn_string})")
    if (depth is None) == (time is None):
        raise ValueError(f'Provide exactly one of time ({time}) and depth ({depth}')

    if not fen:
        fen = get_fen_from_pgn_string(pgn_string)

    board = chess.Board()
    board.set_fen(fen)

    if time:
        score = engine.analyse(board, chess.engine.Limit(time=time))['score'].white()
    elif depth:
        score = engine.analyse(board, chess.engine.Limit(depth=depth))['score'].white()

    return score


def process_file(path, engines):
    outfile = f"results/{path.split('/')[-1]}_processed.tsv"

"""
def main():
    from itertools import islice

    header = ['Code', 'Name', 'Move List', 'Stockfish Eval', 'FinegoldFish Eval']
    target_eco = 'c'
    with open(f'../chess_openings/chess-openings/{target_eco}.tsv', "r", newline="") as in_file, open(
            f'../results/{target_eco}.tsv', 'w', newline="") as out_file:
        f_in = csv.reader(in_file, delimiter='\t')
        f_out = csv.writer(out_file, delimiter='\t')

        f_out.writerow(header)

        for line in tqdm.tqdm(islice(f_in, 1, None), desc="Processing Positions", unit="line"):
            position = line[-1]
            sf_eval = get_eval(vanilla_sf, pgn_string=position, depth=26)
            ff_eval = get_eval(no_f6_sf, pgn_string=position, depth=26)
            f_out.writerow(line + [sf_eval, ff_eval])


if __name__ == "__main__":
    main()
"""
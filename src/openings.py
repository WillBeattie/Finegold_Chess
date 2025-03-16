import chess
import chess.engine
import chess.pgn
from io import StringIO
import berserk
import tqdm
import csv
from time import sleep
import pandas as pd

token = open('../token.token')
token = str(token.readline())
session = berserk.TokenSession(token)
client = berserk.Client(session=session)


def query_master_db(pgn_string=None, fen=None, client=client, t_sleep=3):
    """
    Query the lichess db.  A pause is built in to prevent rate limiting
    :param pgn_string: A string representing a game in pgn format, from the beginning
    :return: A response dictionary from lichess
    """
    if not fen:
        fen = get_fen_from_pgn_string(pgn_string)

    sleep(t_sleep)
    # TODO Add rate limitation error handling
    response = client.opening_explorer.get_masters_games(position=fen)
    return response


def get_fen_from_pgn_string(pgn_string):
    pgn = StringIO(pgn_string)
    board = chess.Board()
    for move in chess.pgn.read_game(pgn).mainline_moves():
        board.push(move)
    return board.fen()


def detail_from_master(pgn_str):
    """
    Fetches pieces of information we might want to know about an opening from the lichess DB
    :param pgn_str:
    :return: number of master games from that position, number of games in which black plays f7f6
    """
    response = query_master_db(pgn_str)
    n_games = sum([response[k] for k in ['black', 'white', 'draws']])

    n_f6 = 0
    moves = response['moves']
    if not moves:
        return n_games, n_f6

    for move in moves:
        if move['uci'] == 'f7f6':
            n_f6 = sum([move['white'], move['black'], move['draws']])

    return n_games, n_f6


def detail_opening_list():
    """
    Supplements the ECO list with fields for number of master games (lichess db) and number of master games involving f7f6
    :return: Nothing.  Creates a json file for each of the ECO lettered inputs
    """

    from itertools import islice
    import json

    for fn in ['a', 'b', 'c', 'd', 'e']:
        with open(f'../results/ECO_master_db_{fn}.json', 'w') as outfile, open(
                f'../chess_openings/chess-openings/{fn}.tsv', 'r', newline='') as infile:

            f_in = csv.reader(infile, delimiter='\t')
            opening_dict = {}

            for line in tqdm.tqdm(islice(f_in, 1, None)):
                ECO_Code = line[0]
                ECO_Name = line[1]
                pgn_str = line[2]

                n_games, n_f6 = detail_from_master(pgn_str)

                opening_dict[pgn_str] = {"ECO Code": ECO_Code,
                                         "ECO Name": ECO_Name,
                                         "Number of Master Games": n_games,
                                         "Number of f6 moves": n_f6}

                print(opening_dict[pgn_str])
            json.dump(opening_dict, outfile, indent=4)


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

    board = chess.Board(fen)

    if time:
        score = engine.analyse(board, chess.engine.Limit(time=time))['score'].white()
    elif depth:
        score = engine.analyse(board, chess.engine.Limit(depth=depth))['score'].white()

    return score.cp


def reduce_openings():
    import json
    """
    Combine the json files from the named opening ECO codes and chuck out any uncommon openings 
    :return:
    """
    cs = ['a', 'b', 'c', 'd', 'e']
    MIN_NUM_GAMES = 5
    openings = []
    for c in cs:
        with open(f"../results/ECO_master_db_{c}.json", "r") as file:
            data = json.load(file)
            df = pd.DataFrame.from_dict(data, orient="index")
            df = df[df['Number of Master Games'] >= MIN_NUM_GAMES]
            print(df.head())
            openings.append(df)
    merged_df = pd.concat(openings)
    merged_df.sort_values(by='Number of Master Games', ascending=False, inplace=True)
    merged_df.to_json("../results/ECO_w_Master_Games.json", orient='index', indent=4)
    return openings


def add_evals_to_json(depth=15):
    import json

    vanilla_sf = chess.engine.SimpleEngine.popen_uci('../Stockfish/stockfish_current_normal.exe')
    no_f6_sf = chess.engine.SimpleEngine.popen_uci('../Stockfish/stockfish_f6_.exe')

    configs = {"Threads": 4,
               "Hash": 2048,
               }
    vanilla_sf.configure(configs)
    no_f6_sf.configure(configs)

    with open('../results/ECO_w_Master_Games_Evaluated.json', "r") as in_file:

        data = json.load(in_file)

    for i, (position, details) in tqdm.tqdm(enumerate(data.items())):
        if 'SF Eval' not in details:
            details['SF Eval'] = get_eval(vanilla_sf, pgn_string=position, depth=depth)
        if 'No f6 Eval' not in details:
            details['No f6 Eval'] = get_eval(no_f6_sf, pgn_string=position, depth=depth)

        if i % 50 == 0: # Periodically dump results in case of interruption
            with open('../results/ECO_w_Master_Games_Evaluated.json', 'w') as out_file:
                json.dump(data, out_file, indent=4)


if __name__ == "__main__":
    add_evals_to_json(depth=30)

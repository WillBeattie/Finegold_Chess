import chess
import chess.engine
import chess.pgn
from io import StringIO
import unittest
import src.openings as openings


class test_engines(unittest.TestCase):
    def test_dutch(self):
        """ We expect the evaluation of the Dutch to be the same between vanilla stockfish and no_f6 stockfish,
        given f6 is never a legal move in any variation for black"""
        DEPTH = 30
        THRESHOLD_EVAL_DIFF = 15 # In centipawns
        vanilla_sf = chess.engine.SimpleEngine.popen_uci("../Stockfish/stockfish_current_normal.exe")
        no_f6_sf = chess.engine.SimpleEngine.popen_uci("../Stockfish/stockfish_f6_.exe")

        pgn_string = "1. d4 f5"
        fen = openings.get_fen_from_pgn_string(pgn_string)
        vanilla_eval = openings.get_eval(vanilla_sf, fen, depth=DEPTH)
        no_f6_eval = openings.get_eval(no_f6_sf, fen, depth=DEPTH)
        print(f'SF Eval: {vanilla_eval.score()}')
        print(f'No f6 Eval: {no_f6_eval.score()}')
        self.assertLessEqual(abs(vanilla_eval.score() - no_f6_eval.score()), THRESHOLD_EVAL_DIFF)


class test_lichess(unittest.TestCase):
    """ Test functionality related to the lichess API"""

    def test_masters_db(self):
        import berserk
        test_fen = "rnbqkbnr/ppp1pppp/8/3p4/2PP4/8/PP2PPPP/RNBQKBNR b KQkq - 0 2"
        with open('../token.token') as token:
            token = str(token.readline())
            session = berserk.TokenSession(token)
            client = berserk.Client(session=session)
            response = client.opening_explorer.get_masters_games(position=test_fen)
            self.assertEqual(response['opening']['name'], "Queen's Gambit")


class helperFunctionTests(unittest.TestCase):
    """ Tests for helper functions"""

    def test_get_fen_from_pgn(self):
        pgn_and_fen = {
            "1. d4 d5 2. c4 e6 3. Nc3 Nf6 4. cxd5 exd5 5. Bg5 Be7": "rnbqk2r/ppp1bppp/5n2/3p2B1/3P4/2N5/PP2PPPP/R2QKBNR w KQkq - 2 6",
            "1. e4 c5 2. Nf3 Nc6 3. d4 cxd4 4. Nxd4 g6 5. Nc3 Bg7 6. Be3 Nf6 7. Bc4 O-O 8. Bb3 Ng4 9. Qxg4 Nxd4 10. Qh4 Qa5 11. O-O Bf6 12. Qxf6": "r1b2rk1/pp1ppp1p/5Qp1/q7/3nP3/1BN1B3/PPP2PPP/R4RK1 b - - 0 12",
            "1. e4 c6 2. d4 d5 3. e5 Bf5 (3... c5)": "rn1qkbnr/pp2pppp/2p5/3pPb2/3P4/8/PPP2PPP/RNBQKBNR w KQkq - 1 4"}
        for pgn in pgn_and_fen:
            expected_fen = pgn_and_fen[pgn]
            self.assertEqual(expected_fen, openings.get_fen_from_pgn_string(pgn))


if __name__ == "__main__":
    unittest.main()

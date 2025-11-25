import unittest
import os
from tennis_logger.game_state import GameState
from tennis_logger.logger import MatchLogger

class TestTennisLogger(unittest.TestCase):
    def test_score_logic(self):
        gs = GameState()
        self.assertEqual(gs.get_display_score(), "0 - 0")
        
        gs.add_point('server')
        self.assertEqual(gs.get_display_score(), "15 - 0")
        
        gs.add_point('receiver')
        self.assertEqual(gs.get_display_score(), "15 - 15")
        
        # Test Game Win
        gs.points_server = 3 # 40
        gs.points_receiver = 0 # 0
        gs.add_point('server') # Game Server
        self.assertEqual(gs.games_server, 1)
        self.assertEqual(gs.points_server, 0)

    def test_logger(self):
        filename = "test_log.csv"
        if os.path.exists(filename):
            os.remove(filename)
            
        logger = MatchLogger(filename=filename)
        self.assertTrue(os.path.exists(filename))
        
        data = {
            "server": "n",
            "final_outcome": "PtWon"
        }
        logger.log_point(data)
        
        with open(filename, 'r') as f:
            lines = f.readlines()
            self.assertEqual(len(lines), 2) # Header + 1 row
            
        os.remove(filename)

if __name__ == '__main__':
    unittest.main()

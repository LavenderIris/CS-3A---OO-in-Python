# Priscilla Chung Finder
# Final Unit test
# CS 3A
# unit tests for various states of my tic tac toe board

import unittest
import pygame, sys
from lib import *

class Test_libpy(unittest.TestCase):

    def test_check_not_game_over(self):
        """
        Unit test to check when in-game
        :return:
        """
        pygame.init()
        board = Board(grid_size=3, box_size=100, border=50, line_width=10)
        surface_size = board.surface.get_height()
        board.process_click_ingame(surface_size/2, surface_size/2)
        ans = False
        self.assertEqual(board.game_over, ans)

    def test_check_gameover(self):
        """
        Unit test to check when gameover.
        :return:
        """
        pygame.init()
        board = Board(grid_size=3, box_size=100, border=50, line_width=10)
        surface_size = board.surface.get_height()

        # sets the board for gameover state
        board.process_click(surface_size/2, surface_size/2)
        board.process_click(surface_size/2, surface_size * 0.7)
        board.process_click(surface_size * 0.7, surface_size/2)
        board.process_click(surface_size/3, surface_size * 0.7)
        board.process_click(surface_size * 0.3, surface_size/2)
        ans = True
        self.assertEqual(board.game_over, ans)

    def test_check_player_1_wins(self):
        """
        Unit test to check when player 1 wins.
        :return:
        """
        pygame.init()
        board = Board(grid_size=3, box_size=100, border=50, line_width=10)
        surface_size = board.surface.get_height()

        # sets the board for gameover state
        board.process_click(surface_size/2, surface_size/2)
        board.process_click(surface_size/2, surface_size * 0.7)
        board.process_click(surface_size * 0.7, surface_size/2)
        board.process_click(surface_size/3, surface_size * 0.7)
        board.process_click(surface_size * 0.3, surface_size/2)
        ans = 1
        self.assertEqual(board.check_for_winner(), ans)

    def test_check_player_2_wins(self):
        """
        Unit test to check when player 2 wins
        :return:
        """
        pygame.init()
        board = Board(grid_size=3, box_size=100, border=50, line_width=10)
        surface_size = board.surface.get_height()

        # sets the board for gameover state
        board.process_click(surface_size * 0.3, surface_size * 0.5)
        board.process_click(surface_size * 0.7, surface_size * 0.3)
        board.process_click(surface_size * 0.5, surface_size * 0.5)
        board.process_click(surface_size * 0.7, surface_size * 0.5)
        board.process_click(surface_size * 0.3, surface_size * 0.7)
        board.process_click(surface_size * 0.7, surface_size * 0.7)
        ans = 2
        self.assertEqual(board.check_for_winner(), ans)


if __name__ == "__main__":
    unittest.main()


# OUTPUT
# ..
# ----------------------------------------------------------------------
# Ran 2 tests in 0.995s
#
# OK

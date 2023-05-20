import math

from board import Board
import time
import random


# GAME LINK
# http://kevinshannon.com/connect4/


def main():
    board = Board()

    time.sleep(2)
    game_end = False
    while not game_end:
        (game_board, game_end) = board.get_game_grid()

        # FOR DEBUG PURPOSES

        # YOUR CODE GOES HERE

        # Insert here the action you want to perform based on the output of the algorithm
        # You can use the following function to select a column

        # print("Selected column: " + str(random_column))
        # board.print_grid(game_board)

        col, minimax_score = board.minimax(game_board, 6, -math.inf, math.inf, True, True)
        # print(game_board)

        if board.is_valid_location(game_board, col):
            board.select_column(col)

            # pygame.time.wait(500)
            row = board.get_next_open_row(game_board, col)

            board.drop_piece(game_board, row, col, 1)
            board.print_grid(game_board)

        time.sleep(2)
        # board.print_grid(game_board)


if __name__ == "__main__":
    main()

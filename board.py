import math
import random

from PIL import ImageGrab
import pyautogui

# YOU MAY NEED TO CHANGE THESE VALUES BASED ON YOUR SCREEN SIZE
LEFT = 583
TOP = 225
RIGHT = 1336
BOTTOM = 864

EMPTY = 0
RED = 1
BLUE = 2
AI = RED
PLAYER = BLUE
ROW_COUNT = 6
COLUMN_COUNT = 7


def calculate_score(_list, piece):
    if piece == RED:
        opponent_piece = BLUE
    else:
        opponent_piece = RED
    score = 0
    c_score = 0
    o_score = 0
    for i in _list:
        # if i == EMPTY and c_score > 2:
        #     score += c_score ** 4
        # if i == EMPTY and o_score > 2:
        #     score -= o_score ** 4
        if i == piece:
            score -= o_score ** 3
            o_score = 0
            c_score += 1
            if c_score == 4:
                score = 100000
                return score
        elif i == opponent_piece:
            score += c_score ** 3
            c_score = 0
            o_score += 1
            if o_score == 4:
                score = -100000
                return score
        else:
            score -= o_score ** 3
            score += c_score ** 3
            c_score = 0
            o_score = 0
    # Calculate score based on the previous iteration
    score -= o_score ** 2
    score += c_score ** 2
    # score += (c_score **2) *_list.count(EMPTY) * .1
    # score -= (c_score **2) *_list.count(EMPTY) * .1
    return score


class Board:
    def __init__(self) -> None:
        self.board = [[EMPTY for i in range(7)] for j in range(6)]

    def drop_piece(self, b, row, col, piece):
        b[row][col] = piece

    def is_valid_location(self, b, col):
        return b[0][col] == 0

    def get_next_open_row(self, b, col):
        for r in reversed(range(6)):
            if b[r][col] == 0:
                return r

    def get_valid_locations(self, b):
        valid_locations = []
        for col in range(COLUMN_COUNT):
            if self.is_valid_location(b, col):
                valid_locations.append(col)
        return valid_locations

    def print_grid(self, grid):
        print(grid)
        for i in range(0, len(grid)):
            for j in range(0, len(grid[i])):
                if grid[i][j] == EMPTY:
                    print("*", end=" \t")
                elif grid[i][j] == RED:
                    print("R", end=" \t")
                elif grid[i][j] == BLUE:
                    print("B", end=" \t")
            print("\n")

    def _convert_grid_to_color(self, grid):
        for i in range(0, len(grid)):
            for j in range(0, len(grid[i])):
                if grid[i][j] == (255, 255, 255):
                    grid[i][j] = EMPTY
                elif grid[i][j][0] > 200:
                    print("RED FOUND")
                    grid[i][j] = RED
                elif grid[i][j][0] > 45:
                    grid[i][j] = BLUE
        return grid

    def _get_grid_cordinates(self):
        startCord = (54, 53)
        cordArr = []
        for i in range(0, 7):
            for j in range(0, 6):
                x = startCord[0] + i * 110
                y = startCord[1] + j * 109
                cordArr.append((x, y))
        return cordArr

    def _transpose_grid(self, grid):
        return [[grid[j][i] for j in range(len(grid))] for i in range(len(grid[0]))]

    def _capture_image(self):
        image = ImageGrab.grab()
        cropedImage = image.crop((LEFT, TOP, RIGHT, BOTTOM))
        return cropedImage

    def _get_grid_cordinates_for_click(self):
        startCord = (54, 53)
        cordArr = []
        for i in range(0, 6):
            for j in range(0, 7):
                x = startCord[0] + i * 110
                y = startCord[1] + j * 109
                cordArr.append((x, y))
        return cordArr

    def _convert_image_to_grid(self, image):
        pixels = [[] for i in range(7)]
        i = 0
        for index, cord in enumerate(self._get_grid_cordinates()):
            pixel = image.getpixel(cord)
            if index % 6 == 0 and index != 0:
                i += 1
            pixels[i].append(pixel)
        return pixels

    def _get_grid(self):
        cropedImage = self._capture_image()
        pixels = self._convert_image_to_grid(cropedImage)
        # save the image to the disk with unique name
        cropedImage.save("image" + str(random.randint(0, 100)) + ".png")
        # cropedImage.show()
        # exit();
        grid = self._transpose_grid(pixels)
        return grid

    def _check_if_game_end(self, grid):
        for i in range(0, len(grid)):
            for j in range(0, len(grid[i])):
                if grid[i][j] == EMPTY and self.board[i][j] != EMPTY:
                    return True
        return False

    def get_game_grid(self):
        game_grid = self._get_grid()
        new_grid = self._convert_grid_to_color(game_grid)
        is_game_end = self._check_if_game_end(new_grid)
        self.board = new_grid
        return (self.board, is_game_end)

    # def select_column(self, column):
    #     print("selecting column", column)
    #     pyautogui.click(
    #         self._get_grid_cordinates()[column][1] + LEFT,
    #         self._get_grid_cordinates()[column][0] + TOP,
    #     )
    #     # pyautogui.click(
    #     #     self._get_grid_cordinates()[column][0] + LEFT,
    #     #     self._get_grid_cordinates()[column][1] + TOP,
    #     # )

    def select_column(self, column):
        pyautogui.click(
            self._get_grid_cordinates_for_click()[column][1] + LEFT,
            self._get_grid_cordinates_for_click()[column][0] + TOP,
        )

    def minimax(self, b, depth, alpha, beta, maximizingPlayer):
        valid_locations = self.get_valid_locations(b)
        is_terminal = len(valid_locations) == 0 or self.winning_move(b, AI) or self.winning_move(b, PLAYER)
        if depth == 0 or is_terminal:
            if is_terminal:
                if self.winning_move(b, AI):
                    return None, 100000
                elif self.winning_move(b, PLAYER):
                    return None, -100000
                else:  # Game is over, no more valid moves
                    return None, 0
            else:  # Depth is zero
                return None, self.score_position(b, AI)
            # return None, self.score_position(b, AI)
        elif maximizingPlayer:
            value = -100000
            column = random.choice(valid_locations)
            # print("valid locations------------------------", valid_locations)
            for col in valid_locations:
                row = self.get_next_open_row(b, col)
                b_copy = [row[:] for row in b]
                self.drop_piece(b_copy, row, col, AI)
                new_score = self.minimax(b_copy, depth - 1, alpha, beta, False)[1]
                if new_score > value:
                    value = new_score
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return column, value
        else:
            value = 100000
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = self.get_next_open_row(b, col)
                b_copy = [row[:] for row in b]

                self.drop_piece(b_copy, row, col, PLAYER)

                new_score = self.minimax(b_copy, depth - 1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return column, value

    def score_position(self, b, piece):
        # Score Horizontal
        score = 0

        # loop through board horizontally
        for row_array in b:
            score += calculate_score(row_array, piece)

        # Score Vertical
        for c in range(7):
            col_array = [b[r][c] for r in range(6)]
            score += calculate_score(col_array, piece)

        # Score diagonal
        n = len(b)
        diagonals_1 = []  # lower-left-to-upper-right diagonals
        diagonals_2 = []  # upper-left-to-lower-right diagonals
        for p in range(2 * n - 1):
            diagonal_1 = [b[p - q][q] for q in range(max(0, p - n + 1), min(p, n - 1) + 1)]
            diagonal_2 = [b[n - p + q - 1][q] for q in range(max(0, p - n + 1), min(p, n - 1) + 1)]
            if len(diagonal_1) > 1:
                diagonals_1.append(diagonal_1)
            if len(diagonal_2) > 1:
                diagonals_2.append(diagonal_2)
        for diagonal in diagonals_1 + diagonals_2:
            score += calculate_score(diagonal, piece)

        return score

    # def winning_move(self, b, piece):
    #     score = 0
    #     # loop through board horizontally
    #     for row_array in b:
    #         score += calculate_score(row_array, piece)
    #
    #
    #     # Score Vertical
    #     # loop through board vertically
    #     # print("c_score",c_score)
    #     for c in range(7):
    #         col_array = [b[r][c] for r in range(6)]
    #         # print(col_array)
    #         score += calculate_score(col_array, piece)
    #
    #     # Score Diagonal
    #     # loop through board diagonally
    #     n = len(b)
    #     diagonals_1 = []  # lower-left-to-upper-right diagonals
    #     diagonals_2 = []  # upper-left-to-lower-right diagonals
    #     for p in range(2 * n - 1):
    #         diagonals_1.append([b[p - q][q] for q in range(max(0, p - n + 1), min(p, n - 1) + 1)])
    #         diagonals_2.append([b[n - p + q - 1][q] for q in range(max(0, p - n + 1), min(p, n - 1) + 1)])
    #
    #     for diagonal in diagonals_1 + diagonals_2:
    #         score += calculate_score(diagonal, piece)
    #
    #     if score >= 100000:
    #         return True
    #     else:
    #         return False
    #     # return score

    def winning_move(self, board, piece):
        for c in range(7 - 3):
            for r in range(6):
                if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][
                    c + 3] == piece:
                    return True
        for c in range(7):
            for r in range(6 - 3):
                if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][
                    c] == piece:
                    return True

        for c in range(7 - 3):
            for r in range(6 - 3):
                if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and \
                        board[r + 3][c + 3] == piece:
                    return True

        for c in range(7 - 3):
            for r in range(3, 6):
                if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and \
                        board[r - 3][c + 3] == piece:
                    return True

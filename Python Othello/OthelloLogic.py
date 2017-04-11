# Othello Logic and Console Interface


class Game:
    """ An Othello game.
    """

    color_dict = {'black': 'B', 'white': 'W', 'none': ' '}

    def __init__(self, rows: int=8, cols: int=8, win_option: str='most',
                 starting_player: str='black', corner_color: str='white'):

        self.board = self._create_new_board(rows, cols, self.color_dict[corner_color])
        self.boardrows = rows
        self.boardcols = cols
        self.current_player = starting_player
        self.winstate_option = win_option

        self.current_player_piece = self.color_dict[self.current_player]
        self.black_score = 0
        self.white_score = 0

        self.update_player_scores()

    def printboard(self) -> None:
        """ Prints a textual representation of the board to the console.
            Includes both players' scores.
        """
        print(' ', end=' ')                 # print out column guides at the top
        for i in range(self.boardcols):
            print(i + 1, end=' ')
        print()

        cnt = 1
        for row in self.board:
            print('{} '.format(cnt), end='')  # print out row guides at the left
            cnt += 1
            for col in row:
                if col == ' ':
                    print('.', end=' ')
                else:
                    print(col, end=' ')
            print()

        print('Black: {}  White: {}'.format(self.black_score, self.white_score))

    def move_phase(self, row: int, col: int) -> None:
        """ Puts down a piece for the current player in space (row, col). If the space is already occupied, raises an
            OverlapError exception. If the move is invalid, raises InvalidMoveError.
        """
        if self.board[row][col] != ' ':
            raise OverlapError
        elif not self._piece_check(row, col, 'move'):
            raise InvalidMoveError
        else:   # This block can raise an IndexError if row or col exceeds the board's coordinates
            self.board[row][col] = self.current_player_piece

    def flip_phase(self, row: int, col: int) -> None:
        """ Goes through the board and flips all the lines that the piece played at (row, col) has created.
        """
        inline_pieces_list = self._get_valid_lines(row, col, self.current_player_piece)

        for rowcol in inline_pieces_list:
            self._flip_line(row, col, rowcol[0], rowcol[1])

    def change_player_phase(self) -> None:
        """ Changes all current-player-related variables to the next player (
        """
        self.current_player = self._flip_color(self.current_player)
        self.current_player_piece = self.color_dict[self.current_player]

    def player_has_moves(self) -> bool:
        """ Looks at the current player's pieces and sees if there are any moves available
        """
        result = False
        for row_index in range(self.boardrows):
            for col_index in range(self.boardcols):
                if self.board[row_index][col_index] == self.current_player_piece:
                    result = self._piece_check(row_index, col_index, 'open')
                    if result:
                        return result

        return result

    def determine_winner(self) -> str:
        """ Take the selected game mode into account and returns the winner of the game at the time it's called
        """
        if self.black_score > self.white_score:
            if self.winstate_option == 'most':
                return 'Black is the winner!'
            elif self.winstate_option == 'least':
                return 'White is the winner!'
        elif self.black_score < self.white_score:
            if self.winstate_option == 'most':
                return 'White is the winner!'
            elif self.winstate_option == 'least':
                return 'Black is the winner!'
        elif self.black_score == self.white_score:
            return 'It\'s a tie!'

    def update_player_scores(self) -> None:
        """ Goes through the board and counts the total number of pieces of both colors
        """
        b_total = 0
        w_total = 0

        for row in self.board:
            for col in row:
                if col == 'B':
                    b_total += 1
                elif col == 'W':
                    w_total += 1

        self.black_score = b_total
        self.white_score = w_total

    def _piece_check(self, row: int, col: int, mode: str) -> bool:
        """ Looks at all 8 directions from a piece. If mode == 'open', comparator = ' ' and function checks for valid
            open spaces for the current player. If mode == 'move', comparator = current_player and function checks for
            pieces of the same color in line with the piece.
        """
        comparator = None
        if mode == 'open':
            comparator = ' '
        elif mode == 'move':
            comparator = self.current_player_piece

        lines_list = self._get_valid_lines(row, col, comparator)

        if len(lines_list) > 0:
            return True
        else:
            return False

    def _get_valid_lines(self, row: int, col: int, comparator: str) -> [tuple]:
        """ Checks for valid pieces in line with the piece at (row, col) and returns their coordinates. If no valid
            lines were created, returns an empty list.
        """
        return_list = []

        left_check = self._single_direction_check(row, col, 0, -1, comparator)
        right_check = self._single_direction_check(row, col, 0, 1, comparator)
        up_check = self._single_direction_check(row, col, -1, 0, comparator)
        down_check = self._single_direction_check(row, col, 1, 0, comparator)
        upright_check = self._single_direction_check(row, col, -1, 1, comparator)
        downright_check = self._single_direction_check(row, col, 1, 1, comparator)
        downleft_check = self._single_direction_check(row, col, 1, -1, comparator)
        upleft_check = self._single_direction_check(row, col, -1, -1, comparator)

        temp_list = [left_check, right_check, up_check, down_check,
                     upright_check, downright_check, downleft_check, upleft_check]

        for item in temp_list:
            if len(item) > 0:
                return_list.append(item)

        return return_list
        
    def _single_direction_check(self, row: int, col: int, row_change: int, col_change: int, comparator: str) -> tuple:
        """ Using row_change and col_change to determine the direction. If there is a valid space/piece to move in that
            column, returns those coordinates as a tuple. If the move is not valid, returns an empty tuple
        """
        valid_spot = tuple()

        opposite_color = self.color_dict[self._flip_color(self.current_player)]
        opposite_color_line = False
        col_index = col
        row_index = row

        # can optimize?
        while 0 <= col_index < self.boardcols and 0 <= row_index < self.boardrows:
            if self.board[row_index][col_index] == opposite_color:
                opposite_color_line = True
            elif self.board[row_index][col_index] == comparator and opposite_color_line:
                valid_spot = (row_index, col_index)
                break

            # When searching for possible moves ('open'), if after finding an opposite-color piece the next one is not
            # still opposite-color, then it's as if there was no opposite-color piece in between; returns (), "false"
            elif self.board[row][col] == self.board[row_index][col_index] and opposite_color_line and comparator == ' ':
                break

            # return nothing (false) if the next same-color piece is right next to to the spot being checked
            elif (abs(row_index - row) == 1 or abs(col_index - col) == 1) and not opposite_color_line:
                break

            # return nothing (false) if there is a blank space in the line
            elif self.board[row_index][col_index] == ' ' and row_index != row or col_index != col:
                break
            row_index += row_change
            col_index += col_change

        return valid_spot

    def _flip_line(self, row1: int, col1: int, row2: int, col2: int) -> None:
        """ Takes the coordinates of 2 pieces of the same color (must be in a row with each other) and flips the color
            of any pieces in between. Starts at (row1, col1) and moves towards (row2, col2)
        """
        row_change = 0
        col_change = 0
        row_index = row1
        col_index = col1

        if row1 - row2 < 0:
            row_change = 1
        elif row1 - row2 > 0:
            row_change = -1

        if col1 - col2 < 0:
            col_change = 1
        elif col1 - col2 > 0:
            col_change = -1

        while min(row1, row2) <= row_index <= max(row1, row2) and min(col1, col2) <= col_index <= max(col1, col2):
            self.board[row_index][col_index] = self.current_player_piece
            row_index += row_change
            col_index += col_change

    def update_score(self) -> None:
        """ Counts the number of black and white pieces on the board and stores those in self.black_score and self.white_score
        """
        bscore = 0
        wscore = 0
        for row in self.board:
            for col in row:
                if col == 'B':
                    bscore += 1
                elif col == 'W':
                    wscore += 1

        self.black_score = bscore
        self.white_score = wscore

    # -------- Static Methods --------

    @staticmethod
    def _flip_color(color: str) -> str:
        """ Returns the opposite color of the string passed. (used for changing self.current_player and flipping pieces)
        """
        if color == 'black':
            return 'white'
        elif color == 'white':
            return 'black'

    @staticmethod
    def _create_new_board(row_amt: int, col_amt: int, left_corner_color: str) -> [[str]]:
        """ Creates a new board with specified starting gamestate
            :param row_amt: integer from 4 to 16 divisible by 2
            :param col_amt: integer from 4 to 16 divisible by 2
            :param left_corner_color: 'B' or 'W'; determines the starting layout of the game board
            :return: 2 dimensional list with 2 black and 2 white pieces arranged for a new game; top left is (0, 0)
        """
        board = []
        for i in range(row_amt):
            row = []
            for j in range(col_amt):
                row.append(' ')
            board.append(row)

        right_corner_color = None

        if left_corner_color == 'B':
            right_corner_color = 'W'
        elif left_corner_color == 'W':
            right_corner_color = 'B'

        board[row_amt // 2 - 1][col_amt // 2 - 1] = left_corner_color
        board[row_amt // 2 - 1][col_amt // 2] = right_corner_color
        board[row_amt // 2][col_amt // 2 - 1] = right_corner_color
        board[row_amt // 2][col_amt // 2] = left_corner_color

        return board


# -------- Exceptions --------


class OverlapError(Exception):
    def __str__(self):
        return 'OverlapError: A piece has already been placed at this location.'


class InvalidMoveError(Exception):
    def __str__(self):
        return 'InvalidMoveError: Piece cannot be placed at this location.'

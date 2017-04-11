# Othello Command Line Version

import OthelloLogic


def main() -> None:
    """ main program
    """

    game = _start_new_game()

    print()

    black_has_moves = True
    white_has_moves = True

    while True:
        game.printboard()
        print('It is {}\'s turn.'.format(game.current_player))

        if black_has_moves is not white_has_moves:  # exclusive or
            print('{} has no available moves.\n'.format(game.current_player.capitalize()))

            game.change_player_phase()

            if game.current_player == 'black':
                black_has_moves = game.player_has_moves()
            elif game.current_player == 'white':
                white_has_moves = game.player_has_moves()

            if not black_has_moves and not white_has_moves:
                print('Neither player has any available moves.\n')
                break
            else:
                game.printboard()
                print('It is {}\'s turn.'.format(game.current_player))

        # get player move
        while True:
            try:
                row_col = _get_move_input()
                game.move_phase(row_col[0], row_col[1])
            except OthelloLogic.OverlapError:
                print('Invalid move, a piece is already in that spot.')
            except OthelloLogic.InvalidMoveError:
                print('Invalid move, piece does not create a valid line with another piece.')
            except IndexError:
                print('Invalid move, coordinates outside of board.')
            else:
                break

        game.flip_phase(row_col[0], row_col[1])

        game.update_player_scores()

        game.change_player_phase()

        if game.current_player == 'black':
            black_has_moves = game.player_has_moves()
        elif game.current_player == 'white':
            white_has_moves = game.player_has_moves()

        print()

    game.printboard()
    print(game.determine_winner())
    print()


def _start_new_game() -> OthelloLogic.Game:
    """ Asks the user for a default or custom gameboard; if 'default' is chosen, options are an 8x8 board,
        most discs wins, black starts, and white is in the top-left corner of the starting layout;
        Else, prompts the user for custom options
        :return: Game object
    """
    while True:
        boardtype = input('[Default] or [custom] board?: ').strip().lower()

        if boardtype == 'default':
            return OthelloLogic.Game()

        elif boardtype == 'custom':
            rows = int(_get_game_option_input('rows', ['4', '6', '8', '10', '12', '14', '16']))
            cols = int(_get_game_option_input('cols', ['4', '6', '8', '10', '12', '14', '16']))
            starting_player = _get_game_option_input('starting player', ['black', 'white'])
            corner_start_player = _get_game_option_input('corner color', ['black', 'white'])
            win_type = _get_game_option_input('win type', ['most', 'least'])

            return OthelloLogic.Game(rows, cols, win_type, starting_player, corner_start_player)

        else:
            print('Invalid input.')


def _get_game_option_input(option: str, valid_options_list: list) -> str:
    """ Keeps prompting user for specified option until the user gives a valid option.
        :param option: one of the five options needed for a custom gameboard
        :param valid_options_list: list of accepted inputs
        :return: valid input for that option, in string format
    """
    prompt_dict = {'rows': 'Number of rows (4-16, evens only): ', 'cols': 'Number of columns (4-16, evens only): ',
                   'win type': 'Gametype (most/least): ', 'starting player': 'Starting player (black/white): ',
                   'corner color': 'Starting left corner color (black/white): '}

    while True:
        choice = input(prompt_dict[option]).strip().lower()
        if choice not in valid_options_list:
            print('Invalid input.')
        else:
            return choice


def _get_move_input() -> tuple:
    """ Asks the user for a valid coordinate input until it is valid.
        :return: a tuple of ints; (row_coord, col_coord)
    """
    move_row = None
    move_col = None

    while True:
        try:
            raw_move_coords = input('Enter row # and column #, separated by a space: ').strip().split()
            move_row = int(raw_move_coords[0])
            move_col = int(raw_move_coords[1])
            if move_row > 0 and move_col > 0:
                move_row -= 1
                move_col -= 1
            else:
                print('Please enter integers above 0.')
                continue
        except IndexError:
            print('Please separate each number with a space.')
        except ValueError:
            print('Please enter only integers.')
        else:
            break

    return move_row, move_col

if __name__ == '__main__':
    while True:
        main()
        replay = input('Play again? (y/n): ').strip().lower()
        if replay not in ['y', 'yes']:
            break

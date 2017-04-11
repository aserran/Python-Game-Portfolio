# connectfour_ui.py


import connectfour
        
def draw_current_board(game_state:connectfour.ConnectFourGameState) -> "updated board":
    '''
    Draw the current game board according to each player's move
    '''
    game_board, turns = game_state[0], game_state[1]
    for number in range(1,connectfour.BOARD_COLUMNS+1,1):
        print (number, end = "  ")
    print ()    
    for row in range(connectfour.BOARD_ROWS):
        for column in range(connectfour.BOARD_COLUMNS):
            if game_board[column][row] == 0:
                print (".", end = "  ")
            elif game_board[column][row] == 1:
                print ("R", end = "  ")
            elif game_board[column][row] == 2:
                print ("Y", end = "  ")
        print ()
    if game_state[1] == 1:
        print ("It's RED turn")
    elif game_state[1] ==2:
        print ("It's YELLOW turn")


def move_input() -> "move:str,column_number:int":
    '''
    Ask users to clarify their moves, and check if they are valid.
    Different errors will have different messages to help notify users.
    '''
    while True:
        move = input("Type 'DROP' or 'POP' to clarify your move: ")
        if move == "DROP" or move == "POP":
            break
        else:
            print ("Not a valid move. (Not 'DROP' or 'POP')")
    while True:
        try:
            column_number = int(input("Type an integer to clarify which column you want to make a move:  "))
        except:
            print ("Not a valid column number. (Not an integer)")
        if column_number >0 and column_number <= connectfour.BOARD_COLUMNS:
            break
        else:
            print ("Not a valid column number. (Out of range)")
    return move,column_number

def move(action:str,column_number:int,game_state:connectfour.ConnectFourGameState) -> connectfour.ConnectFourGameState:
    '''
    Update the game state according to players' move.
    '''
    if action == "DROP":
        try:
            current_game_state = connectfour.drop_piece(game_state,column_number-1)
        except:
            print ("Not a valid move. (The column is full)")
            return game_state
    elif action == "POP":
        try:
            current_game_state = connectfour.pop_piece(game_state,column_number-1)
        except:
            print ("Not a valid move. (The column is empty or the piece belongs to the other player)")
            return game_state
    return current_game_state
                

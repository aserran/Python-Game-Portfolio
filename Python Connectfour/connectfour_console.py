# connectfour_console.py

import connectfour
import connectfour_ui

def main():
    '''
    Main function flow.
    '''
    connectfour_ui.draw_current_board(connectfour.new_game_state())
    current_game_state = connectfour.new_game_state()
    while True:
        if connectfour.winning_player(current_game_state) == 1 :
            print ("The winner is RED!")
            break
        elif connectfour.winning_player(current_game_state) == 2 :
            print ("The winner is YELLOW!")
            break
        move,column_number = connectfour_ui.move_input()
        current_game_state = connectfour_ui.move(move,column_number,current_game_state)
        connectfour_ui.draw_current_board(current_game_state)

if __name__ == '__main__':
    main()
            

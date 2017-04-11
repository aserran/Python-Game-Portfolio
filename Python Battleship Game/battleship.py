#Beginning of game

import random
def make_board ():
    columns = []
    rows = ["-","-","-","-","-","-","-","-","-","-"]
    i = 0
    while (i < 10):
        columns.append(list(rows))
        i += 1

    gameboard = columns
    return gameboard

def display_board(gameboard:list):
    columns = [" ","0","1","2","3","4","5","6","7","8","9"]
    rows = ['A','B','C','D','E','F','G','H','I','J']
    index = 0
    print("  ".join(num for num in columns))
    for row in gameboard:
        print(rows[index] + "  " + "  ".join(r for r in row))
        index+=1
           
def put_ships(gameboard, ship_file):
    infile = open(ship_file)
    moves = infile.readlines()
    for line in moves:
        moves = line.split(',')
        moves.pop(0)
        for move in moves:
            make_move(move[0],move[1],gameboard, "*")
    infile.close()

def make_move(row:str, col:str, gameboard, symbol:str):
    row_letters = {'A':0, 'B':1, 'C':2 , 'D':3, 'E':4 , 'F':5, 'G':6 , 'H':7, 'I':8, 'J':9}
    gameboard[row_letters[row]][int(col)] = symbol

def isHit(row:str, col:str, gameboard):
    row_letters = {'A':0, 'B':1, 'C':2 , 'D':3, 'E':4 , 'F':5, 'G':6 , 'H':7, 'I':8, 'J':9}
    if gameboard[row_letters[row]][int(col)] == "*":
        return True
    else:
        return False

def starting_turn():
    num = random.randrange(0,2)
    if num == 0:
        return "p1"
    return "p2"
    
def change_turn(turn:str):
    if turn == "p1":
        return "p2"
    return "p1"

def start_game(p1_ships, p2_ships):
    turn = starting_turn()
    player1_view = list(make_board())
    put_ships(player1_view, p1_ships)
    
    player2_view = list(make_board())
    put_ships(player2_view, p2_ships)

    game_loop(player1_view, player2_view, turn)

def all_boats_hit(gameboard):
    for rows in gameboard:
        if "*" in rows:
            return False
    return True

def print_stats(p1_board, p2_board, p1file, p2file):
    row_letters = {'A':0, 'B':1, 'C':2 , 'D':3, 'E':4 , 'F':5, 'G':6 , 'H':7, 'I':8, 'J':9}
    print("Player 1 Ships HP\t Player 2 Ships HP")
    p1 = open(p1file)
    p2 = open(p2file)

    player1 = p1.readlines()
    player2 = p2.readlines()
          
    p1_stats = ''
    p2_stats = ''
    stats = "{:}\t\t\t{:}"
    
    for line_p1 in player1:
        health = 0
        moves = line_p1.split(',')
        p1_stats += moves[0] + ' - '
        moves.pop(0)
        for m in moves:
            if p1_board[row_letters[m[0]]][int(m[1])] == "*":
                health+=1
        p1_stats += str(health) + '\n'

    for line_p2 in player2:
        health = 0
        moves = line_p2.split(',')
        p2_stats += moves[0] + ' - '
        moves.pop(0)
        for m in moves:
            if p2_board[row_letters[m[0]]][int(m[1])] == "*":
                health+=1
        p2_stats += str(health) + '  \n\t\t\t'

    print(stats.format(p1_stats,p2_stats))
    p1.close()
    p2.close()
    
def game_loop(p1_board, p2_board, turn):
    while True:
        if turn == "p1":
            print("Player 1's Turn")
            display_board(p1_board)
            print_stats(p1_board, p2_board, "p1.txt", "p2.txt")
            move = input("Please enter coordinates player1[A-J][0-9]: ")
            display_board(p1_board)
            turn = change_turn(turn)
            
            
            if isHit(move[0], move[1], p2_board) == True:
                print("That's a hit!")
                make_move(move[0], move[1], p2_board, "X")
                make_move(move[0], move[1], p1_board, "H")
            else:
                print("That's a miss!")
                make_move(move[0], move[1], p1_board, "M")
        
            if (all_boats_hit(p2_board)):
                print("Player 1 wins")
                return False

        elif turn == "p2":
            print("Player 2's Turn")
            display_board(p2_board)
            print_stats(p1_board, p2_board, "p1.txt", "p2.txt")
            move = input("Please enter coordinate player2 [A-J][0-9]: ")
            display_board(p2_board)
            turn = change_turn(turn)
    

            if isHit(move[0], move[1], p1_board) == True:
                print("That's a hit!")
                make_move(move[0], move[1], p1_board, "X")
                make_move(move[0], move[1], p2_board, "H")
            else:
                print("That's a miss!")
                make_move(move[0], move[1], p2_board, "M")
            
            if (all_boats_hit(p1_board)):
                print("Player 2 wins")
                return False

            
def save_gameoption():
    GameFile= open('game.txt', 'w')
    GameFile.close()
        

    
def main():
    print("--------- BATTLESHIP! ----------\n")
    command = input("N:\tNew Game\nQ:\tQuit\nEnter command:")    
    if command == "N":
        start_game("p1.txt", "p2.txt")
    elif command == "Q":
        return
                                    
                                 
    
main()

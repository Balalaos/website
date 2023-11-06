import random


# This class is responsible for Battleship game.
# It has 2 boards - player and computer board.
# Boards have following elements: 
#                 " " - empty field
#                 "X" - hit ship
#                 "O" - alive ship
#                 "*" - missed shot
# TODO: add intellect for computer
class Battleship():
    def __init__(self) -> None:
        self.board_enemy = [[" " for j in range(10)] for i in range(10)]
        self.board_player =  [[" " for j in range(10)] for i in range(10)]
        self.end_game = False
        self.message = ''
    
    
    # Error messages
    class Error(Exception):
        def __init__(self, message="Unexpected error"):
            super().__init__(message)
    
        
    # Function for sending board data
    def get_board(self):
        return self.board_player, self.board_enemy
    
    
    # This function resets game and board
    def reset(self):
        self.board_enemy = [[" " for j in range(10)] for i in range(10)]
        self.board_player =  [[" " for j in range(10)] for i in range(10)]
        self.end_game = False
        self.message = ''
        return self.board_player, self.board_enemy
    
    
    # This function reads input click and update the board. Moreover, it calculates move for computer
    # Input: data of input click
    # Return: player board
    #         computer board
    #         error message 
    def game(self, data):
        message = ""
        # Checks if game is ended
        if self.end_game:
            return self.board_player, self.board_enemy, self.message
        
        # Checks where was a shoot made and updates a board if needed
        # If ship was shot or user clicked in already shot place returns error message
        try:
            self.make_a_shot_player(data) 
        except self.Error as e:
            # Checks if player won
            if self.check_winner(self.board_enemy):
                self.end_game = True
                self.message = "Winner is player"
                return self.board_player, self.board_enemy, self.message 
            else:
                # Sends error message
                raise self.Error(e)
        
        # Make a move for computer 
        self.make_a_shot_computer()
        # Checks if computer won
        if self.check_winner(self.board_player):
            self.end_game = True
            self.message = "Winner is computer"
            message = self.message
               
        return self.board_player, self.board_enemy, message
    
    
    # This function checks if there still not shoted ships on the board
    # Input: board 
    # Return: True boolean if all ships are shooted
    #         False boolean if there still are ships
    def check_winner(self, board):
        # Check if there are ships. O value on board is mean ship
        for i in range(10):
            for j in range(10):
                if board[i][j] == "O":
                    return False
        return True
    
    
    # This function checks if player shot the ship or not
    # Input: data of input click 
    def make_a_shot_player(self, data):
        # Take coordinates of a shoot
        place, *_ = data
        place = int(place)
        x = place // 10
        y = place % 10
        
        # Check if player already shot on this place
        if self.board_enemy[x][y] == "X" or self.board_enemy[x][y] == "*":
            raise self.Error("You already shoot there")
        
        # Check if player shot in ship
        elif self.board_enemy[x][y] == "O":
            self.board_enemy[x][y] = "X"
            # Check if player killed whole ship
            if self.check_kill(self.board_enemy, x, y, x, y):
                # Create a circle around the killed ship
                self.kill_circle(self.board_enemy, x, y, x, y)
                raise self.Error("KILL!!!! Shoot another ship!")  
            else:
                raise self.Error("STRIKE!!!! You shooted the ship. Make another shoot!")
        elif self.board_enemy[x][y] == " ":
            self.board_enemy[x][y] = "*"
    
    
    # This function make a shoot for computer. Computer shoots in random place.
    # TODO: add intellect
    def make_a_shot_computer(self):
        # Computer choose random coordinate until it shoots in empty field
        while True:
            # Random coordinate
            x = random.randint(0, 9)
            y = random.randint(0, 9)
            
            # If random place was already shot, computer shoots again
            if self.board_player[x][y] == "X" or self.board_player[x][y] == "*":
                continue
            # If computer shoots in ship, it shoots again 
            elif self.board_player[x][y] == "O":
                self.board_player[x][y] = "X"
                # Check if computer killed whole ship
                if self.check_kill(self.board_player, x, y, x, y):
                    # Create a circle around the killed ship
                    self.kill_circle(self.board_player, x, y, x, y)
                continue
            # If computer misses, a turn goes to player
            elif self.board_player[x][y] == " ":
                self.board_player[x][y] = "*"
            break
        

    # This function draw a circle around killed ship
    # Input:    board 
    #           x, y = x and y coordinates of place around what circle should be drawn 
    #           x_old, y_old = x and y of coordinates of previous place around what circle was drawn 
    # Return:   board       
    def kill_circle(self, board, x, y, x_old, y_old):
        # Checks every field around the shot place
        for i in range(3):
            for j in range(3):
                m = x+i-1
                n = y+j-1
                # Control if coordinates are in the board
                if m < 0 or m > 9 or n < 0 or n > 9:
                    continue
                # Draw a missed shot on empty place
                if board[m][n] != "X":
                    board[m][n] = "*"
                else:
                    # If near is another ship hit field, draw circle around it
                    if not (m == x and n == y or m == x_old and n == y_old):
                        self.kill_circle(board, m, n, x, y)
        return board


    # This function check if whole ship was killed
    # Input:    board 
    #           x, y = x and y coordinates of place what should be checked 
    #           x_old, y_old = x and y of coordinates of previous place what was checked
    # Return:   board 
    def check_kill(self, board, x, y, x_prev, y_prev):
        for i in range(3):
            for j in range(3):
                m = x+i-1
                n = y+j-1
                # Checks if field was already in use
                if m == x and n == y or m == x_prev and n == y_prev:
                    continue
                # Control if coordinates are in the board
                if m < 0 or m > 9 or n < 0 or n > 9:
                    continue
                # Check if ship killed
                if 'O' == board[m][n]:
                    return False
                if "X" == board[m][n]:
                    # If near is another ship hit field, check it as well
                    if not self.check_kill(board, m, n, x, y):
                        return False
        return True
    
    
    # This makes the board fields for enemy and player and arrange ships on it
    # Return:   player board    
    def make_field(self):
        self.auto_ships(self.board_player)
        self.auto_ships(self.board_enemy)
        return self.board_player
    
    
    # This arrange all ships on board
    # Input:    board 
    # Return:   board 
    def auto_ships(self, board):
        # Create one 4-square ship
        board = self.add_ships_computer(board, 4)
        # Create two 3-square ship
        for i in range(2):
            board = self.add_ships_computer(board, 3)
        # Create three 2-square ship
        for i in range(3):
            board = self.add_ships_computer(board, 2)
        # Create four 1-square ship
        for i in range(4):
            board = self.add_ships_computer(board, 1)
        return board
    
    
    # This arrange ship on board
    # Input:    board 
    #           size of ship
    # Return:   board 
    def add_ships_computer(self, board, ship_size):
        control_x = False
        control_y = False
        x = 0
        y = 0
        
        while True:
            # finding random place for a ship
            while True:
                if not control_x:
                    x = random.randint(0, 9)
                if not control_y:
                    y = random.randint(0, 9)
                
                # Check if ship is go throw one of the wall
                if x + ship_size - 1 < 9:
                    control_x = True
                if y + ship_size - 1 < 9:
                    control_y = True
                    
                if control_x or control_y:
                    break
            
            # Check if ship is near wall
            if not control_x:
                size_way = "Down"
            elif not control_y:
                size_way = "Left"
            # If ship is not near the wall choose direction randomly
            else:
                size_way = random.randint(0, 1)
                if size_way == 0:
                    size_way = "Left"
                else:
                    size_way = "Down"
            
            # Draw ship down
            if size_way == "Down":
                # Check if there another ship on the way
                for i in range(ship_size):
                    check = self.check_ship(board, x, y+i)
                    if not check:
                        control_x = False
                        control_y = False
                        break
                if not check:
                    continue
                # Add ship
                for i in range(ship_size):
                    board[x][y+i] = "O"
                break
            
            # Draw ship left
            elif size_way == "Left":
                # Check if there another ship on the way
                for i in range(ship_size):
                    check = self.check_ship(board, x+i, y)
                    if not check:
                        control_x = False
                        control_y = False
                        break
                if not check:
                    continue
                # Add ship
                for i in range(ship_size):
                    board[x+i][y] = "O"  
                break
        return board
    
    
    # This functions checks if there ship on the way
    # Input:    board 
    #           x and y coordinates of field around what fields should be checked if there ship or not
    # Return:   True or False board 
    def check_ship(self, board, x, y):
        for i in range(3):
            for j in range(3):
                m = x+i-1
                n = y+j-1
                # Control if coordinates are in the board
                if m < 0 or m > 9 or n < 0 or n > 9:
                    continue
                # Check if there another ship
                if 'O' == board[m][n]:
                    return False
        return True

        
        
    

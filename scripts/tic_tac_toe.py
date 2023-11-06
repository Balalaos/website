# This class is responsible for Tic Tac Toe game
class TicTacToe():
    def __init__(self) -> None:
        self.board = ["","","","","","","","","",]
        self.current_player = "X"
        self.end_game = False
        self.message = ''

        
    # Function for sending board data
    def get_board(self):
        return self.board
    
    
    # This main game function of the game. It reads input click and update the board
    # Input: data of input click
    # Return: board
    #         error message 
    def game(self, data):
        # Check if game is ended
        if self.end_game:
            return self.board, self.message
        # Read an input field
        place, *_ = data
        place = int(place)
        # Check if field is free
        if self.board[place] == "":
            # Add player sign to the field
            self.board[place] = self.current_player
            # Check if game is ended
            self.check_winner()
            # Update next player
            self.current_player = "O" if self.current_player == "X" else "X"
        
        return self.board, self.message
        
        
    # This function resets game and board 
    def reset(self):
        self.board = ["","","","","","","","","",]
        self.current_player = "X"
        self.end_game = False
        self.message = ''
        return self.board
    
    
    # This function checks if one of the players is winner
    def check_winner(self):
        # All winning combinations
        win_combination = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
        
        # Check if one of the players made the winning combination
        for pos in win_combination:
            if self.board[pos[0]] == self.board[pos[1]] == self.board[pos[2]] != "":
                # Send message and end the game
                self.message = "Winner is player " + self.current_player
                self.end_game = True
                return
        
        # Check if all fields are filled, in this case that is a tie
        tie = True
        for pos in self.board:
            if pos == "":
                tie = False
        if tie:
            self.message = "It is a tie"

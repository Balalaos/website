class TicTacToe():
    def __init__(self) -> None:
        self.board = ["","","","","","","","","",]
        self.current_player = "X"
        self.end_game = False
        self.message = ''
    
    
    class Winner(Exception):
        def __init__(self):
            super().__init__()
        
    
    def get_board(self):
        return self.board
    
    
    def game(self, data):
        if self.end_game:
            return self.board, self.message
        place, *_ = data
        place = int(place)
        if self.board[place] == "":
            self.board[place] = self.current_player
            self.check_winner()
            self.current_player = "O" if self.current_player == "X" else "X"
        
        
        return self.board, self.message
        
        
    def reset(self):
        self.board = ["","","","","","","","","",]
        self.current_player = "X"
        self.end_game = False
        self.message = ''
        return self.board
    
    def check_winner(self):
        win_combination = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
        
        for pos in win_combination:
            if self.board[pos[0]] == self.board[pos[1]] == self.board[pos[2]] != "":
                self.message = "Winner is player " + self.current_player
                self.end_game = True
            
        tie = True
        for pos in self.board:
            if pos == "":
                tie = False
        if tie:
            self.message = "It is a tie"

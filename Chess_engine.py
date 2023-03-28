"""
It is reponsible for storing all the information about the current game state of a chess game. It will also determine valid moves at the current state. It will also keep move log. It will thus be able to look back at the game how it went.
"""
class GameState():
    def __init__ (self):
        # There are ways of creating board with numpy and libraries but that is when we are too much in AI stuff. Here it is fine with this hard coded board.
        # white perspective
        # board is an 8X8 two dimensional list and each element has 2 characters.
        # The first character represents colour b/w and second means the type of piece- KQRBNp
        #"--" means an empty space
        self.board=[
            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bp","bp","bp","bp","bp","bp","bp","bp"],
            ["--","--","--","--","--","--","--","--"], 
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wp","wp","wp","wp","wp","wp","wp","wp"],
            ["wR","wN","wB","wQ","wK","wB","wN","wR"]
        ] 
        self.whiteToMove=True
        self.moveLog= []
        # have to make sure that moving king and rook is registered for castling rights
    # Creating a function in chess engine now to finally make a move.
    def makeMove(self,move):
        self.board[move.startRow][move.startCol]="--"
        self.board[move.endRow][move.endCol]=move.pieceMoved
        # As of now assuming that move is valid- later on will checek and then play the move
        self.moveLog.append(move) # for pgn or undo 
        self.whiteToMove= not self.whiteToMove # change turns


class Move():
    # We have to make sure to validate the move too that's why board is also a parameter. We also have to store captured piece so that we can move back in moves.
    # useful mapping to actual chess notations
    ranksToRows={"1":7, "2":6,"3":5,"4":4,"5":3,"6":2,"7":1,"8":0}
    rowsToRanks={v: k for k, v in ranksToRows.items()} # cool way of reversing above
    filesToCols= {"a":0,"b":1,"c":2,"d":3,"e":4,"f":5,"g":6,"h":7 }
    colsToFiles={v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        # init access is for all functions
        self.startRow= startSq[0]
        self.startCol= startSq[1]
        self.endRow= endSq[0]
        self.endCol= endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        # This is just to get information of moves. We are not moving still.

    def getChessNotation(self):
        # Not the actual chess notation but will work for now. Improve later.
        return self.getRankAndFile(self.startRow, self.startCol) + self.getRankAndFile(self.endRow, self.endCol)
    
    def getRankAndFile(self,row,col):
        return self.colsToFiles[col] + self.rowsToRanks[row]
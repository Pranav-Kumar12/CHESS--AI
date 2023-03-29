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
    """ This will take move as parameter and executes it ( except for castling and en-passant and pawn promotion) """
    def makeMove(self,move):
        self.board[move.startRow][move.startCol]="--"
        self.board[move.endRow][move.endCol]=move.pieceMoved
        # As of now assuming that move is valid- later on will checek and then play the move
        self.moveLog.append(move) # for pgn or undo 
        self.whiteToMove= not self.whiteToMove # change turns
    """ Undo the latest move"""
    def undo_move(self):
        if len(self.moveLog)!=0: # making sure that a move does exist
            move= self.moveLog.pop() # In python pop does return 
            self.board[move.startRow][move.startCol]=move.pieceMoved
            self.board[move.endRow][move.endCol]=move.pieceCaptured
            self.whiteToMove = not self.whiteToMove # change turns back
    """
    Now we have to make sure that we are doing valid moves. All possible moves and valid moves are different. We can play a possible move but it may be invalid as it causes us to be in check or if we already in check then all possible moves are not valid that do not take care of check.
    """
    def getValidMoves(self):
        return self.getPossibleMoves() # not caring for checks as of now
    
    def getPossibleMoves(self):
        # there is a lot of things here. Traversal across the baord and check if it is having the same colour as the one with move. Then we geenrate all possible moves.
        moves=[Move((6,6),(4,6),self.board)] # for manual testing- when only this provided then it allows only this move nothing else.
        # moves=[] # stores the possible moves
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                # finding whose turn it is.
                currentTurn = self.board[row][col][0]
                if(currentTurn=='w' and self.whiteToMove==True) or (currentTurn=='b' and self.whiteToMove==False):
                    piece= self.board[row][col][1]
                    # making structure now. Will do it later on.
                    if piece=='p':
                        self.getPawnMoves(row,col,moves) # will make this function inside gameState class only.
                    elif piece=='B':
                        self.getBishopMoves(row,col,moves)
                    elif piece=='R':
                        self.getRookMoves(row,col,moves)
                    elif piece=='N':
                        self.getKnightMoves(row,col,moves)
                    elif piece=='K':
                        self.getKingMoves(row,col,moves)
                    elif piece=='Q':
                        self.getQueenMoves(row,col,moves)
        return moves
    """Get all the pawn moves for the pawn at row=w and column=c and add in list of moves"""
    def getPawnMoves(self,r,c,moves):
        pass

    """Get all the rook moves for the pawn at row=w and column=c and add in list of moves"""
    def getRookMoves(self,r,c,moves):
        pass

    """Get all the bishop moves for the pawn at row=w and column=c and add in list of moves"""
    def getBishopMoves(self,r,c,moves):
        pass

    """Get all the knight moves for the pawn at row=w and column=c and add in list of moves"""
    def getKnightMoves(self,r,c,moves):
        pass

    """Get all the queen moves for the pawn at row=w and column=c and add in list of moves"""
    def getQueenMoves(self,r,c,moves):
        pass

    """Get all the king moves for the pawn at row=w and column=c and add in list of moves"""
    def getKingMoves(self,r,c,moves):
        pass



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
        self.moveID = self.startRow*1000 + self.startCol*100 + self.endRow*10 + self.endCol # unique ID to move. Maybe use this ID to save and do things. We are making this for __eq__ below
        print(self.moveID)
        # This is just to get information of moves. We are not moving still.
    """
    Overriding the equals. We shouldn't have to do this when we are dealing with functions but in classes we have to do (Learn this in java too)
    """
    def __eq__(self,other):
        # this is comparing self object to other object. We want to compare one move to move in validMoves 
        #First have to make sure that they are same thing that is instance of one is same as other.
        # 2 moves are same when startRow,startCol,endRow,endCol are same.
        if isinstance(other,Move):
            return other.moveID == self.moveID
        return False

    def getChessNotation(self):
        # Not the actual chess notation but will work for now. Improve later.
        return self.getRankAndFile(self.startRow, self.startCol) + self.getRankAndFile(self.endRow, self.endCol)
    
    def getRankAndFile(self,row,col):
        return self.colsToFiles[col] + self.rowsToRanks[row]
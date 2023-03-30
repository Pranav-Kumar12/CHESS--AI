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
            # ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            # ["bp","bp","bp","bp","bp","bp","bp","bp"],
            # ["--","--","--","--","--","--","--","--"], 
            # ["--","--","--","--","--","--","--","--"],
            # ["--","--","--","--","--","--","--","--"],
            # ["--","--","--","--","--","--","--","--"],
            # ["wp","wp","wp","wp","wp","wp","wp","wp"],
            # ["wR","wN","wB","wQ","wK","wB","wN","wR"]
            ["bK","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","wQ","--"],
            ["--","wK","--","--","--","--","--","--"], 
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"]
        ] 
        self.whiteToMove=True
        self.moveLog= []
        self.whiteKingLocation = (7,4)
        self.blackKingLocation = (0,4) # These are stored for castling benefits checking and in general validating moves.
        # have to make sure that moving king and rook is registered for castling rights
        self.checkMate= False
        self.staleMate=False


    # Creating a function in chess engine now to finally make a move.
    """ This will take move as parameter and executes it ( except for castling and en-passant and pawn promotion) """
    def makeMove(self,move):
        self.board[move.startRow][move.startCol]="--"
        self.board[move.endRow][move.endCol]=move.pieceMoved
        # if it is king then update its location
        if move.pieceMoved[1] == "K":
            if move.pieceMoved[0]=='w':
                self.whiteKingLocation = (move.endRow,move.endCol)
            else:
                self.blackKingLocation = (move.endRow, move.endCol)
        # As of now assuming that move is valid- later on will checek and then play the move
        self.moveLog.append(move) # for pgn or undo 
        self.whiteToMove= not self.whiteToMove # change turns

    """ Undo the latest move"""
    def undo_move(self):
        if len(self.moveLog)!=0: # making sure that a move does exist
            move= self.moveLog.pop() # In python pop does return 
            self.board[move.startRow][move.startCol]=move.pieceMoved
            self.board[move.endRow][move.endCol]=move.pieceCaptured
            # king's coordinates
            if(move.pieceMoved == "wK" or move.pieceMoved=='bK'):
                if(move.pieceMoved == 'wK'):
                    self.whiteKingLocation= (move.startRow, move.startCol)
                else:
                    self.blackKingLocation = (move.startRow, move.startCol)
            self.whiteToMove = not self.whiteToMove # change turns back
    """
    Now we have to make sure that we are doing valid moves. All possible moves and valid moves are different. We can play a possible move but it may be invalid as it causes us to be in check or if we already in check then all possible moves are not valid that do not take care of check.
    """
    def getValidMoves(self):
        # Naive solution- Very trivial way of dealing with it.
        # 1) All possible moves
        moves= self.getPossibleMoves()
        # 2) For each move, make a move (generally have to traverse the list in backward direction when we have to deal with erasing of elements as indexes are concerned)
        for i in range(len(moves)-1,-1,-1):
            self.makeMove(moves[i])
            # 3) generate all possible moves
            # 4)for each of your opponent moves, see if they attack your king
            self.whiteToMove= not self.whiteToMove # Now after we make the move above then it automatically swaps the moves, but we want to see for isInCheck for same colour complex so doing this again of swapping colours
            if self.isInCheck():
                # have to remove this move as it creates check on our king
                moves.remove(moves[i]) #5)
            # Now we have to switch the players back and undo the move back that we used to check earlier
            self.whiteToMove= not self.whiteToMove # We gave the move to black with one makeMove done before in this loop so that we can undo it and control regained by white.
            self.undo_move()
        # check here whether valid moves are achievable or not 
        if len(moves)==0:
            #checkmate or stalemate
            if(self.isInCheck()):
                self.checkMate=True
            else:
                self.staleMate=True
        else:
            # when we are undoing a checkmate or stalemate
            self.checkMate= False
            self.staleMate = False
        return moves 
    
    """
    Find if the current player is in check
    """
    def isInCheck(self):
            # Returning whether king coordinates is under attack
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0],self.blackKingLocation[1])
        

    """
    Determine if the enemy can attack square r,c
    """
    def squareUnderAttack(self,r,c):
        # I am going to change looking at situation 
        self.whiteToMove= not self.whiteToMove # from his perspective
        oppMoves= self.getPossibleMoves()
        self.whiteToMove= not self.whiteToMove # switch moves back. We switched to get all moves for opponent
        # Now if the opponent moves attack r,c then found
        for move in oppMoves:
            if move.endRow==r and move.endCol==c:
                return True
        return False

    """
    All Moves without considering checks
    """
    def getPossibleMoves(self):
        # there is a lot of things here. Traversal across the baord and check if it is having the same colour as the one with move. Then we geenrate all possible moves.
        # moves=[Move((6,6),(4,6),self.board)] # for manual testing- when only this provided then it allows only this move nothing else.
        moves=[] # stores the possible moves
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
        if self.whiteToMove: #white pawns
            if self.board[r-1][c]=="--":
                moves.append(Move((r,c),(r-1,c),self.board)) # for the next square.
                if r==6 and self.board[r-2][c]=="--":
                    moves.append(Move((r,c),(r-2,c),self.board)) # for double squares move during first move.
            if c>0 and self.board[r-1][c-1][0]=="b": # capturing enemy piece
                moves.append(Move((r,c),(r-1,c-1),self.board))
            if c<len(self.board)-1 and self.board[r-1][c+1][0]=="b": 
                moves.append(Move((r,c),(r-1,c+1),self.board))
        else:   #black pawn moves
            if self.board[r+1][c]=="--":
                moves.append(Move((r,c),(r+1,c),self.board)) # for the next square.
                if r==1 and self.board[r+2][c]=="--":
                    moves.append(Move((r,c),(r+2,c),self.board)) # for double squares move during first move.
            if c>0 and self.board[r+1][c-1][0]=="w": # capturing left enemy piece
                moves.append(Move((r,c),(r+1,c-1),self.board))
            if c<len(self.board)-1 and self.board[r+1][c+1][0]=="w":    # capturing right enemy piece 
                moves.append(Move((r,c),(r+1,c+1),self.board))
        # pawn promotions later
    """Get all the rook moves for the pawn at row=w and column=c and add in list of moves"""
    def getRookMoves(self,r,c,moves):
        # Tried to make code uniform so that the same can be applied to others by changing directions
        directions=[[1,0],[-1,0],[0,1],[0,-1]]
        if self.whiteToMove:    #for white
            origRow=r
            origCol=c
            for direction in directions:
                while(True):
                    r= r+direction[0]
                    c= c+direction[1]
                    if(r>=0 and r<8 and c>=0 and c<8):
                        if(self.board[r][c][0]=='w'): # same army
                            r=origRow
                            c=origCol
                            break
                        elif self.board[r][c][0]=='b': #capture
                            moves.append(Move((origRow,origCol),(r,c),self.board))
                            r=origRow
                            c=origCol
                            break
                        else: # empty square
                            moves.append(Move((origRow,origCol),(r,c),self.board))
                    else:
                        r=origRow
                        c=origCol
                        break      
        else:   #for black
            origRow=r
            origCol=c
            for direction in directions:
                while(True):
                    r= r+direction[0]
                    c= c+direction[1]
                    if(r>=0 and r<8 and c>=0 and c<8):
                        if(self.board[r][c][0]=='b'): # same army
                            r=origRow
                            c=origCol
                            break
                        elif self.board[r][c][0]=='w': #capture
                            moves.append(Move((origRow,origCol),(r,c),self.board))
                            r=origRow
                            c=origCol
                            break
                        else: # empty square
                            moves.append(Move((origRow,origCol),(r,c),self.board))
                    else:
                        r=origRow
                        c=origCol
                        break
            

    """Get all the bishop moves for the pawn at row=w and column=c and add in list of moves"""
    def getBishopMoves(self,r,c,moves):
        directions=[[1,1],[-1,1],[1,-1],[-1,-1]]
        if self.whiteToMove:    #for white
            origRow=r
            origCol=c
            for direction in directions:
                while(True):
                    r= r+direction[0]
                    c= c+direction[1]
                    if(r>=0 and r<8 and c>=0 and c<8):
                        if(self.board[r][c][0]=='w'): # same army
                            r=origRow
                            c=origCol
                            break
                        elif self.board[r][c][0]=='b': #capture
                            moves.append(Move((origRow,origCol),(r,c),self.board))
                            r=origRow
                            c=origCol
                            break
                        else: # empty square
                            moves.append(Move((origRow,origCol),(r,c),self.board))
                    else:
                        r=origRow
                        c=origCol
                        break      
        else:   #for black
            origRow=r
            origCol=c
            for direction in directions:
                while(True):
                    r= r+direction[0]
                    c= c+direction[1]
                    if(r>=0 and r<8 and c>=0 and c<8):
                        if(self.board[r][c][0]=='b'): # same army
                            r=origRow
                            c=origCol
                            break
                        elif self.board[r][c][0]=='w': #capture
                            moves.append(Move((origRow,origCol),(r,c),self.board))
                            r=origRow
                            c=origCol
                            break
                        else: # empty square
                            moves.append(Move((origRow,origCol),(r,c),self.board))
                    else:
                        r=origRow
                        c=origCol
                        break

    """Get all the knight moves for the pawn at row=w and column=c and add in list of moves"""
    def getKnightMoves(self,r,c,moves):
        directions=[[1,2],[-1,2],[1,-2],[-1,-2],[2,1],[2,-1],[-2,1],[-2,-1]]
        if self.whiteToMove:    #for white
            for direction in directions:
                newrow= r+direction[0]
                newcol= c+direction[1]
                if(newrow>=0 and newrow<8 and newcol>=0 and newcol<8):
                    if self.board[newrow][newcol][0]=='b': #capture
                        moves.append(Move((r,c),(newrow,newcol),self.board))
                    elif self.board[newrow][newcol]=="--": # empty square
                        moves.append(Move((r,c),(newrow,newcol),self.board))     
        else:   #for black
            for direction in directions:
                newrow= r+direction[0]
                newcol= c+direction[1]
                if(newrow>=0 and newrow<8 and newcol>=0 and newcol<8):
                    if self.board[newrow][newcol][0]=='w': #capture
                        moves.append(Move((r,c),(newrow,newcol),self.board))
                    elif self.board[newrow][newcol]=="--": # empty square
                        moves.append(Move((r,c),(newrow,newcol),self.board))     

    """Get all the queen moves for the pawn at row=w and column=c and add in list of moves"""
    def getQueenMoves(self,r,c,moves):
        #similar to rook with different direction array
        # shorter is to actually use rook and bishop functions
        self.getBishopMoves(r,c,moves)
        self.getRookMoves(r,c,moves)

    """Get all the king moves for the pawn at row=w and column=c and add in list of moves"""
    def getKingMoves(self,r,c,moves):
        #similar to knight as only one step allowed.
        directions=[[1,1],[-1,1],[1,-1],[-1,-1],[1,0],[-1,0],[0,1],[0,-1]]
        if self.whiteToMove:    #for white
            for direction in directions:
                newrow= r+direction[0]
                newcol= c+direction[1]
                if(newrow>=0 and newrow<8 and newcol>=0 and newcol<8):
                    if self.board[newrow][newcol][0]=='b': #capture
                        moves.append(Move((r,c),(newrow,newcol),self.board))
                    elif self.board[newrow][newcol]=='--': # empty square
                        moves.append(Move((r,c),(newrow,newcol),self.board))     
        else:   #for black
            for direction in directions:
                newrow= r+direction[0]
                newcol= c+direction[1]
                if(newrow>=0 and newrow<8 and newcol>=0 and newcol<8):
                    if self.board[newrow][newcol][0]=='w': #capture
                        moves.append(Move((r,c),(newrow,newcol),self.board))
                    elif self.board[newrow][newcol]=='--': # empty square
                        moves.append(Move((r,c),(newrow,newcol),self.board))     


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
        # print(self.moveID)
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
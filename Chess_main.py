"""
This is going to be our main driver file where it is responsible for handling user responses and current game state object.
"""
import pygame as p
import Chess_engine

# p.init() # It can be initialized here too. Doesn't matter here.
WIDTH = HEIGHT = 512  # 400 is another good option
DIMENSION = 8 # chess board is 8X8
SQ_SIZE = HEIGHT//DIMENSION
MAX_FPS =15  # mostly will be used later on in animations.
IMAGES= {}  # dictionary of images
# images should only be loaded once in memory and after that it should be saved so that it is not loaded every frame and makes becomes laggy.

"""
initialized a global dictionary of images. Will be called once in main
"""
# testing 
# We can even change images and chess set so defining load images separately.(flexible)
def loadImages():
  # IMAGES["wp"]= p.image.load('Images/wp.png') 
  # This is not the best way as we have to do this for each and every piece.
  pieces=['wp','wR','wN','wB','wQ','wK','bp','bR','bN','bB','bQ','bK']
  for piece in pieces:
    IMAGES[piece]=p.transform.scale(p.image.load("Images/"+piece+ ".png"),(SQ_SIZE,SQ_SIZE)) #we can decrease or increase size of piece
  # We can access an image by calling the dictionary IMAGES['wp']
  # We will look whether that position is empty or not. If it is not empty then we will draw that piece in that sqaure with IMAGES[piece]

"""
This is main driver for code and it will handle user input and updating the graphics.
"""

def main():
  p.init()
  # set up screen
  screen= p.display.set_mode((WIDTH, HEIGHT))
  clock= p.time.Clock()
  screen.fill(p.Color("white"))
  # Now we will use Chess_engine to grab game state object.
  gs = Chess_engine.GameState() # Now we have access to three variables of game state by gs.board, gs.whiteToMove and gs.moveLog
  # print(gs.board) # don't have to do board() as it is not a method/function but a variable
  loadImages() # only once, before while loop
  running= True
  sqSelected=() # We are making a tuple (row, col). 
  # empty initially- stores last click
  playerClick=[] # keeps track of players clicks (two tuples-> (6,4),(4,4))
  while running:
    for e in p.event.get():
      if e.type == p.QUIT: #whenever current event is being quitted
        running = False
      elif e.type == p.MOUSEBUTTONDOWN:
        location= p.mouse.get_pos() #(x,y) of mouse
        col= location[0]//SQ_SIZE # x coordinate responsible for it
        row = location[1]//SQ_SIZE
        if sqSelected == (row,col): # same square selected
          sqSelected=() # deselecting the given piece
          playerClick=[] # clearing it out
        else:
          sqSelected=(row,col)
          playerClick.append(sqSelected) # append for both first and second clicks
        if len(playerClick)==2:
          # now we will implement everything in move class so that we can store it and back it. Write in notations etc.
          move= Chess_engine.Move(playerClick[0],playerClick[1], gs.board)
          print(move.getChessNotation())
          gs.makeMove(move)
          sqSelected=()
          playerClick=[]

    drawGameState(screen, gs)
    clock.tick(MAX_FPS)
    p.display.flip()
    #We write these 2 statements whenever it is running
    # For meaning of display flip : https://stackoverflow.com/questions/29314987/difference-between-pygame-display-update-and-pygame-display-flip

"""
Responsible for all graphics in a given current state.
"""
def drawGameState(screen, gs):
  # these two parameter enough to draw it out
  drawBoard(screen) # draws squares on the board. Doesn't need game state to draw board.
  # If we want changes such as piece highlighting and move suggestions, or square highlight on clicking (will add later)
  drawPieces(screen, gs.board)  # draws out the pieces.

"""
Draw the squares on the board (Might cause changes to let user select the colour of board.Prefer gray with black pieces for better visibility)
"""
def drawBoard(screen):

  colors= [p.Color("white"), p.Color("gray")]
  # we can put colours here and change the squares colours
  for i in range(DIMENSION):
    for j in range(DIMENSION):
      # sum of two sqaures is of different parity for dark and light square, sum even then light square
      color = colors[(i+j)%2]
      # now draw the square
      p.draw.rect(screen, color, p.Rect(j*SQ_SIZE, i*SQ_SIZE, SQ_SIZE, SQ_SIZE)) 
      # Here dimension is decided by imagining a real x and y axis. First fix for x axis and then for y axis
                     
  
"""
Draws the pieces on the board using the current game state board
"""
def drawPieces(screen,board):
  for i in range(DIMENSION):
    for j in range(DIMENSION):
      piece= board[i][j]
      if piece != "--":
        screen.blit(IMAGES[piece], p.Rect(j*SQ_SIZE, i*SQ_SIZE , SQ_SIZE, SQ_SIZE)) # It is going to blit in IMAGE[piece] in the rectangle given

# Even though I could have done both drawPieces and drawBoard together but keeping it separate allows flexibility to improve both separately.- maybe piece highlighting and the square highlighting
# Important to call board first and then pieces for able to see pieces over board.
if __name__ == "__main__":
  main()

  
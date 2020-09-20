# Chess-Game-GUI
Chess game designed on pygame.   Currently a Work-In-Progress. For example, 'checks' have not been implemented fully yet.  

Legal moves and capturing is fully functional. Captured pieces are stored, but not yet shown.  

Movement of pieces is now animated. Instead of disappearing and appearing in new place, piece moves across the board.

## Dependencies
Pygame: Graphics platorm (pip install pygame)
Numpy: 8x8 array used to manage board (pip install numpy)

## Usage
Run `chs_game.py`

## Contents
`chs_game.py:` The 'frontend' / GUI. Handles clicks, moves pieces, shows allowed moves. 

`chs_pieces.py:` Contains piece classes. Main 'Piece' interface initializes common attributes. Specific pieces (ie. Bishop) inherits from Piece and implements method to get 'legal moves'.  

`chs_board.py:` The 'backend' to the GUI board. 8x8 Array which contains all pieces in their positions. 'Checks', 'Victory', etc will be implemented soon in this class.  

`chs_const.py:` Stores various constants (height/width of board, size of indvidual squares, etc.)

`chs_themes.py:` Contains a dictonary of color themes for the chess games. More will be added soon.

`images folder:` Contains images for each chess piece  



## Future Updates
- MAIN PLANNED UPDATE -> SOCKETS:
    - Play the game over local network or on the web
    - Implement chat feature between players
- Timer and/or Stopwatch
- Multiple themes with theme builder (pending completion)
- Misc tweaks/additions to GUI 
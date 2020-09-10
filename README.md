# Chess-Game-GUI
Chess game designed on tkinter Canvas.   Currently a Work-In-Progress. For example, 'checks' have not been implemented fully yet.  

Legal moves and capturing is fully functional. Captured pieces are stored, but not yet drawn.

## Dependencies
Pillow: Used to place images on display (pip install pillow)
Numpy: 8x8 array used to manage board (pip install numpy)

## Usage
Run `chsGame.py`

## Contents
`images folder:` Contains images for each chess piece  

`chsPieces.py:` Contains piece classes. Main 'Piece' class initializes common attributes. Specific pieces (ie. Bishop) inherits from Piece and implements method to get 'legal moves'.  

`chsBoard.py:` The 'backend' to the GUI board. 8x8 Array which contains all pieces in their positions. 'Checks', 'Victory', etc will be implemented soon in this class.  

`chsGame.py:` The 'frontend' / GUI. Handles clicks, moves pieces, shows allowed moves. 

## Future Updates
- MAIN UPDATE -> SOCKETS:
    - Play the game over local network or on the web
    - Implement chat feature between players
- Timer and/or Stopwatch
- Multiple themes with theme builder (pending completion)
- Misc tweaks/additions to GUI 
Othello-AI
==========

Basic AI Project for the game Othello (also known as Reversi).
Written in Python 2.7
Uses 
* Pygames
* numpy
* cython

Make sure pygames (http://www.pygame.org/install.html), numpy (http://www.scipy.org/install.html), and cython (http://cython.org/#download (optional)

To run the program run:
    python main.py


The following files have been changed to cython files to attempt to increase performance:
* board.pyx
* players.pyx

To recompile cython (.pyx) files run:
    make all

Classes:
* Board (Handles all board operations)
* GUI (Handles all graphical user interface commands)
* players (Classes for human/ computer player)
* othello (Actual game class)
* Menu (Handles main menu)


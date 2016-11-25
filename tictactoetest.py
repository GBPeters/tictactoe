# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 13:07:26 2016

@author: peter086
"""

from tictactoe import *
from tictactoeAI import *

testEmptyM = [[0,0,0],[0,0,0],[0,0,0]]
testM = [[0,1,2],[1,2,0],[1,0,2]]

board = Board(3, testM)
board.show()
assert board.hasStone(1,1) == 2
assert len(board.getEmptySpots()) == 3
assert not board.whoHasWon()
assert board.placeStone(0,0,2)
assert len(board.getEmptySpots()) == 2
assert board.whoHasWon() == 2
assert not board.placeStone(1,2,1)
board.show()

board = Board(3, testM)
turns = createPossibleMoves(board, 1)
for t in turns:
    print t
    
board = Board(3)
# turns = createPossibleMoves(board, 1)
# for t in turns:
#     print t

#playshellgame()
testsize=4

for i in range(testsize / 2 + 1):
    for j in range(i+1):
        game = Game(size=testsize)
        outcome = game.playTurn(i, j)
        while outcome == 0:
            move = findBestMove(game.getBoard(), game.getTurnPlayer(), maxrecursion=4)
            outcome = game.playTurn(move.row, move.column)
        raw_input("Ready for the next game?")
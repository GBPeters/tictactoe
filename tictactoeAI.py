# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 14:44:43 2016

@author: peter086
"""

from tictactoe import *

class PossibleTurn (object):
    
    def __init__(self, row, column, player, winpotential = 0, loserisk = 0, remiserisk = 0):
        self.row = row
        self.column = column
        self.player = player
        self.winpotential = winpotential
        self.loserisk = loserisk
        self.remiserisk = 0
        
    def __str__(self):
        return "Turn: (%d, %d) - W:%d, L%d, R%d" % (self.row, self.column, self.winpotential, self.loserisk, self.remiserisk) 
    

def createPossibleTurns(board, player, reclvl = 0):
    print reclvl
    emptyspots = board.getEmptySpots()
    turns = []
    for row, column in emptyspots:
        boardcopy = board.copy()
        boardcopy.placeStone(row, column, player)
        won = board.whoHasWon()
        if won == 3:
            turns += [PossibleTurn(row, column, player, remiserisk = 1)]
        elif won == player:
            turns += [PossibleTurn(row, column, player, winpotential = 1)]
        else:
            turnlist = createPossibleTurns(boardcopy, switchPlayer(player), reclvl + 1)
            if len(turnlist) > 0:
                if 1 in [turn.winpotential for turn in turnlist]:
                    turn = PossibleTurn(row, column, player, loserisk = 1)
                else:
                    potential = min(turnlist, key = lambda x : x.loserisk).loserisk
                    remise = min(turnlist, key = lambda x : x.remiserisk).remiserisk
                    turn = PossibleTurn(row, column, player, winpotential = potential, remiserisk = remise)
            else:
                turn = PossibleTurn(row, column, player, remiserisk = 1)
            turns += [turn]
    return turns
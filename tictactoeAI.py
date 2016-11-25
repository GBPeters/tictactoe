# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 14:44:43 2016

@author: peter086
"""

from tictactoe import *
from random import random


class PossibleTurn(object):
    def __init__(self, row, column, player, winpotential=0, loserisk=0, remiserisk=0):
        self.row = row
        self.column = column
        self.player = player
        self.winpotential = winpotential
        self.loserisk = loserisk
        self.remiserisk = remiserisk

    def __str__(self):
        return "Turn: (%d, %d) - W:%d, L%d, R%d" % (
        self.row, self.column, self.winpotential, self.loserisk, self.remiserisk)


def createPossibleMoves(board, player, maxrecursion=999, reclvl=0):
    emptyspots = board.getEmptySpots()
    turns = []
    for row, column in emptyspots:
        boardcopy = board.copy()
        boardcopy.placeStone(row, column, player)
        won = boardcopy.whoHasWon()
        if won == 3:
            turns += [PossibleTurn(row, column, player, remiserisk=1)]
        elif won == player:
            turns += [PossibleTurn(row, column, player, winpotential=1)]
        elif reclvl < maxrecursion:
            turnlist = createPossibleMoves(boardcopy, switchPlayer(player), maxrecursion=maxrecursion, reclvl=reclvl + 1)
            if len(turnlist) > 0:
                if 1 in [turn.winpotential for turn in turnlist]:
                    turn = PossibleTurn(row, column, player, loserisk=1)
                else:
                    potential = sum([t.loserisk for t in turnlist]) / float(len(turnlist))
                    remise = sum([t.remiserisk for t in turnlist]) / float(len(turnlist))
                    risk = sum([t.winpotential for t in turnlist]) / float(len(turnlist))
                    turn = PossibleTurn(row, column, player, winpotential=potential, loserisk=risk, remiserisk=remise)
            else:
                turn = PossibleTurn(row, column, player, remiserisk=1)
            turns += [turn]
        else:
            turns += [PossibleTurn(row, column, player)]
    return turns

def minimiseRiskHeuristic(moves):
    moves = sorted(moves, key=lambda m: (m.loserisk, -m.winpotential, -m.remiserisk))
    return moves[0]

def maximisePotentialHeuristic(moves):
    moves = sorted(moves, key=lambda m: (m.winpotential- (m.loserisk == 1), -m.loserisk, -m.remiserisk), reverse=True)
    return moves[0]

def randomMinimiseRiskHeuristic(moves):
    moves = sorted(moves, key=lambda m: (m.loserisk, -m.winpotential, -m.remiserisk, random()))
    return moves[0]

def randomMaximisePotentialHeuristic(moves):
    moves = sorted(moves, key=lambda m: (m.winpotential - (m.loserisk == 1), -m.loserisk, -m.remiserisk, random()), reverse=True)
    return moves[0]

def randomBalancedHeuristic(moves):
    moves = sorted(moves, key=lambda m: (m.winpotential - m.loserisk, -m.remiserisk, random()), reverse=True)
    return moves[0]

def findBestMove(board, player, heuristic=randomBalancedHeuristic, maxrecursion=999):
    moves = createPossibleMoves(board, player, maxrecursion)
    move = heuristic(moves)
    return move

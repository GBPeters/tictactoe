# -*- coding: utf-8 -*-
"""
Spyder Editor

This temporary script file is located here:
C:\Users\peter086\.spyder2\.temp.py
"""

symbols = ' xo'

class Board (object):        
    
    def __init__(self, size=3, boardMatrix=None):
        self._board = [size * [0] for i in range(size)]
        if boardMatrix != None:
            assert len(boardMatrix) == size
            for row in boardMatrix:
                assert len(row) == size
            for i in range(size):
                for j in range(size):
                    elem = boardMatrix[i][j]
                    assert elem == 0 or elem == 1 or elem == 2
                    self._board[i][j] = elem
        
    def show(self):
        for i in range(len(self._board)):
            row = self._board[i]
            line = ''
            for elem in row:
                symbol = symbols[elem]
                line += ' %s |' % symbol
            print line[:-1]
            if i < len(self._board) - 1:
                print '-----------'
            
    def hasStone(self, row, column):
        return self._board[row][column]     
    
    def placeStone(self, row, column, player):
        assert player == 1 or player == 2
        if self.hasStone(row, column) or self.whoHasWon():
            return False
        else:
            self._board[row][column] = player
            return True
            
    def _clear(self):
        size = len(self._board)
        self._board = [size * [0] for i in range(size)]
    
    def getEmptySpots(self):
        spots = []
        for i in range(len(self._board)):
            row = self._board[i]
            for j in range(len(row)):
                if not self.hasStone(i, j):
                    spots += [(i, j)]
        return spots
        
    def whoHasWon(self):
        # First, check diagonals
        remise = True
        size = len(self._board)
        row1 = []
        row2 = []
        for i in range(size):
            row1 += [self._board[i][i]]
            row2 += [self._board[i][size-i-1]]
            remise = 1 in row1 and 2 in row1 and 1 in row2 and 2 in row2
        if row1.count(row1[0]) == size:
            return row1[0]
        elif row2.count(row2[0]) == size:
            return row2[0]
        # Then, check horizontals
        for row in self._board:
            if row.count(row[0]) == size:
                return row[0]
            if not (1 in row and 2 in row):
                remise = False
        # Finally, check verticals
        for i in range(size):
            column = [row[i] for row in self._board]
            if column.count(column[0]) == size:
                return column[0]
            if not (1 in column and 2 in column):
                remise = False
        # With no win, return 0. With remise, return 3
        if remise:
            return 3
        return 0
    
    def copy(self):
        return Board(size = len(self._board), boardMatrix = self._board)
   
     
class Game (object):
    
    def __init__(self, size=3, player1name = 'player 1', player2name = 'player 2', verbose=True):
        self._board = Board(size)
        self._turncount = 0
        self._player = 1
        self.playernames = [player1name, player2name]
        self.verbose = verbose
        if verbose:
            print 'Welcome to a new game of tic tac toe!'
            print '%s (%s) v. %s (%s)' % (self.playernames[0], symbols[1], self.playernames[1], symbols[2])
            self._board.show()
            
        
    def getBoard(self):
        return self._board.copy()
    
    def getTurnCount(self):
        return self._turncount
    
    def getTurnPlayer(self):
        return self._player
        
    # Plays a round of tic tac toe, returns 0 for valid but non-winning turn, 1 if player one has one, and two if player two has won
    # If an invalid turn is played, it returns -1, and the turn does not count and has to be redone.
    def playTurn(self, row, column):
        try:
            played = self._board.placeStone(row, column, self._player)
            outcome = self._board.whoHasWon()
        except:
            outcome = -1
        if outcome < 1 and not played:
            outcome = -1
        else:
            self._turncount += 1
        if self.verbose:
            if played:
                print 'Tic Tac Toe - %s (%s) v. %s (%s)' % (self.playernames[0], symbols[1], self.playernames[1], symbols[2])
                print 'Turn %d - %s placed stone (%d, %d)' % (self._turncount, self.playernames[self._player - 1], row, column)
                self._board.show()
            else:
                print '%s made an invalid turn: (%d, %d)' % (self.playernames[self._player - 1], row, column)
            if outcome >= 1:
                if outcome == 3:
                    print 'Remise after %d turns.' % self._turncount
                else:
                    print '%s has won the game in %d turns!' % (self.playernames[self._player - 1], self._turncount)
        if played:
            self._player = switchPlayer(self._player)
        return outcome
        
def playshellgame():
    game = Game()
    outcome = 0
    while outcome <= 0:
        coords = [int(i) for i in raw_input("Enter turn row and column: ").split()]
        row = coords[0]
        column = coords[1]
        outcome = game.playTurn(row, column)

def switchPlayer(player):
    return 1 if player == 2 else 2
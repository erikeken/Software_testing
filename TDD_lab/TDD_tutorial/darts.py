class scoreboard:
    """ Implements a score board for a darts game
    """
    def __init__(self):
        self.playerscores = [301, 301]
        #add a turn variable to keep track of whose turn it is
        self.turn = 1
        self.throws=0

    def playerscore(self, player):
        if player==1 or player==2:
            #adding code for winning condition
            if self.playerscores[player-1] == 0:
                return('WON')
            else:
                return (self.playerscores[player-1])
        else:
            raise NameError('player out of range')

    def playerthrown(self, player, multiplier, number):
        #throw error if it is not the player's turn
        if player != self.turn:
            raise NameError('throw out of turn')
        #increment the number of throws
        self.throws += 1
        #if we have done 3 throws, it is the other player's turn
        if self.throws == 3:
            self.throws = 0
            if self.turn == 1:
                self.turn = 2
            else:
                self.turn = 1
        #code to just pass the first 6 tests till three_throws
        # if self.throws == 3:
        #     self.turn= 2

        if multiplier == 'double':
            number = number * 2
        elif multiplier == "triple":
            number = number * 3
        self.playerscores[player - 1] -= number
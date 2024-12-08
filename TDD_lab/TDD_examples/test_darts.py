import darts
import pytest

def test_scoreboard():
    game = darts.scoreboard()


# test to initialize the game with 2 players
def test_score():
    game = darts.scoreboard()
    assert game.playerscore(1) == 301
    assert game.playerscore(2) == 301


# test to check if the player is out of range
def test_noThirdPlayer():
    game = darts.scoreboard()
    with pytest.raises(NameError):
        game.playerscore(3)

def test_scoring():
    game = darts.scoreboard()

    game.playerthrown(1, 'single', 15)
    assert game.playerscore(1) == 301 - 15

    game.playerthrown(1, 'double', 20)
    assert game.playerscore(1) == 301 - 15 - 2 * 20

    game.playerthrown(1, 'triple', 5)
    assert game.playerscore(1) == 301 - 15 - 2 * 20 - 3 * 5

def test_player1_plays_first():
    game = darts.scoreboard()
    with pytest.raises(NameError):
        game.playerthrown(2, 'single', 5)

def test_three_throws():
    game = darts.scoreboard ()
    game.playerthrown(1 ,"triple" ,5)
    game.playerthrown(1 ,"triple" ,5)
    game.playerthrown(1 ,"triple" ,5)
    #extending the test to check if the turn is switched
    game. playerthrown (2 ,"triple" ,20)
    game. playerthrown (2 ,"triple" ,20)
    game. playerthrown (2 ,"triple" ,20)
    game. playerthrown (1 ,"triple" ,20)
    assert game.playerscore(1) == 301 - 3*3 * 5 - 3*20
    # assert game.playerscore(2) == 301 - 3 * 20

def test_win():
    game = darts.scoreboard()
    game.playerthrown(1, 'triple', 20)
    game.playerthrown(1, 'triple', 20)
    game.playerthrown(1, 'triple', 20)
    game.playerthrown(2, 'single', 1)
    game.playerthrown(2, 'single', 1)
    game.playerthrown(2, 'single', 1)
    game.playerthrown(1, 'double', 19)
    game.playerthrown(1, 'double', 19)
    game.playerthrown(1, 'double', 19)
    game.playerthrown(2, 'single', 1)
    game.playerthrown(2, 'single', 1)
    game.playerthrown(2, 'single', 1)
    game.playerthrown(1, 'single', 1)
    game.playerthrown(1, 'single', 3)
    game.playerthrown(1, 'single', 3)
    assert game.playerscore(1)== "WON"

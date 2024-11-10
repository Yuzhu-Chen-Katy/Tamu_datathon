import numpy as np
from MCTSAgent import MCTSAgent

#Testing
#from mcts.base.base import BaseState
#from mcts.searcher.mcts import MCTS

class Game():
  def __init__(self):
    self.board = np.full((8, 8), 0)   # Board represented as a np array of empty spaces (0s)
    self.current_player = 1                       # Player that has the current move
    self.turn_count = 0                                 # Number of turns elapsed in the game
    self.p1_pieces = 2                                  # Number of pieces that Player1 has placed on the board
    self.p2_pieces = 2                                  # Number of pieces that Player2 has placed on the board
    self.p1win = False
    self.p2win = False

  def modifyMatrix(self, newMatrix):
    self.board = newMatrix


newGame = Game()


boardArray = [[0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 1, 1, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, -1, -1, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0]]

newGame.modifyMatrix(np.array(boardArray))

testAgent = MCTSAgent()

bestAction = testAgent.get_best_move(newGame)
print(bestAction)



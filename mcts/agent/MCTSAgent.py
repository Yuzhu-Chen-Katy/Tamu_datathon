from mcts.searcher.mcts import MCTS
from mcts.base.base import BaseState


class MCTSAgent():
  def __init__(self):
    self.searcher = MCTS(3800)
  
  def get_best_move(self, game, attempt):
    currentState = BaseState(game)
    if attempt == 1:
      self.searcher.timeLimit = 3800
    else:
      self.searcher.timeLimit = 2000
      
    best_move = self.searcher.search(initial_state=currentState, turnCount=game.turn_count)
    return best_move

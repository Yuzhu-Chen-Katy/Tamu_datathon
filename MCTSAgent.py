from mcts.searcher.mcts import MCTS
from mcts.base.base import BaseState


class MCTSAgent():
  def __init__(self):
    self.searcher = MCTS(4000)
  
  def get_best_move(self, game):
    currentState = BaseState(game)
    best_move = self.searcher.search(initial_state=currentState, turnCount=game.turn_count)
    return best_move

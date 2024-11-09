import pickle
from MCTSTrain import MyState


class MCTSAgent():
  def __init__(self):
    with open('MCTSTree.pkl', 'rb') as f:
      self.searcher = pickle.load(f)
  
  def get_best_move(self, game):
    currentState = MyState(game)
    best_move = self.searcher.search(initial_state=currentState)
    return best_move

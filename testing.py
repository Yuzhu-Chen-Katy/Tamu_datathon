from mcts.base.base import BaseState, BaseAction
from mcts.searcher.mcts import MCTS
from copy import deepcopy
import numpy as np
#from PushBattle import Game, PLAYER1, PLAYER2, EMPTY, BOARD_SIZE, NUM_PIECES, _torus, chess_notation_to_array, array_to_chess_notation


# GLOBAL VARIABLES
EMPTY = 0       # Empty space board value
PLAYER1 = 1     # First player board value
PLAYER2 = -1    # Second player board value

BOARD_SIZE = 8  # Size of the board
NUM_PIECES = 8  # Number of pieces each player is allowed to place of their own color

##################

def _torus(r, c):
  rt = (r + BOARD_SIZE) % BOARD_SIZE
  ct = (c + BOARD_SIZE) % BOARD_SIZE
  return rt, ct

class MyState(BaseState):
  def __init__(self):
    self.board = np.full((BOARD_SIZE, BOARD_SIZE), 0)   # Board represented as a np array of empty spaces (0s)
    self.current_player = PLAYER1                       # Player that has the current move
    self.turn_count = 0                                 # Number of turns elapsed in the game
    self.p1_pieces = 0                                  # Number of pieces that Player1 has placed on the board
    self.p2_pieces = 0                                  # Number of pieces that Player2 has placed on the board
    self.p1win = False
    self.p2win = False
  
  def get_possible_actions(self) -> [any]:
    """Returns list of all possible moves in current state."""
    moves = []
    current_pieces = self.p1_pieces if self.current_player == PLAYER1 else self.p2_pieces
    
    if current_pieces < NUM_PIECES:
      # placement moves
      for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
          if self.board[r][c] == EMPTY:
            moves.append((r, c))
    else:
      # movement moves
      for r0 in range(BOARD_SIZE):
        for c0 in range(BOARD_SIZE):
          if self.board[r0][c0] == self.current_player:
            for r1 in range(BOARD_SIZE):
              for c1 in range(BOARD_SIZE):
                if self.board[r1][c1] == EMPTY:
                  moves.append((r0, c0, r1, c1))
    return moves

  def take_action(self, action: any) -> 'BaseState':
    newState = deepcopy(self)

    if (len(action) == 4): #if the action moves a piece already on the board
      newState.board[action[0]][action[1]] = EMPTY
      newState.board[action[2]][action[3]] = self.current_player
      newState.push_neighbors(action[2], action[3])
    elif (len(action) == 2): #if the action places a piece onto the board
      newState.board[action[0]][action[1]] = self.current_player
      if newState.current_player == PLAYER1:
        newState.p1_pieces += 1
      else:
        newState.p2_pieces += 1
      newState.push_neighbors(action[0], action[1])
    return newState

  def push_neighbors(self, r0, c0):
    dirs = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]
    for dr, dc in dirs:
      # (r1, c1) is a 1-tile (immediate) neighbor of (r0, c0) in the direction (dr, dc)
      r1, c1 = _torus(r0 + dr, c0 + dc)
      if self.board[r1][c1] != EMPTY:
        # (r2, c2) is a 2-tile (secondary) neighbor of (r0, c0) in the direction (dr, dc)
        r2, c2 = _torus(r1 + dr, c1 + dc)
        if self.board[r2][c2] == EMPTY:
          self.board[r2][c2], self.board[r1][c1] = self.board[r1][c1], self.board[r2][c2]

  def is_terminal(self) -> bool:
    # check rows
    for row in range(0, BOARD_SIZE):
      cnt = 0
      tile = EMPTY
      for col in range(-2, BOARD_SIZE+2):
        r, c = _torus(row, col)
        curr_tile = self.board[r][c]
        if curr_tile == EMPTY:
          cnt = 0
        elif curr_tile != tile:
          cnt = 1
        else:
          cnt += 1
          if (cnt == 3):
            if tile == PLAYER1:
              self.p1win = True
            elif tile == PLAYER2:
              self.p2win = True
        tile = self.board[r][c]

    # check cols
    for col in range(0, BOARD_SIZE):
      cnt = 0
      tile = EMPTY
      for row in range(-2, BOARD_SIZE+2):
        r, c = _torus(row, col)
        curr_tile = self.board[r][c]
        if curr_tile == EMPTY:
          cnt = 0
        elif curr_tile != tile:
          cnt = 1
        else:
          cnt += 1
          if (cnt == 3):
            if tile == PLAYER1:
              self.p1win = True
            elif tile == PLAYER2:
              self.p2win = True
        tile = self.board[r][c]

    # check negative diagonals
    for col_start in range(0, BOARD_SIZE):
      cnt = 0
      tile = EMPTY
      for i in range(-2, BOARD_SIZE+2):
        r, c = _torus(i, col_start + i)
        curr_tile = self.board[r][c]
        if curr_tile == EMPTY:
          cnt = 0
        elif curr_tile != tile:
          cnt = 1
        else:
          cnt += 1
          if (cnt == 3):
            if tile == PLAYER1:
              self.p1win = True
            elif tile == PLAYER2:
              self.p2win = True
        tile = self.board[r][c]

    # check positive diagonals
    for col_start in range(0, BOARD_SIZE):
      cnt = 0
      tile = EMPTY
      for i in range(-2, BOARD_SIZE+2):
        r, c = _torus(i, col_start - i)
        curr_tile = self.board[r][c]
        if curr_tile == EMPTY:
          cnt = 0
        elif curr_tile != tile:
          cnt = 1
        else:
          cnt += 1
          if (cnt == 3):
            if tile == PLAYER1:
              self.p1win = True
            elif tile == PLAYER2:
              self.p2win = True
        tile = self.board[r][c]
    return (self.p1win or self.p2win)

  def get_reward(self) -> float:
    if (self.is_terminal()):
      if (self.p1win):
        return PLAYER1
      elif (self.p2win):
        return PLAYER2
    else:
      return 0

  def get_current_player(self) -> int:
    return self.current_player


initial_state = MyState()
searcher = MCTS(time_limit=4000)
for i in range(10):
    searcher.search(initial_state=initial_state)

bestAction = searcher.search(initial_state=initial_state)
print(bestAction)
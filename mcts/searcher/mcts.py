from __future__ import division

import math
import random
import time

from mcts.base.base import BaseState


def random_policy(state: BaseState) -> float:
    while not state.is_terminal():
        try:
            action = random.choice(state.get_possible_actions())
        except IndexError:
            raise Exception("Non-terminal state has no possible actions: " + str(state))
        state = state.take_action(action)
    return state.get_reward()


class TreeNode:
    def __init__(self, state, parent):
        self.state = state
        self.is_terminal = state.is_terminal()
        self.is_fully_expanded = self.is_terminal
        self.parent = parent
        self.numVisits = 0
        self.totalReward = 0
        self.children = {}

    def __str__(self):
        s = ["totalReward: %s" % self.totalReward,
             "numVisits: %d" % self.numVisits,
             "isTerminal: %s" % self.is_terminal,
             "possibleActions: %s" % (self.children.keys())]
        return "%s: {%s}" % (self.__class__.__name__, ', '.join(s))


class MCTS:
    def __init__(self,
                 timeLimit):
        # backwards compatibility
        self.timeLimit = timeLimit
        
        #exploration constant originally math.sqrt(2)
        #implementing dynamic exploration constant
        self.initial_exploration_constant = math.sqrt(2)
        self.exploration_constant = math.sqrt(2)
        self.decay_factor = 0.999

        self.root = None
        self.rollout_policy = random_policy
        self.prevRoots = {}

    def search(self, initial_state, turnCount = 0):
        self.root = TreeNode(initial_state, None)
        self.initial_exploration_constant = max(0.5, self.initial_exploration_constant-(0.1*turnCount))
        if (turnCount > 6):
            self.decay_factor = 0.9999
        else:
            self.decay_factor = 0.9974

        i = 0
        time_limit = time.time() + self.timeLimit / 1000
        while time.time() < time_limit:
            self.execute_round()
            self.exploration_constant = (self.initial_exploration_constant * (self.decay_factor)**i)
            i += 1
        print(i) 

        best_child = self.get_best_child(self.root, 0)
        action = (action for action, node in self.root.children.items() if node is best_child).__next__()
        return action

    def execute_round(self):
        """
            execute a selection-expansion-simulation-backpropagation round
        """
        node = self.select_node(self.root)
        reward = self.rollout_policy(node.state)
        self.backpropogate(node, reward)

    def select_node(self, node: TreeNode) -> TreeNode:
        while not node.is_terminal:
            if node.is_fully_expanded:
                node = self.get_best_child(node, self.exploration_constant)
            else:
                return self.expand(node)
        return node

    def expand(self, node: TreeNode) -> TreeNode:
        actions = node.state.get_possible_actions()
        for action in actions:
            if action not in node.children:
                newNode = TreeNode(node.state.take_action(action), node)
                node.children[action] = newNode
                if len(actions) == len(node.children):
                    node.is_fully_expanded = True
                return newNode

        raise Exception("Should never reach here")

    def backpropogate(self, node: TreeNode, reward: float):
        while node is not None:
            node.numVisits += 1
            node.totalReward += reward
            node = node.parent

    def get_best_child(self, node: TreeNode, explorationValue: float, exploration_value: float = None) -> TreeNode:
        exploration_value = explorationValue if exploration_value is None else exploration_value
        best_value = float("-inf")
        best_nodes = []
        for child in node.children.values():
            node_value = (node.state.get_current_player() * child.totalReward / child.numVisits +
                          exploration_value * math.sqrt(math.log(node.numVisits) / child.numVisits))
            if node_value > best_value:
                best_value = node_value
                best_nodes = [child]
            elif node_value == best_value:
                best_nodes.append(child)
        return random.choice(best_nodes)

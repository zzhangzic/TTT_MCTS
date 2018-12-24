from __future__ import division
from mcts_node import MCTSNode
from random import choice
from math import sqrt, log
from time import time

num_nodes = 1000
explore_faction = 2.


def traverse_nodes(node, board, state, identity):
    last_value = 0
    return_node = node
    while return_node.child_nodes != {}:
        for x in return_node.child_nodes:
            children = return_node.child_nodes[x]
            temp = return_node.visits/children.visits
            if temp == 0:
                pass
            else:
                temp = log(return_node.visits)/children.visits
            current_value = children.wins/children.visits + sqrt(2) * sqrt(temp)
            if(current_value > last_value):
                last_value = current_value
                if(return_node.parent_action != None):
                    board.next_state(state,return_node.parent_action)
        return_node = children
    return return_node
    pass
    # Hint: return leaf_node


def expand_leaf(node, board, state):
    new_move = choice(node.untried_actions)
    board.next_state(state,new_move)
    new_node = MCTSNode(parent=node, parent_action=new_move, action_list=board.legal_actions(state))
    node.child_nodes[new_move] = new_node
    return new_node
    pass
    # Hint: return new_node


def rollout(board, state):
    win = None
    # moves = board.legal_actions(state)
    for move in board.legal_actions(state):
        new_state = board.next_state(state, move)
        big_board_coor = (move[0], move[1])

        """
        if the commented out code below weren't commented, there would be an error in the if statement

        my implementation was for every move in legal_actions, pick the one that will complete a board
        otherwise, random


        """
        # if check_in_owned_boxes(board, new_state, big_board_coor):
        #     return new_state
        # else:
        #     win = False
    # if not win:
        while (board.is_ended(state) != True):
            state = board.next_state(state, choice(board.legal_actions(state)))
        return state


def check_in_owned_boxes(board, state, coor):
    boxes = board.owned_boxes(state)
    return True if boxes[coor] == 1 else False


def backpropagate(node, won):
    while node.parent != None:
        node.visits += 1
        if won == True:
            node.wins += 1
        node = node.parent
        pass


def think(board, state):
    temp = 0
    last_value = 0
    identity_of_bot = board.current_player(state)
    root_node = MCTSNode(parent=None, parent_action=None, action_list=board.legal_actions(state))
    for step in range(num_nodes):
        # print(step)
        won = False
        sampled_game = state

        node = root_node

        return_node = traverse_nodes(node,board,sampled_game,identity_of_bot)

        newadded_node = expand_leaf(return_node,board,sampled_game)

        sampled_game = rollout(board, sampled_game)
        final_score = board.points_values(sampled_game)
        if final_score[1] == 1:
            won = True
        backpropagate(newadded_node,won)
    # Return an action, typically the most frequently used action (from the root) or the action with the best.
    bestaction = None
    for x in root_node.child_nodes:
        children = root_node.child_nodes[x]
        temp = children.wins/children.visits
        bestaction = children
        if temp > last_value:
            bestaction = children
            last_value = temp
    if bestaction.parent_action in board.legal_actions(state):
        wow = bestaction.wins/bestaction.visits
        print(wow)
        return bestaction.parent_action
    else:
        return choice(board.legal_actions(state))
    # estimated win rate.
    # return None

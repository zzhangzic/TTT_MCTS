from __future__ import division
from mcts_node import MCTSNode
from random import choice
from math import sqrt, log

num_nodes = 500
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
            # current_value = children.wins/children.visits + sqrt(2) * sqrt(temp)
            current_value = children.wins/children.visits + (explore_faction * sqrt(temp))
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
    while(board.is_ended(state)!=True):
        #print(board.is_ended(state))
        state = board.next_state(state,choice(board.legal_actions(state)))
    return state
    pass


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

        sampled_game = rollout(board,sampled_game)
        final_score = board.points_values(sampled_game)
        if final_score[1] == 1:
            won = True
        backpropagate(newadded_node,won)
        # print(root_node.child_nodes)
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
    return None

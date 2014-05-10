from copy import *
from operator import attrgetter
from random import randint

from game.moves import EndAttackMove, AttackMove


__author__ = 'art'

class Bot:

    def __init__(self, id):
        self.id = id

    def attack(self, board):
        pass

    def move_armies_after_attack(self, board, attacked_node, captured_node):
        pass

    def place_armies(self, units, board):
        pass

    def move_armies(self, board):
        pass


class RandomBot(Bot):

    def attack(self, board):
        for node in board.nodes.values():
            if self.id == node.owner and node.army > 1:
                for neighbour in node.neighbours:
                    if neighbour.owner != self.id:
                        return AttackMove(node.id, neighbour.id)
        return EndAttackMove()

    def place_armies(self, units, board):
        #place armies randomly all armies at one country
        my_nodes = board.nodes_by_owner(self.id)
        random_node = randint(0, len(my_nodes) - 1)
        return [(my_nodes[random_node].id, units)]


    def move_armies(self, board):
        from_node = None
        to_node = None
        my_nodes = board.nodes_by_owner(self.id)
        for node in my_nodes:
            has_enemy_neighbours = False
            for neighbour in node.neighbours:
                if neighbour.owner != self.id:
                    to_node = node
                    has_enemy_neighbours = True
            if not has_enemy_neighbours and node.army > 1:
                from_node = node
            if from_node and to_node:
                return from_node.id, to_node.id, from_node.army - 1
        return None, None, 0

    def move_armies_after_attack(self, board, attacked_node, captured_node):
        return board.nodes[attacked_node].army/2


class BetterReinforcingBot(RandomBot):

   def place_armies(self, units, board):
        my_nodes = board.nodes_by_owner(self.id)
        for node in my_nodes:
            #place armies randomly all armies at one country
            for neighbour in node.neighbours:
                if neighbour.owner != self.id:
                    return [(node.id, units)]


class BestReinforcingBot(RandomBot):

    def place_armies(self, units, board):
        nodes_armies = []
        border_nodes = deepcopy(board.border_nodes(self.id))
        for i in range(0, units):
            min_army_node = min(border_nodes,key=attrgetter('army'))
            min_army_node.add_army(1)
            nodes_armies.append((min_army_node.id, 1))
        return nodes_armies

class BetterMovingArmiesAfterAttackBot(BestReinforcingBot):

    def move_armies_after_attack(self, board, attacked_node, captured_node):
        att_node = board.nodes[attacked_node]
        if att_node.is_border_node():
            return 0
        else:
            return att_node.army - 1


__author__ = 'art'

from main.risk.moves import EndAttackMove, AttackMove
from random import shuffle
import logging

logger = logging.getLogger("risk")

class Board:

    def __init__(self, nodes):
        self.nodes = nodes

    def connect_nodes(self, node1_id, node2_id):
        if node1_id != node2_id:
            node1 = self.nodes[node1_id]
            node2 = self.nodes[node2_id]
            node1.neighbours.append(node2)
            node2.neighbours.append(node1)

    def nodes_by_owner(self, owner):
        owned_nodes = []
        for node in self.nodes.values():
            if node.owner == owner:
                owned_nodes.append(node)
        return owned_nodes

    def border_nodes(self, player_id):
        my_nodes = self.nodes_by_owner(player_id)
        border_nodes = []
        for node in my_nodes:
            if node.is_border_node():
                border_nodes.append(node)
        return border_nodes

    def __str__(self):
        to_str = ""
        for key, value in self.nodes.items():
            to_str += str(key) + ":{" + value.__str__() + "},"
        return to_str[:-1]

    class Node:

        def __init__(self, id, owner, army):
            self.id = id
            self.owner = owner
            self.army = army
            self.neighbours = []

        def __str__(self):
            return "id=" + str(self.id) + ", owner=" + str(self.owner) + ", army=" + str(self.army)

        def add_army(self, army):
            self.army += army

        def is_border_node(self):
            for neighbour in self.neighbours:
                if neighbour.owner != self.owner:
                    return True
            return False

class Player:

    def __str__(self):
        return "player=" + str(self.id)

    def __init__(self, id, bot):
        self.id = id
        self.bot = bot
        self.won = 0

    def increase_won(self):
        self.won += 1

    def __str__(self):
        return "player=" + str(self.id) + ", bot=" + self.bot.__class__.__name__ + ", won=" + str(self.won)


class Game:

    def __init__(self, board, players):
        self.board = board
        self.players = players

    def player_by_id(self, id):
        for player in self.players:
            if player.id == id:
                return player

    def is_over(self):
        owner = self.board.nodes.values()[0].owner
        for node in self.board.nodes.values():
            if node.owner != owner:
                return False, None
        return True, owner

    def move_armies(self, bot):
        from_node, to_node, armies = bot.move_armies(self.board)
        if armies != 0:
            self.board.nodes[from_node].add_army((-1) * armies)
            self.board.nodes[to_node].add_army(armies)
            logger.debug("moving: " + str(armies) + " armies from: " + str(from_node) + ", to: " + str(to_node))
            logger.debug(self.board)

    def move_armies_after_attack(self, bot, attacked_node, captured_node):
        armies = bot.move_armies_after_attack(self.board, attacked_node, captured_node)
        self.board.nodes[attacked_node].add_army((-1) * armies)
        self.board.nodes[captured_node].add_army(armies)

    def reinforce_army(self, bot):
        reinforcements = len(self.board.nodes_by_owner(bot.id)) / 2
        if reinforcements < 2:
            reinforcements = 2
        armies_to_move = bot.place_armies(reinforcements, self.board)
        total_units = 0
        for node_id, units in armies_to_move:
            logger.debug("adding " + str(units) + " to: " + str(node_id))
            node = self.board.nodes[node_id]
            if node.owner != bot.id:
                raise StandardError("Can not place reinforcement on enemy node: " + node_id)
            node.add_army(units)
            total_units += units
        if total_units != reinforcements:
            raise StandardError("Wrong reinforcement, actual: " + str(total_units) + " should be: " + str(reinforcements))


        logger.debug(self.board)

    def get_next_player(self):
        player = self.players.pop(0)
        self.players.append(player)
        return player

    def run(self):
        move_num = 1
        shuffle(self.players)
        player = self.get_next_player()

        while not self.is_over()[0]:
            logger.debug("")
            logger.debug("--------------" + "Move = " + str(move_num) + " by " + str(player) + "------------")
            if move_num == 200:
                break

            bot = player.bot
            self.reinforce_army(bot)
            move = bot.attack(self.board)
            while not isinstance(move, EndAttackMove):
                logger.debug(move)
                move.do(self.board, player.id)
                self.move_armies_after_attack(bot, move.attacking_node, move.defending_node)
                logger.debug(self.board)
                move = bot.attack(self.board)
            else:
                self.move_armies(bot)
                player = self.get_next_player()
            move_num += 1

        return self.is_over()[1]

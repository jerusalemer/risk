from random import shuffle
from random import randint
import logging
from main.risk.game import Board

__author__ = 'art'


class Setup:

    def __init__(self):
        pass

    @staticmethod
    def setup_logger():
        #filename='log/risk.log', filemode='w',
        logging.basicConfig(format='%(asctime)s %(message)s' ,level=logging.DEBUG)

    @staticmethod
    def setup_board(players, num_of_nodes):

        Setup().setup_logger()

        nodes = {}
        board = Board(nodes)

        #create empty nodes
        for i in range(0, num_of_nodes):
            nodes[i] = board.Node(i, 0, 1)

        #create connections
        for i in range(1, num_of_nodes):
            board.connect_nodes(i, i - 1)
        board.connect_nodes(0, num_of_nodes - 1)
        for i in range(0, num_of_nodes/4):
            board.connect_nodes(randint(0, num_of_nodes - 1), randint(0, num_of_nodes - 1))

        #split nodes between players
        nodes_to_split = nodes.values()[:]
        shuffle(nodes_to_split)
        for i in range(0, num_of_nodes):
            player_id = i % len(players)
            nodes_to_split[i].owner = player_id

        #split armies between players
        armies_per_node = 3
        armies_per_player = num_of_nodes * (armies_per_node - 1) / len(players)
        for player in players:
            my_nodes = board.nodes_by_owner(player.id)
            for i in range(0, armies_per_player):
                node = my_nodes[randint(0, len(my_nodes) - 1)]
                node.add_army(1)
        return board



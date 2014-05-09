import logging
import time

from bot import RandomBot, BestReinforcingBot
from setup import Setup
from visualization import draw_board
from game import Player, Game


__author__ = 'art'

logger = logging.getLogger("risk")

num_of_nodes = 10
num_of_games = 1
num_of_players = 2
logger.setLevel("INFO")
players = [Player(0, RandomBot(0)), Player(1, BestReinforcingBot(1))]

start_time = time.time()

for j in range(0, num_of_games):

    board = Setup().setup_board(players, num_of_nodes)
    game = Game(board, players)
    logger.debug("")
    logger.debug(board)

    draw_board(board)

    #winner = game.run()
    #game.player_by_id(winner).increase_won()
    #logger.info("Game #" + str(j) + " Over. Winner" + str(winner))

logger.info("")
logger.info("---------------------------------")
logger.info("Winners: ")
for player in players:
    logger.info(player)
logger.info(str(time.time() - start_time) +  "seconds")
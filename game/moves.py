__author__ = 'art'

from random import randint


class Move:
    def do(self, board, player):
        pass


class AttackMove(Move):

    def __init__(self, attacking_node, defending_node):
        self.attacking_node = attacking_node
        self.defending_node = defending_node

    def __str__(self):
        return "Attacking: " + str(self.attacking_node) + "->" + str(self.defending_node)


    def do(self, board, player):
        att_node = board.nodes[self.attacking_node]
        def_node = board.nodes[self.defending_node]

        if att_node.owner != player or def_node.owner == player:
            raise StandardError("Illegal attack: " + str(self))


        if def_node not in att_node.neighbours:
            raise AssertionError("" + att_node + " and " + def_node + " are not neighbours")

        success, att_node.army, def_node.army = self.__attack(att_node.army, def_node.army)
        if success:
            def_node.army = 1
            def_node.owner = att_node.owner
            att_node.add_army(-1)

    def __attack(self, attackers, defenders):
        if defenders == 0:
            #__print_stats("attackers won.", attackers, defenders)
            return True, attackers, defenders
        elif attackers == 1:
            #__print_stats("defenders won.", attackers, defenders)
            return False, attackers, defenders

        att_number = 3
        if attackers == 2:
            att_number = 2

        def_num = 2
        if defenders == 1:
            def_num = 1

        lost_att, lost_def = self.__attack_single_round(att_number, def_num)
        return self.__attack(attackers - lost_att, defenders - lost_def)

    @staticmethod
    def __attack_single_round(attackers, defenders):
        att_cubes = []
        def_cubes = []
        for i in range(attackers):
            att_cubes.append(randint(1, 6))
        for i in range(defenders):
            def_cubes.append(randint(1, 6))

        att_cubes.sort(reverse=True)
        def_cubes.sort(reverse=True)

        lost_att = 0
        lost_def = 0

        att_cubes.pop()

        for att_value in att_cubes:
            if not def_cubes:
                break
            def_value = def_cubes.pop(0)
            if def_value >= att_value:
                lost_att += 1
            else:
                lost_def += 1

        return lost_att, lost_def


class EndAttackMove(Move):
    def __init__(self):
        pass

    def do(self, board, player):
        pass

    def __str__ (self):
        return "End turn"




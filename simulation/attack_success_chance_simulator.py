from random import randint

ROUNDS = 10000

__author__ = 'art'


def __print_stats(msg, attackers, defenders):
    print msg, "attackers:", attackers, "defenders:", defenders


def attack(attackers, defenders):
    if defenders == 0:
        #__print_stats("attackers won.", attackers, defenders)
        return attackers, defenders
    elif attackers == 1:
        #__print_stats("defenders won.", attackers, defenders)
        return attackers, defenders

    att_number = 3
    if attackers == 2:
        att_number = 2

    def_num = 2
    if defenders == 1:
        def_num = 1

    lost_att, lost_def = attack_single_round(att_number, def_num)
    return attack(attackers - lost_att, defenders - lost_def)


def attack_single_round(attackers, defenders):
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


def should_attack(attackers, defenders):
    lost_att = 0
    lost_def = 0
    att_won = 0
    for i in (range(ROUNDS)):
        left_att, left_def = attack(attackers, defenders)
        lost_att = lost_att + attackers - left_att
        lost_def = lost_def + defenders - left_def
        if left_def == 0:
            att_won += 1

    print "attackers won", 100 * att_won / ROUNDS, "% rounds"
    print "lost att units of total loss =", lost_att*100/(lost_def + lost_att), "%"
    print "att loses on average", (1.0 * lost_att)/ROUNDS, "def loses on average", (1.0 * lost_def)/ROUNDS, "units"

import time
start_time = time.time()

for att in range(2, 4):
    for defend in range(1, 10):
        print "------------------attackers =", att, " defenders =", defend, "-----------------------"
        should_attack(att, defend)
        print "------------------------------------------------------------------------"
        print ""


print time.time() - start_time, "seconds"


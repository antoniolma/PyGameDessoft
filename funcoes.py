from assets import *
from player_class import Munition

def addGroup(sprite, group, name):
    for g in group:
        g.add(sprite)
    groups[name].add(sprite)


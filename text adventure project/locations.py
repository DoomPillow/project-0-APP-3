import enemies as enemy
import items as itm
from dialogue_test import DialogueTree, path

class Location():
    def __init__(self):
        dialogue_trees = {}
        fights = {}

###############################

class Admin(Location):
    def __init__(self):

        self.active_tree = None

        self.checks = {
            "bogem": True
        }

        self.dialogue_trees = {
            "default": DialogueTree.load_from_file(path + 'admin/mr_tran_opening.json', self),
            "mr_tran_room": DialogueTree.load_from_file(path + 'admin/mr_tran_room.json', self),
            "mr_chen_hallway": DialogueTree.load_from_file(path + 'admin/mr_chen_hallway.json', self)
        }
        self.fights = {
            "dog_agents": {
                "enemies": [enemy.DogAgent("D.O.G Agent 1"), enemy.DogAgent("D.O.G Agent 2"), enemy.DogAgent("D.O.G Agent 3"), enemy.DogAgent("D.O.G Agent 4"), enemy.DogAgent("D.O.G Agent 5"), enemy.DogAgent("D.O.G Agent 6")],
                "loot": [15, itm.bandaid()]
            },
            "mr_chen": {
                "enemies": [enemy.MrChen()],
                "loot": [30, itm.cigarette(), itm.cigarette(), itm.bandaid]
            }
        }

class EQuad(Location):
    def __init__(self):

        self.active_tree = None

        self.dialogue_trees = {
            "default": DialogueTree.load_from_file(path + 'lunch area/lunch_area.json', self),
        }
        self.fights = {}

###############################

locations = {
    "admin": Admin(),
    "e_quad": EQuad()
}

###############################

current_location = locations["admin"]
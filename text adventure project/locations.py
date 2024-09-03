import enemies as enemy
import items as itm
from dialogue_test import DialogueTree, path

class Location():
    def __init__(self):
        dialogue_trees = {}
        fights = {}

########


class Admin(Location):
    def __init__(self):
        self.dialogue_trees = {
            "default":   DialogueTree.load_from_file(path + 'dg_mrtran_001.json', self),
        }
        self.fights = {
            "dog_agents": {
                "enemies": [enemy.DogAgent("D.O.G Agent 1"), enemy.DogAgent("D.O.G Agent 2"), enemy.DogAgent("D.O.G Agent 3"), enemy.DogAgent("D.O.G Agent 4"), enemy.DogAgent("D.O.G Agent 5"), enemy.DogAgent("D.O.G Agent 6")],
                "loot": [15, itm.bandaid()]
            }
        }

location_admin = Admin()
location_admin.dialogue_trees["default"].run()
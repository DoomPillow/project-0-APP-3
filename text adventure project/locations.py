import enemies as enemy
import items as itm
from dialogue_test import DialogueTree, path

###############################

class World():
    def __init__(self):

        self.active_tree = None

        self.checks = {
            "cafe_rats_battled": False,
            "govt_cheese": False
        }

        self.dialogue_trees = {
            "default": DialogueTree.load_from_file(path + 'admin/mr_tran_opening.json', self),
            "mr_tran_room": DialogueTree.load_from_file(path + 'admin/mr_tran_room.json', self),
            "mr_chen_hallway": DialogueTree.load_from_file(path + 'admin/mr_chen_hallway.json', self),
            "lunch_area": DialogueTree.load_from_file(path + 'lunch area/lunch_area.json', self),
            "cafeteria": DialogueTree.load_from_file(path + 'lunch area/cafeteria.json', self),
            "garden": DialogueTree.load_from_file(path + 'lunch area/garden.json', self),
            "rat_dungeon": DialogueTree.load_from_file(path + 'lunch area/rat_dungeon.json', self)
        }
        self.fights = {
            "dog_agents": {
                "enemies": [enemy.DogAgent("D.O.G Agent 1"), enemy.DogAgent("D.O.G Agent 2"), enemy.DogAgent("D.O.G Agent 3"), enemy.DogAgent("D.O.G Agent 4"), enemy.DogAgent("D.O.G Agent 5"), enemy.DogAgent("D.O.G Agent 6")],
                "loot": [1000, itm.milk()]
            },
            "mr_chen": {
                "enemies": [enemy.MrChen()],
                "loot": [35, itm.cigarette(), itm.cigarette(), itm.bandaid()]
            },
            "cafe_rats": {
                "enemies": [enemy.Rat("Rat 1"), enemy.Rat("Rat 2"), enemy.Rat("Rat 3"), enemy.Rat("Rat 4"), enemy.Rat("Rat 5")],
                "loot": [20, itm.milk()]
            },
            "guard_rats": {
                "enemies": [enemy.RatGuard("Rat Guard 1"), enemy.RatGuard("Rat Guard 2")],
                "loot": [50, itm.bandaid(), itm.bandaid(), itm.hobobomb()]
            },
            "ant_heroes": {
                "enemies": [enemy.AntAchilles(), enemy.AntHercules(), enemy.AntSpartacus()],
                "loot": [100]
            }
        }

###################

world = World()
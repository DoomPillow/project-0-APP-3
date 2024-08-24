import random
from conditions import conditions

### Item Class
class Item:
    def __init__(self):
        self.name = "undefined"
        self.itemid = -1
        self.description = "this looks broken and like the dev doesn't want you to see this"

### Specific Items
class itm_bomb(Item):
    def __init__(self):
        super().__init__()
        self.name = "Bomb"
        self.emojo = "🧨"
        self.itemid = 0
        self.description = "An explosive weapon dealing a decent amount of damage."
    
    def use(self, target, player):
        dmg = random.randint(4, 8)
        print(f"> 💥💥💥 You blow up {target.name} for {dmg} damage!!! 💥💥💥")
        target.hp -= dmg

class itm_pill(Item):
    def __init__(self):
        super().__init__()
        self.name = "Pill"
        self.emojo = "💊"
        self.itemid = 1
        self.description = "A delicious little capsule that heals you."
    
    def use(self, target, player):
        heal = random.randint(4, 6)
        player.hp = min(player.hp + heal, player.hpmax)
        print(f"> You down a pill and heal to ❤ {player.hp} hp!")

class itm_cam(Item):
    def __init__(self):
        super().__init__()
        self.name = "Disposable Camera"
        self.emojo = "📷"
        self.itemid = 2
        self.description = "A very cheap disposable camera. Its bright flash can stun an enemy for a couple rounds."
    
    def use(self, target, player):
        print(f"> You camera flash {target.name}, stunning them!")
        target.apply_condition(conditions["stunned"], duration = 3)

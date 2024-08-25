import random
from conditions import conditions
import time

### Item Class
class Item:
    def __init__(self):
        self.name = "undefined"
        self.emojo = "❔"
        self.description = "this looks broken and like the dev doesn't want you to see this"

### Specific Items
class itm_bomb(Item):
    def __init__(self):
        super().__init__()
        self.name = "Bomb"
        self.emojo = "🧨"
        self.description = "An explosive weapon dealing a decent amount of damage."
    
    def use(self, target, player, enemies):
        print("You hurl a stick of dynamite onto the battlefield...")
        time.sleep(0.85)
        for enemy in enemies:
            dmg = random.randint(4, 8)
            print(f"> 💥 You blow up {enemy.name} for {dmg} damage!!! 💥")
            enemy.hp -= dmg
            time.sleep(0.3)

class itm_pill(Item):
    def __init__(self):
        super().__init__()
        self.name = "Pill"
        self.emojo = "💊"
        self.description = "A delicious little capsule that heals you."
    
    def use(self, target, player, enemies):
        heal = random.randint(4, 6)
        player.hp = min(player.hp + heal, player.hpmax)
        print(f"> You down a pill and heal to ❤ {player.hp} hp!")

class itm_cam(Item):
    def __init__(self):
        super().__init__()
        self.name = "Disposable Camera"
        self.emojo = "📷"
        self.description = "A very cheap disposable camera. Its bright flash can stun an enemy for a couple rounds."
    
    def use(self, target, player, enemies):
        print(f"> You camera flash {target.name}, stunning them!")
        target.apply_condition(conditions["stunned"], duration = 3)

class itm_juice(Item):
    def __init__(self):
        super().__init__()
        self.name = "Juice Box"
        self.emojo = "🧃"
        self.description = "A bland yet refreshing juice. Recovers some energy."
    
    def use(self, target, player, enemies):
        heal = random.randint(15, 30)
        player.pp = min(player.pp + heal, player.ppmax)
        print(f"> You slurp down the juice box and recover ⚡{heal} energy!")
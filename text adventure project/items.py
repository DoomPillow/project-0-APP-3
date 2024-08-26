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
        print("> You hurl a stick of dynamite onto the battlefield...")
        time.sleep(0.85)
        for enemy in enemies:
            dmg = random.randint(4, 8)
            print(f"> 💥 You blow up {enemy.name} for {dmg} damage!!! 💥")
            enemy.hp -= dmg
            time.sleep(0.3)

class itm_pill(Item):
    def __init__(self):
        super().__init__()
        self.name = "Painkiller"
        self.emojo = "💊"
        self.description = "It stops the pain, but temporarily makes you weaker."
    
    def use(self, target, player, enemies):
        heal = 10
        player.hp = min(player.hp + heal, player.hpmax)
        player.dmgbonus -= 1
        print(f"> You down a painkiller, and recover ❤️ {heal} hp!")

class itm_bandaid(Item):
    def __init__(self):
        super().__init__()
        self.name = "Bandaid"
        self.emojo = "🩹"
        self.description = "Heals a moderate amount."
    
    def use(self, target, player, enemies):
        heal = random.randint(5, 9)
        player.hp = min(player.hp + heal, player.hpmax)
        print(f"> You slap a bandaid on your gushing wounds, and recover ❤️ {heal} hp!")

class itm_cam(Item):
    def __init__(self):
        super().__init__()
        self.name = "Disposable Camera"
        self.emojo = "📷"
        self.description = "A very cheap disposable camera. Its bright flash can stun an enemy for a couple rounds."
    
    def use(self, target, player, enemies):
        print(f"> 📸 You camera flash {target.name}, stunning them!")
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

class itm_cigarette(Item):
    def __init__(self):
        super().__init__()
        self.name = "Cigarette"
        self.emojo = "🚬"
        self.description = "Mmmmm... lung cancer. Cures poison."
    
    def use(self, target, player, enemies):
        heal = random.randint(15, 30)
        player.pp = min(player.pp + heal, player.ppmax)
        print(f"> You slurp down the juice box and recover ⚡{heal} energy!")

class itm_soap(Item):
    def __init__(self):
        super().__init__()
        self.name = "Soap Bar"
        self.emojo = "🧼"
        self.description = "A sudsy bar of soap. Can be thrown to make your opponents slippery."
    
    def use(self, target, player, enemies):
        print("> 🫧  You hurl the bar of soap onto the battlefield, slipperying everyone up!")
        time.sleep(0.85)
        for enemy in enemies:
            enemy.apply_condition(conditions["soapy"], duration = random.randint(2,4))

class itm_hobobomb(Item):
    def __init__(self):
        super().__init__()
        self.name = "Hobo Bomb"
        self.emojo = "🧦"
        self.description = "A terrible-smelling fibrous green ball wrapped up in a sock. It smells poisonous."
    
    def use(self, target, player, enemies):
        print("> You hurl the Hobo Bomb onto the battlefield... poisoning everyone!")
        time.sleep(0.85)
        for enemy in enemies:
            enemy.apply_condition(conditions["poisoned"], duration = random.randint(2,4))
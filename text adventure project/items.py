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
class bomb(Item):
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

class pill(Item):
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

class bandaid(Item):
    def __init__(self):
        super().__init__()
        self.name = "Bandaid"
        self.emojo = "🩹"
        self.description = "Heals a moderate amount."
    
    def use(self, target, player, enemies):
        heal = random.randint(5, 9)
        player.hp = min(player.hp + heal, player.hpmax)
        print(f"> You slap a bandaid on your gushing wounds, and recover ❤️ {heal} hp!")

class burger(Item):
    def __init__(self):
        super().__init__()
        self.name = "Burger"
        self.emojo = "🍔"
        self.description = "Homemade! Heals you fully."
    
    def use(self, target, player, enemies):
        player.hp = player.hpmax
        print(f"> You gorge down the burger, and heal back up to ❤️ {player.hpmax} hp!")

class cam(Item):
    def __init__(self):
        super().__init__()
        self.name = "Disposable Camera"
        self.emojo = "📷"
        self.description = "A very cheap disposable camera. Its bright flash can stun an enemy for a couple rounds."
    
    def use(self, target, player, enemies):
        print(f"> 📸 You camera flash {target.name}, stunning them!")
        target.apply_condition(conditions["stunned"], duration = 3)

class juice(Item):
    def __init__(self):
        super().__init__()
        self.name = "Juice Box"
        self.emojo = "🧃"
        self.description = "A bland yet refreshing juice. Recovers some energy."
    
    def use(self, target, player, enemies):
        heal = random.randint(15, 30)
        player.pp = min(player.pp + heal, player.ppmax)
        print(f"> You slurp down the juice box and recover ⚡{heal} energy!")

class cigarette(Item):
    def __init__(self):
        super().__init__()
        self.name = "Cigarette"
        self.emojo = "🚬"
        self.description = "Smooooooooooothhhhh. Cures all ailments. May lower your lifespan."
    
    def use(self, target, player, enemies):
        print("> You eat a cigarette. You feel better.")
        for condition in player.active_conditions:
            player.active_conditions[condition] = 0
        time.sleep(1.0)
        player.rebuff()

class soap(Item):
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

class hobobomb(Item):
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

##### debug items

class cancer(Item):
    def __init__(self):
        super().__init__()
        self.name = "Pure Liquid Cancer"
        self.emojo = "🧪"
        self.description = "You probably shouldn't drink this."
    
    def use(self, target, player, enemies):
        player.hp = 0
        print(f"> You drink the liquid and instantly become a ball of cancer.")

class itm_nuke(Item):
    def __init__(self):
        super().__init__()
        self.name = "Nuclear Bomb"
        self.emojo = "☢️"
        self.description = "Why do you have this? You shouldn't be allowed to have this."
    
    def use(self, target, player, enemies):
        print("> You poke the nuclear bomb, and it detonates!")
        time.sleep(0.85)
        for enemy in enemies:
            dmg = random.randint(400, 800)
            print(f"> 💥 You blow up {enemy.name} for {dmg} damage!!! 💥")
            enemy.hp -= dmg
            time.sleep(0.5)

class itm_milk(Item):
    def __init__(self):
        super().__init__()
        self.name = "Milk Carton"
        self.emojo = "🥛"
        self.description = "Makes you STRONG! RRRAAAAAAAGGGGHHHHH!!!"
    
    def use(self, target, player, enemies):
        player.dmgbonus += 3
        print(f"> 💪 You shotgun the milk carton, and your muscles grow to ten times their size!")
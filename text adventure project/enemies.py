
import random
import time
from conditions import conditions

dead_enemies = []

#### DEFAULT ENEMY

class Enemy:
    def __init__(self, name, hp):
        self.emojo = "❤️"
        self.name = name
        self.hpmax = hp
        self.hp = self.hpmax
        self.dead = False

        self.dmgbonus = 0
        self.hitratio = 75 # % chance of hitting

        self.active_conditions = {}
        #self.moves = [
        #    self.attack
        #]

    def apply_condition(self, condition, duration):
        if condition.name in self.active_conditions:
            self.active_conditions[condition.name] += duration
        else:
            self.active_conditions[condition.name] = duration
            condition.apply(self)

    def attack(self, player):
        if random.randint(1, 100) <= self.hitratio:
            dmg = random.randint(1, 3 + self.dmgbonus)
            print(f"> {self.name} smacks you for {dmg} damage!!!")
            player.hp -= dmg
            time.sleep(1.0)
        else:
            print(f"> {self.name} takes a swing... but misses!")
            time.sleep(1.0)    

    def make_turn(self, player):
        self.attack(player)


    def rebuff(self, player):

        ## Do condition stuff
        expired_conditions = []

        for condition_name, duration in self.active_conditions.items():
            self.active_conditions[condition_name] = max(duration - 1, 0)
            if conditions[condition_name].reapply:
                conditions[condition_name].apply(self)
                
            if self.active_conditions[condition_name] == 0:
                expired_conditions.append(condition_name)

        for condition_name in expired_conditions:
            condition = conditions[condition_name]
            condition.remove(self)
            del self.active_conditions[condition_name]

        ## Check if I'm dead
        if self.hp <= 0 and not self.dead:
            self.dead = True
            self.hp = 0 # just so hp doesn't go negative cuz that looks gross
            print(f"> 🪦  {self.name} drops dead!")
            time.sleep(0.3)
            if player.target == self:
                player.target = None
            dead_enemies.append(self)
            return

    def has_condition(self, condition_name):
        return self.active_conditions.get(condition_name, 0) > 0

############ SPECIFIC ENEMIES

class MrTran(Enemy):
    def __init__(self):
        super().__init__("Mr Tran", 30)

    def noxious_spray(self, player):
        print("> Mr Tran sprays you with noxious chemicals!")
        if player.has_condition("poisoned"):
            self.attack(player)
            return
        player.apply_condition(conditions["poisoned"], 3)
        time.sleep(1.0)

    def make_turn(self, player):
        #super().make_turn(player)
        self.attack(player)

class DogAgent(Enemy):
    def __init__(self, name):
        super().__init__(name, 50)
        self.hitratio = 90

    def attack(self, player):
        if random.randint(1, 100) <= self.hitratio:
            dmg = random.randint(8, 15 + self.dmgbonus)
            print(f"> {self.name} unloads bullets into you for {dmg} damage!!!")
            player.hp -= dmg
            time.sleep(1.0)
        else:
            print(f"> {self.name}'s gun is jammed.")
            time.sleep(1.0)    

    def make_turn(self, player):
        self.attack(player)

class Rat(Enemy):
    def __init__(self, name):
        super().__init__(name, 10)
        self.hitratio = 70

    def idle(self):
        messages = [
            f"> {self.name} scuttles around doing rat things for a moment",
            f"> {self.name} doesn't quite know where it is.",
            f"> {self.name} sniffs you.",
            f"> {self.name} wants to bite you but doesn't remember how.",
            f"> {self.name} chases its own tail."
        ]
        print(messages[random.randint(0,len(messages) - 1)])
        time.sleep(1.0)

    def attack(self, player):
        if random.randint(1, 100) <= self.hitratio:
            dmg = random.randint(1, 2 + self.dmgbonus)
            print(f"> {self.name} takes a chomp at you, for {dmg} damage!!!")
            player.hp -= dmg
            time.sleep(1.0)
        else:
            print(f"> {self.name} tries to chomp you... but misses!")
            time.sleep(1.0)    

    def make_turn(self, player):
        #super().make_turn(player)
        rando = random.randint(0,10)
        if rando < 6:
            self.attack(player)
        else:
            self.idle()

class MrChen(Enemy):
    def __init__(self):
        super().__init__("Mr Chen", 50)
        self.hitratio = 80

    def burn(self, player):
        if not player.has_condition("fire"):
            print(f"> {self.name} puts out his cigarette on you, setting you on fire!")
            player.apply_condition(conditions["fire"], 4)
            time.sleep(1.0)
        else:
            self.attack(player)

    def attack(self, player):
        if random.randint(1, 100) <= self.hitratio:
            
            # Damage
            dmg = random.randint(1, 3 + self.dmgbonus)
            # Message stuff
            match(random.randint(0,4)):
                case 0: print(f"> {self.name} punches you with his brass knuckles for {dmg} damage!!!")
                case 1: print(f"> {self.name} punches you in the gut, dealing {dmg} damage!!!")
                case 2: print(f"> {self.name} gives you a knuckle sandwich, for {dmg} damage!!!")
                case 3: print(f"> {self.name} hits you with the ol' one-two for {dmg} damage!!!")
                case 4: print(f"> {self.name} kicks you in the thorax for {dmg} damage!!!")
                
            # Do stuff
            player.hp -= dmg
            time.sleep(1.0)
        else:
            match(random.randint(0,4)):
                case 0: print(f"> {self.name} takes a swing at you... but misses!")
                case 1: print(f"> {self.name} slips... and misses!")
                case 2: print(f"> {self.name} jabs at you... but misses!")
                case 3: print(f"> {self.name} forgets where he is for a moment")
                case 4: print(f"> {self.name} reconsiders his life choices")            
            time.sleep(1.0)    

    def make_turn(self, player):

        if self.hp < self.hpmax*0.5 and not self.has_condition("angry"):
            print(f"> 💢 {self.name} is furious!")
            self.apply_condition(conditions["angry"], 100)
            time.sleep(1.0)

        if random.randint(1,5) > 2:
            self.attack(player)
        else:
            self.burn(player)

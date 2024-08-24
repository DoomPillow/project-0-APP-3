import time
import random
from items import itm_bomb, itm_pill, itm_cam
from conditions import conditions

##### Player Class
class Player:
    def __init__(self):
        self.emojo = "❤️"
        self.hpmax = 10
        self.hp = self.hpmax
        self.ppmax = 50
        self.pp = self.ppmax
        self.inventory = [itm_bomb(), itm_pill(), itm_pill(), itm_bomb(), itm_cam()]

        self.dmgbonus = 0
        self.hitratio = 90 # % chance of hitting


player = Player()

##### Enemy Class
class Enemy:
    def __init__(self, name, hp):
        self.emojo = "❤️"
        self.name = name
        self.hpmax = hp
        self.hp = self.hpmax

        self.dmgbonus = 0
        self.hitratio = 75 # % chance of hitting

        self.active_conditions = {}

    def apply_condition(self, condition, duration):
        if condition.name in self.active_conditions:
            self.active_conditions[condition.name] += duration
        else:
            self.active_conditions[condition.name] = duration
            condition.apply(self)

    def rebuff(self):
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

    def has_condition(self, condition_name):
        return self.active_conditions.get(condition_name, 0) > 0


##### Initialize Player and Enemy

enemy = Enemy("Mr. Tran", 30)

fight_state = "ongoing"
player_turn = True

### End fight 

def check_for_outcome():
    global fight_state

    if player.hp <= 0:
        fight_state = "playerlose"
        return True
    if enemy.hp <= 0:
        fight_state = "playerwin"
        return True
    return False

##### Game Loop
while fight_state == "ongoing":
    
    #### Player Turn
    if player_turn:

        enemy.rebuff()
        # Check to see if fight is over in case the buffs killed an enemy
        if check_for_outcome():
            break;

        print("-----------------------------------------------")
        print(f"Player  {player.emojo} {player.hp}/{player.hpmax}      vs      {enemy.emojo} {enemy.hp}/{enemy.hpmax} {enemy.name}")
        print(f"        ⚡ {player.pp}/{player.ppmax} ")
        print("-----------------------------------------------")
        print("""
        **Actions**
        - attack
        - abilities
        - ability [ability #]
        - inventory
        - examine [item name]
        - use [item name]
        - flee
        """)
        
        move_on = False
        
        while not move_on:
            action = input(":: what do you want to do? ").lower().split(' ')
           
            match action[0]:
               
                case "attack":
                    dmg = random.randint(1, 3 + player.dmgbonus)
                    print(f"> You beat {enemy.name} for {dmg} damage!!!")
                    enemy.hp -= dmg
                    move_on = True
             
                case "inventory":
                    if len(player.inventory) > 0:
                        for i in range(len(player.inventory)):
                            print(f"{i+1} | {player.inventory[i].emojo} {player.inventory[i].name}")
                    else:
                        print("Your inventory is empty :(")
               
                case "abilities":
                    print("""
    1 | Power Stance    : ⚡ 0 Recover a small amount of energy
    2 | Bulldog Beating : ⚡ 15 A strong attack that's likely to miss
    3 | Taunt           : ⚡ 10 Makes you deal and take more damage for two rounds
    4 | Ptooie          : ⚡ 15 you spit on your opponent, poisoning them for five rounds
    5 | Headbutt        : ⚡ 20 A strong attack with a chance to stun for one round
                    """)
                    
                case "ability":
                    match (int(action[1])):
                        case 2: ## Bulldog Beating
                            if player.pp >= 15:
                                player.pp -= 15
                                if random.randint(1, 5) > 2:
                                    dmg = random.randint(4, 10 + player.dmgbonus)
                                    print(f"> You hurl yourself toward {enemy.name}, dealing {dmg} damage!!!")
                                    enemy.hp -= dmg
                                else:
                                    print(f"> You hurl yourself toward {enemy.name}, but miss!")
                                
                                move_on = True
                            else:
                                print("❌ You don't have enough energy for that")
                            
                        case 3: ## Taunt
                            if player.pp >= 10:
                                player.pp -= 10
                                print(f"> You do a little dance, which makes {enemy.name} turn red with rage!")
                                enemy.apply_condition(conditions["angry"], duration = 4)
                                move_on = True
                            else:
                                print("❌ You don't have enough energy for that")
                        case 4: ## Ptooie
                            if player.pp >= 20:
                                player.pp -= 20
                                print(f"You huak a loogie at {enemy.name}, instantly befouling them with your vile disease!")
                                enemy.apply_condition(conditions["poisoned"], duration = 6)
                                move_on = True
                            else:
                                print("❌ You don't have enough energy for that")
                        case 1: ## Power Stance
                            energy = random.randint(3, 14)
                            print(f"> You recover {energy} energy!")
                            player.pp = min(player.pp + energy, player.ppmax)
                            move_on = True
                        case 5: ## Headbutt
                            if player.pp >= 20:
                                player.pp -= 20
                                dmg = random.randint(4, 7 + player.dmgbonus)
                                print(f"> You bash your skull against {enemy.name}, dealing {dmg} damage!!!")
                                enemy.hp -= dmg
                                if random.randint(1,3) == 1:
                                    #print(f"> {enemy.name} is stunned!")
                                    enemy.apply_condition(conditions["stunned"], duration = 2 )
                            
                                move_on = True
                            else:
                                print("❌ You don't have enough energy for that")
               
                case "examine":
                    found = False;
                    for _item in player.inventory:
                        if  " ".join(action) == f"examine {_item.name.lower()}":
                            print(f"\n{_item.emojo} *{_item.name}*\n{_item.description}\n")
                            found = True
                            break
                    if not found:
                        print("❌ You can't look at something you don't have.")

                case "use":
                    for _item in player.inventory:
                        if  " ".join(action) == f"use {_item.name.lower()}":
                            _item.use(enemy, player)
                            player.inventory.remove(_item)
                            move_on = True
                            break
                    if not move_on:
                        print("❌ That's not an item you have bud.")
              
                case "flee":
                    move_on = True
                    fight_state = "fleed"
    
                case _:
                    print("❌ That's not a command. Try harder.")

    ##################### Enemy Turn   
    else:
        if enemy.has_condition("stunned"):
            print(f"> 💫 {enemy.name} is stunned..")
        else:
            if random.randint(1, 100) <= enemy.hitratio:
                dmg = random.randint(1, 3 + enemy.dmgbonus)
                print(f"> {enemy.name} smacks you for {dmg} damage!!!")
                player.hp -= dmg
            else:
                print(f"> {enemy.name} takes a swing... but misses!")
        
    # End fight if conditions are met
    if check_for_outcome():
        break;
    
    # Reset
    player_turn = not player_turn
    time.sleep(1.0)

### Game over message
match(fight_state):
    case "fleed":
        print("You ran away! Coward.")
    case "playerlose":
        print("You died. L")
    case "playerwin":
        print(f"You defeated {enemy.name}! Good job.")
    case _:
        print("Someone won. Dunno who.")

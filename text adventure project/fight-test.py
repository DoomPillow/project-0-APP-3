import time
import random
from items import itm_bomb, itm_pill, itm_cam, itm_juice, itm_soap, itm_bandaid
from conditions import conditions

round_num = 0

##### Player Class
class Player:
    def __init__(self):
        self.emojo = "❤️"
        self.hpmax = 25
        self.hp = self.hpmax
        self.ppmax = 50
        self.pp = self.ppmax
        self.inventory = [itm_bomb(), itm_pill(), itm_pill(), itm_bomb(), itm_cam(), itm_juice(), itm_juice(), itm_soap(), itm_bandaid(), itm_bandaid()]
        self.target = None

        self.dmgbonus = 0
        #self.hitratio = 90 # % chance of hitting # currently doesn't do anything


player = Player()
dead_enemies = []

##### Enemy Class
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

    def apply_condition(self, condition, duration):
        if condition.name in self.active_conditions:
            self.active_conditions[condition.name] += duration
        else:
            self.active_conditions[condition.name] = duration
            condition.apply(self)

    def rebuff(self):

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
            if player.target == self:
                player.target = None
            dead_enemies.append(self)
            return

    def has_condition(self, condition_name):
        return self.active_conditions.get(condition_name, 0) > 0


##### Initialize Fight

#enemies = [Enemy("Bodyguard 1", 20), Enemy("Mr Tran", 35), Enemy("Bodyguard 2", 20)]
enemies = [Enemy("Junior Recruit 1", 25), Enemy("Junior Recruit 2", 25), Enemy("Junior Recruit 3", 25)]

fight_state = "ongoing"
player_turn = True

### End fight 

def check_for_outcome():
    global fight_state
    
    if player.hp <= 0:
        fight_state = "playerlose"
        return True
    if len(enemies) == 0:
        fight_state = "playerwin"
        return True
    return False

print("(Type 'actions' for a list of commands)")

##### Game Loop
while fight_state == "ongoing":
    
    #### Player Turn
    if player_turn:
        
        # Update the state of each enemy
        for enemy in enemies:
            enemy.rebuff()

        # Remove all of the dead enemies from the enemy list
        for corpse in dead_enemies:
            enemies.remove(corpse)
        dead_enemies.clear()

        # Check to see if fight is over in case the buffs killed an enemy
        if check_for_outcome():
            break;

        if player.target == None:
            player.target = enemies[0]

        print("---------------------------------------------------")
        print(f"    Player {player.emojo} {player.hp}/{player.hpmax} ⚡{player.pp}/{player.ppmax}")
        print("                 · · · · vs. · · · ·")
        for enemy in enemies:
            print(f"            {enemy.emojo} {enemy.hp}/{enemy.hpmax}          {enemy.name}")
        #print("---------------------------------------------------")

        
        move_on = False
        
        while not move_on:
            action = input(f":: what do you want to do? (⯐ {player.target.name if player.target != None else "None"}): ").lower().split(' ')
           
            match action[0]:
                
                case "actions":
                    print("""
**Actions**
- attack
- target [enemy name]
- abilities
- ability [ability #]
- inventory
- examine [item name]
- use [item name]
- flee""")
                case "target":
                    target_name = " ".join(action).replace("target ", "")
                    found = False
                    for enemy in enemies:
                        if enemy.name.lower() == target_name and not enemy.dead:
                            player.target = enemy
                            found = True
                            break
                    if found == False:
                        print("❌ You can't target that")
                case "attack":
                    if player.target == "none":
                        print("❌ You need to actually target someone.")
                    else:
                        dmg = random.randint(1, max(3 + player.dmgbonus, 1) )
                        print(f"> You beat {player.target.name} for {dmg} damage!!!")
                        player.target.hp -= dmg
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
                    if len(action) <= 1:
                        print("❌ You need to specify which ability you want to use")
                    else:
                        match (int(action[1])):
                            case 2: ## Bulldog Beating
                                if player.pp >= 15:
                                    if player.target == "none":
                                        print("❌ You need to actually target someone.")
                                    else:
                                        player.pp -= 15
                                        if random.randint(1, 5) > 2:
                                            dmg = random.randint(4, 12 + player.dmgbonus)
                                            print(f"> You hurl yourself toward {player.target.name}, dealing {dmg} damage!!!")
                                            player.target.hp -= dmg
                                        else:
                                            print(f"> You hurl yourself toward {player.target.name}, but miss!")
                                        
                                        move_on = True
                                else:
                                    print("❌ You don't have enough energy for that")
                                
                            case 3: ## Taunt
                                if player.pp >= 10:
                                    if player.target == "none":
                                        print("❌ You need to actually target someone.")
                                    else:
                                        player.pp -= 10
                                        print(f"> You do a little dance, which makes {player.target.name} turn red with rage!")
                                        player.target.apply_condition(conditions["angry"], duration = 4)
                                        move_on = True
                                else:
                                    print("❌ You don't have enough energy for that")
                            case 4: ## Ptooie
                                if player.pp >= 20:
                                    if player.target == "none":
                                        print("❌ You need to actually target someone.")
                                    else:
                                        player.pp -= 20
                                        print(f"> You huak a loogie at {player.target.name}, instantly befouling them with your vile disease!")
                                        player.target.apply_condition(conditions["poisoned"], duration = 6)
                                        move_on = True
                                else:
                                    print("❌ You don't have enough energy for that")
                            case 1: ## Power Stance
                                energy = random.randint(4, 11)
                                print(f"> You recover {energy} energy!")
                                player.pp = min(player.pp + energy, player.ppmax)
                                move_on = True
                            case 5: ## Headbutt
                                if player.pp >= 20:
                                    if player.target == "none":
                                        print("❌ You need to actually target someone.")
                                    else:
                                        player.pp -= 20
                                        dmg = random.randint(4, 7 + player.dmgbonus)
                                        print(f"> You bash your skull against {player.target.name}, dealing {dmg} damage!!!")
                                        player.target.hp -= dmg
                                        if random.randint(1,3) == 1:
                                            #print(f"> {player.target.name} is stunned!")
                                            player.target.apply_condition(conditions["stunned"], duration = 2 )
                                    
                                        move_on = True
                                else:
                                    print("❌ You don't have enough energy for that")
                            case _:
                                print("❌ That's not an ability")

                case "examine":
                    found = False;
                    for _item in player.inventory:
                        if  " ".join(action) == f"examine {_item.name.lower()}":
                            print(f"\n{_item.emojo} *{_item.name}*\n{_item.description}")
                            found = True
                            break
                    if not found:
                        print("❌ You can't look at something you don't have.")

                case "use":
                    for _item in player.inventory:
                        if  " ".join(action) == f"use {_item.name.lower()}":
                            _item.use(player.target, player, enemies)
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

        time.sleep(1)

    ##################### Enemy Turn   
    else:
        for enemy in enemies:
            
            # Ignore dead enemies
            if enemy.hp <= 0:
                continue

            # Ignore stunned enemies
            if enemy.has_condition("stunned"):
                if enemy.active_conditions["stunned"] > 1:
                    print(f"> 💫 {enemy.name} is stunned..")
                    time.sleep(1.0)
            # The actual turn
            else:
                if random.randint(1, 100) <= enemy.hitratio:
                    dmg = random.randint(1, 3 + enemy.dmgbonus)
                    print(f"> {enemy.name} smacks you for {dmg} damage!!!")
                    player.hp -= dmg
                    time.sleep(1.0)
                else:
                    print(f"> {enemy.name} takes a swing... but misses!")
                    time.sleep(1.0)
            
    # End fight if conditions are met
    #if check_for_outcome():
    #    break;
    
    # Reset
    round_num += 1
    player_turn = not player_turn

### Game over message
match(fight_state):
    case "fleed":
        print("You ran away! Coward.")
    case "playerlose":
        print("You died. L")
    case "playerwin":
        print(f"You win! Good job.")
    case _:
        print("Someone won. Dunno who.")

import time
import random
from enemies import dead_enemies
from conditions import conditions
from player import player

## Would be supplied from the location variables in an actual in-game fight
#enemies = [Enemy_Rat("Scruffy rat"), Enemy_Rat("Dirty rat"), Enemy_Rat("Long rat"), Enemy_Rat("Slimy rat"), Enemy_Rat("Normal rat"), Enemy_Rat("Furry rat")]

### See if the fight is over
def check_for_outcome(enemies):
    outcome = "ongoing"
    
    if player.hp <= 0:
        outcome = "LOSE"
    if len(enemies) == 0:
        outcome = "WIN"
    return outcome

### 
def begin_battle(enemies, loot): 

    fight_state = "ongoing"
    player_turn = True

    print("\n\033[31;1m             ⚔️ BEGIN FIGHT! ⚔️\033[0m\033[38;5:231m\n\n(Type 'actions' for a list of commands)")

    ##### Game Loop
    while fight_state == "ongoing":
        
        #### Player Turn
        if player_turn:
            
            # Update the state of each enemy
            for enemy in enemies:
                enemy.rebuff(player)

            # Update player conditions
            player.rebuff(True)

            # Remove all of the dead enemies from the enemy list
            for corpse in dead_enemies:
                enemies.remove(corpse)
            dead_enemies.clear()

            # Check to see if fight is over
            fight_state = check_for_outcome(enemies)
            if fight_state != "ongoing":
                break;

            # Reset the player target both at the beginning of the battle, and when the target dies
            if player.target == None:
                player.target = enemies[0]

            # Print all the turn info
            print("---------------------------------------------------")
            print(f"    Player {player.emojo} {player.hp}/{player.hpmax} ⚡{player.pp}/{player.ppmax}")
            print("                 · · · · vs. · · · ·")
            for enemy in enemies:
                print(f"            {enemy.emojo} {enemy.hp}/{enemy.hpmax}          {enemy.name}")
            
            # Only move on when the player actually makes a valid action
            move_on = False
            
            while not move_on:
                action = input(f"\n:: what do you want to do? (⯐ {player.target.name if player.target != None else "None"}): ").lower().split(' ')

                # Do things depending on the player input
                match action[0]:
                    # Helpful message of available actions
                    case "actions":
                        print("""
    **Actions**
    - attack                : attacks the targeted creature
    - block                 : blocks from incoming attacks
    - target [enemy name]   : changes which creature is targeted
    - abilities             : gives a list of your abilities
    - ability [ability #]   : uses the given ability
    - inventory             : gives a list of the items in your inventory
    - examine [item name]   : tells you about the given item
    - use [item name]       : uses the given item""")  
                    # Change the targeted enemy
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
                    # Attack the targeted enemy
                    case "attack":
                        if player.target == "none":
                            print("❌ You need to actually target someone.")
                        else:
                            dmg = random.randint(1, max(3 + player.dmgbonus, 1) )
                            print(f"> You beat {player.target.name} for {dmg} damage!!!")
                            player.target.hp -= dmg
                            move_on = True
                    # Defend
                    case "block":
                        print("> 🛡️  You enter a defensive stance!")
                        player.apply_condition(conditions["blocking"], 1)
                        move_on = True
                    # Print items in the player's inventory that can be used in battle
                    case "inventory":
                        if len(player.inventory) > 0:
                            for i in range(len(player.inventory)):
                                print(f"{i+1} | {player.inventory[i].emojo} {player.inventory[i].name}")
                        else:
                            print("Your inventory is empty :(")
                    # list off special moves
                    case "abilities":
                        print("""
1 | Power Stance    : ⚡ 0 Recover a small amount of energy
2 | Bulldog Beating : ⚡ 15 A strong attack that's likely to miss
3 | Ptooie          : ⚡ 15 you spit on your opponent, poisoning them for five rounds
4 | Headbutt        : ⚡ 20 A strong attack with a chance to stun for one round""")
                    ##################### Actually use one of the special moves
                    case "ability":
                        if len(action) <= 1:
                            print("❌ You need to specify which ability you want to use")
                        elif not action[1].isnumeric():
                            print("❌ You need to provide a number")
                        else:
                            match (int(action[1])):
                                case 2: ## Bulldog Beating
                                    if player.pp >= 15:
                                        if player.target == "none":
                                            print("❌ You need to actually target someone.")
                                        else:
                                            player.pp -= 15
                                            if random.randint(1, 5) > 2:
                                                dmg = random.randint(5, 15 + player.dmgbonus)
                                                print(f"> You hurl yourself toward {player.target.name}, dealing {dmg} damage!!!")
                                                player.target.hp -= dmg
                                            else:
                                                print(f"> You hurl yourself toward {player.target.name}, but miss!")
                                            
                                            move_on = True
                                    else:
                                        print("❌ You don't have enough energy for that")
                            
                                case 3: ## Ptooie
                                    if player.pp >= 15:
                                        if player.target == "none":
                                            print("❌ You need to actually target someone.")
                                        else:
                                            player.pp -= 15
                                            print(f"> You huak a loogie at {player.target.name}, instantly befouling them with your vile disease!")
                                            player.target.apply_condition(conditions["poisoned"], duration = 6)
                                            move_on = True
                                    else:
                                        print("❌ You don't have enough energy for that")
                                case 1: ## Power Stance
                                    energy = random.randint(10, 20)
                                    print(f"> You recover {energy} energy!")
                                    player.pp = min(player.pp + energy, max(player.pp, player.ppmax))
                                    move_on = True
                                case 4: ## Headbutt
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
                    # Describe an item the player has
                    case "examine":
                        found = False;
                        for _item in player.inventory:
                            if  " ".join(action) == f"examine {_item.name.lower()}":
                                print(f"\n{_item.emojo} *{_item.name}*\n{_item.description}")
                                found = True
                                break
                        if not found:
                            print("❌ You can't look at something you don't have.")
                    # Use an item the player has
                    case "use":
                        for _item in player.inventory:
                            if  " ".join(action) == f"use {_item.name.lower()}":
                                _item.use(player.target, player, enemies)
                                player.inventory.remove(_item)
                                move_on = True
                                break
                        if not move_on:
                            print("❌ That's not an item you have bud.")
                    # Run like a little coward
                    #case "flee":
                    #    move_on = True
                    #    fight_state = "fleed"
        
                    case _:
                        print("❌ That's not a command. Try harder.")

            time.sleep(1)

        ##################### Enemy Turn   
        else:
            for enemy in enemies:
                0
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
                    enemy.make_turn(player, enemies)
        
        # Reset
        player_turn = not player_turn

    # Return player to max stats
    player.reset()

    # Determine outcome
    if fight_state == "WIN":
        print("\n\x1b[33;1m    VICTORY! \033[0m\033[38;5:231m\n")
        print("----- LOOT -----")
        for item in loot:
            # for money
            if isinstance(item, int):
                print(f" - {item} coins")
                player.money += item
            # for items
            else:
                print(f" - {item.emojo} {item.name}")
                player.inventory.append(item)
    else:
        print("\n\033[31;1m    YOU WERE DEFEATED \033[0m\033[38;5:231m\n")
    
    return fight_state
import random

player_hp = 10
enemy_hp = 10

player_turn = True

fight_state = "ongoing"

### Items
class Item:
    def __init__(self):
        self.name = "undefined"
        self.itemid = -1

class itm_bomb(Item):
    def __init__(self):
        self.name = "Bomb"
        self.itemid = 0
    
    def use(self):
        global enemy_hp
        dmg = random.randint(3, 5)
        print(f"> 💥💥💥 You blow up the spooky guy for {dmg} damage!!! 💥💥💥")
        enemy_hp -= dmg

class itm_hpotion(Item):
    def __init__(self):
        self.name = "Pill"
        self.itemid = 1
    
    def use(self):
        global player_hp
        heal = random.randint(4, 6)
        player_hp = min(player_hp + heal, 10)
        print(f"> You have healed to ❤ {player_hp} hp!")

inventory = [itm_bomb(), itm_hpotion()]

##### game loop
while fight_state == "ongoing":
    
    if player_turn:
        print("-----------------------------------------------")
        print(f"player  ❤️ {player_hp}/{10}            💜 {enemy_hp}/{10} Spooky Guy")
        print("-----------------------------------------------")
        print("""
        Actions:
        attack
        inventory
        use [item]
        flee
        """)
        
        move_on = False
        
        while not move_on:
            action = input(":: what do you want to do? ").lower().split(' ')
            
            match action[0]:
                case "attack":
                    dmg = random.randint(1, 3)
                    print(f"> You beat the spooky guy for {dmg} damage!!!")
                    enemy_hp -= dmg
                    move_on = True
                case "inventory":
                    for i in range(len(inventory)):
                        print(f"{i+1} | {inventory[i].name}")
                case "use":
                    for _item in inventory:
                        if _item.name.lower() == action[1]:
                            _item.use()
                            move_on = True
                            break;
                    if not move_on:
                        print("That's not an item you have bud.")
                case "flee":
                    move_on = True
                    fight_state = "fleed"
                case _:
                    print("That's not a command. Try harder.")
        
    else:
        dmg = random.randint(1, 3)
        print(f"> The spooky guy smacks you for {dmg} damage!!!")
        player_hp -= dmg
        
    # End fight if conditions are met
    if player_hp <= 0:
        fight_state = "playerlose";
    if enemy_hp <= 0:
        fight_state = "playerwin";
    
    #
    player_turn = not player_turn
        
print("Battle over. Dunno who won.")

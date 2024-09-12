import re
import json
from fight_test import begin_battle
from items import item_map
from player import player
from shop import open_shop

class DialogueTree:
    def __init__(self, text_file=None, location=None):
        self.text = text_file or {}
        self.current_node = self.text
        self.location = location

    @staticmethod
    def load_from_file(file_path, location):
        with open(file_path, 'r') as file:
            dialogue_data = json.load(file)

        return DialogueTree(dialogue_data, location)

    def find_node(self, msgid):
        # Stack to hold nodes to visit, initialized with the root node
        stack = [self.text]

        # Iterate while there are nodes to visit
        while stack:
            _node = stack.pop()
            # Check if the current node has the desired msgid
            if _node.get("msgid") == msgid:
                return _node

            # If the current node has options, add them to the stack for further exploration
            if "options" in _node:
                for option in _node["options"].values():
                    stack.append(option)

        # If no node with the given msgid is found, return None
        return None

    def process_text(self, input_text):
        tag_regex = r'\[.*?\]'

        # Step 1: Find all matches of the command tags
        matches = re.findall(tag_regex, input_text)

        if matches:
            # Step 2: Remove all command tags from the input text
            input_text = re.sub(tag_regex, '', input_text).strip()
            print(f"\033[38;5;231m{input_text}\n")

            # Step 3: Process each command found in the text
            for match in matches:
                _match = match.replace('[', '').replace(']', '')
                args = _match.split(' ')
                match (args[0]):
                    
                    case "check": # Set a variable to true in the location
                        self.location.checks[args[1]] = True

                    case "uncheck": # Set a variable to true in the location
                        self.location.checks[args[1]] = False

                    case "switch": # Go to either one message or another depending on the state of a location variable
                        # args [1] is the variable to check
                        # args [2] and [3] are the messages to warp to if its either true or false respectively
                        if self.location.checks[args[1]]:
                            self.current_node = self.find_node(int(args[2]))
                        else:
                            self.current_node = self.find_node(int(args[3]))
                        # Display the new text
                        return True

                    case "item": # give an item to the player
                        item = item_map[args[1]]()
                        player.inventory.append(item)
                        if len(args) > 2:
                            print(f" - You got {item.emojo} \033[38;5;226m{item.name}\033[38;5;231m!")
                        else:
                            print(f" - You got {item.emojo} \033[38;5;226m{item.name}\033[38;5;231m!\n")

                    case "remove": # remove an item from the player's inventory
                        for i in range(len(player.inventory)):
                            if player.inventory[i].name is args[1]:
                                del player.inventory[i]

                    case "warp": # go to a message with a given msg id
                        self.current_node = self.find_node(int(args[1]))
                        if len(args) > 2:
                            if args[2] == "reprint":
                                return True

                    case "unlock": # unlock a message
                        self.find_node(int(args[1]))["locked"] = False

                    case "lock": # lock either a specified message, or the current message
                        if len(args) == 1:
                            self.current_node["locked"] = True
                        else:
                            self.find_node(int(args[1]))["locked"] = True
                    case "fight": # begin a fight
                        fight_struct = self.location.fights[args[1]]
                        input("\x1b[31;1mPress ENTER to continue...\x1b[0m\033[38;5;231m")
                        self.current_node = self.current_node["options"][begin_battle(fight_struct["enemies"], fight_struct["loot"])]
                        return True

                    case "shop":
                        open_shop(args[1])
                        
                    case "load": # Enter a different dialogue tree
                        self.location.active_tree = self.location.dialogue_trees[args[1]]
                        self.location.active_tree.current_node = self.location.active_tree.find_node(int(args[2]))

                    case "riddle": # Riddle for the stupid rat king guy
                        won = False
                        riddle_num = 1
                        while not won:
                            done = False
                            answer = ""
                            lives = 3
                            match(riddle_num):
                                case 1:
                                    answer = "a pot of boiling water"
                                case 2:
                                    print("Here is the next riddle: What's kinda smelly and also it hurt your head just a few seconds ago?")
                                    answer = "A rotten canteloupe that fell on your head and exploded everywhere"
                                case 3:
                                    print("Who is ugly and big and stupid and fat?")
                                    answer = "me"
                                case 4:
                                    won = True
                                    done = True


                            while not done:
                                guess = input("\033[38;5;228mWhat is your guess?: ")
                                if guess.lower() == answer.lower():
                                    print("\033[38;5;231m")
                                    self.current_node = self.current_node["options"]["WIN?"]
                                    done = True
                                else:
                                    print("\033[38;5;231m")
                                    # Check if answer was 'you' for specifically the third riddle
                                    if guess.lower() == "you":
                                        print("Rat King: Wha-!? HOW DARE YOU!!! I'M GONNA KILL YOU SIDJ SDOIUH SD")
                                        self.current_node = self.current_node["options"]["MURDER"]
                                        done = True
                                        won = True

                                    # regular bad guess
                                    lives -= 1
                                    match(lives):
                                        case 2:
                                            print("Rat King: Nuh uh! BAD GUESS! You have two more guesses.")
                                        case 1:
                                            print("Rat King: O! OO! WRONG AGAIN! One more guess buddy. ")
                                        case 0:
                                            print(f"Rat King: OH! SO CLOSE! Obviously, the answer was {"you" if answer == "me" else answer}. Anyways, onto the next riddle!")
                                            riddle_num += 1
                                            done = True

                        if riddle_num == 4:
                            self.current_node = self.current_node["options"]["FAIL"]
                                



                    case _: # Broken
                        print(f"Unknown command: {args[0]}")
        else:
            print(f"\033[38;5;231m{input_text}\n")
        
        return False
    

    def run(self):

        # In case process text needs to be ran multiple times due to warping or loading or whatnot
        resetty = True

        # Process and print the text of the current node
        while resetty:
            if self.current_node["text"] != "":
                resetty = self.process_text(self.current_node["text"])
            else:
                resetty = False

        # If the current node has options, display them and get user input
        if "options" in self.current_node:
            
            available_options = [
                option for option in self.current_node["options"].keys()
                if not (
                    # Check if "locked" is present and it's True
                    self.current_node["options"][option].get("locked", False) == True 
                    # Check if "locked" is a string, and the corresponding value in "checks" is True
                    or isinstance(self.current_node["options"][option].get("locked"), str)
                    and not self.location.checks.get(self.current_node["options"][option]["locked"], True)
                )
            ]

            # List options, make options that have been explored already grey instead of white.
            for index, option in enumerate(available_options):
                color_code = "\033[38;5;231m"
                if "found" in self.current_node["options"][option]:
                    if self.current_node["options"][option]["found"]:
                        color_code = "\033[38;5;232m"
                print(f"{color_code}{index + 1}) {option}\033[38;5;231m")
            print("")

            valid_choice = False
            while not valid_choice:
                restricted = True
                if "unrestricted" in self.current_node:
                    restricted = False
                    choice = input("\033[38;5;219mWhat do you do?: ")
                else:
                    choice = input("\033[38;5;228mChoose an option: ")

                print("")
                #print("\033[38;5;231m")

                # Validate the user's choice and navigate to the selected option
                try:
                    choice_index = int(choice) - 1
                    if 0 <= choice_index < len(available_options):
                        valid_choice = True
                        selected_option = available_options[choice_index]
                        self.current_node = self.current_node["options"][selected_option]
                        self.current_node["found"] = True
                    else:
                        valid_choice = False
                        print("That's not an option. Try again.")
                except ValueError:
                    valid_choice = False
                    if restricted:
                        print("You need to enter a number. Try again")
                    else:
                        args = choice.split(' ')
                        match( args[0] ):
                            case "help":
                                print("""   Commands:
    - help                  : displays this command
    - inventory             : gives a list of the items in your inventory
    - use [item_name]       : uses an item in your inventory 
    - examine [item name]   : tells you about the given item
                                """)
                            case "inventory":
                                print(f"\033[38;5;231mYou have: ¢{player.money}\n")
                                if len(player.inventory) > 0:
                                    for i in range(len(player.inventory)):
                                        if not player.inventory[i].usable_in_battle:
                                            print(f"\033[38;5;231m{i+1} | {player.inventory[i].emojo} {player.inventory[i].name}")
                                        else:
                                            print(f"{i+1} | {player.inventory[i].emojo} \033[38;5;235m{player.inventory[i].name}\033[38;5;231m")
                                else:
                                    print("Your inventory is empty :(")
                            case "examine":
                                found = False
                                for _item in player.inventory:
                                    if  choice.lower() == f"examine {_item.name.lower()}":
                                        print(f"\033[38;5;231m\n{_item.emojo} *{_item.name}*\n{_item.description}")
                                        found = True
                                        break
                                if not found:
                                    print("\033[38;5;231m❌ You can't look at something you don't have.")
                            case "use":
                                move_on = False
                                for _item in player.inventory:
                                    if  choice == f"use {_item.name.lower()}":
                                        if _item.usable_in_battle == False:
                                            _item.use(None, player, None)
                                            player.inventory.remove(_item)
                                            move_on = True
                                            break
                                        else:
                                            print("\033[38;5;231m❌ You can only use that item when in battle.")
                                            move_on = True
                                            break
                                if not move_on:
                                    print("\033[38;5;231m❌ That's not an item you have bud.")
        else:
            return

path = "text adventure project/dialogue/"
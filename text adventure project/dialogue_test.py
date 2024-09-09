import re
import json
from fight_test import begin_battle
from items import item_map
from player import player

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
                        print(f" - You got {item.emojo} \033[38;5;226m{item.name}\033[38;5;231m!\n")

                    case "warp": # go to a message with a given msg id
                        self.current_node = self.find_node(int(args[1]))

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
                        
                    case "load": # Enter a different dialogue tree
                        self.location.active_tree = self.location.dialogue_trees[args[1]]

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


            for index, option in enumerate(available_options):
                color_code = "\033[38;5;231m"
                if "found" in self.current_node["options"][option]:
                    if self.current_node["options"][option]["found"]:
                        color_code = "\033[38;5;232m"
                print(f"{color_code}{index + 1}) {option}\033[38;5;231m")
            print("")

            valid_choice = False
            while not valid_choice:
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
                    print("You need to enter a number. Try again")
        else:
            #self.location.active_tree = None
            return

path = "text adventure project/dialogue/"
#test_dialogue = DialogueTree.load_from_file(path + 'dg_mrtran_001.json')
#print("\033[38;5;231m")
#test_dialogue.run()
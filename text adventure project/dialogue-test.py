import re
import json

class DialogueTree:
    def __init__(self, text_file=None):
        self.text = text_file or {}
        self.current_node = self.text

    @staticmethod
    def load_from_file(file_path):
        with open(file_path, 'r') as file:
            dialogue_data = json.load(file)

        return DialogueTree(dialogue_data)

    def find_node(self, msgid):
        # Stack to hold nodes to visit, initialized with the root node
        stack = [self.text]

        # Iterate while there are nodes to visit
        while stack:
            current_node = stack.pop()

            # Check if the current node has the desired msgid
            if current_node.get("msgid") == msgid:
                return current_node

            # If the current node has options, add them to the stack for further exploration
            if "options" in current_node:
                for option in current_node["options"].values():
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
            print(f"\033[38;5;231m{input_text}")

            # Step 3: Process each command found in the text
            for match in matches:
                _match = match.replace('[', '').replace(']', '')
                args = _match.split(' ')
                match (args[0]):
                    
                    case "warp":
                        self.current_node = self.find_node(int(args[1]))
                        print("...")

                    case "unlock":
                        self.find_node(int(args[1]))["locked"] = False

                    case "lock":
                        self.find_node(int(args[1]))["locked"] = True
                        
                    case _:
                        print(f"Unknown command: {args[0]}")
        else:
            print(f"\033[38;5;231m{input_text}")

    def run(self):
        while True:
            # Process and print the text of the current node
            self.process_text(self.current_node["text"])

            # If the current node has options, display them and get user input
            if "options" in self.current_node:
                
                available_options = [
                    option for option in self.current_node["options"].keys()
                    if not self.current_node["options"][option].get("locked", False)
                ]

                for index, option in enumerate(available_options):
                    color_code = "\033[38;5;231m"
                    if "found" in self.current_node["options"][option]:
                        if self.current_node["options"][option]["found"]:
                            color_code = "\u001b[38;5;232m"
                    print(f"{color_code}{index + 1}) {option}\033[38;5;231m")
                print("")

                valid_choice = False
                while not valid_choice:
                    choice = input("\033[38;5;228mChoose an option: ")
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
                print("zoobers")
                break

        # Print the leaf node or ending node text
        #self.process_text(self.current_node["text"])

path = "text adventure project/dialogue/"
test_dialogue = DialogueTree.load_from_file(path + 'dialogue_002.json')
print("\033[38;5;231m")
test_dialogue.run()
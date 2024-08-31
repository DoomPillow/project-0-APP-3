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

    def find_warphole(self, msgid):
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

        matches = re.search(tag_regex, input_text)

        if matches:

            # remove the tag from the text
            input_text = re.sub(tag_regex, '', input_text)

            print(input_text)

            # Do something with the given command
            _match = matches.group(0).replace('[','').replace(']','')
            args = _match.split(',')
            match (args[0]):
                case "give pill":
                    print("\n> You were given a 💊 pill!\n")
                case "warp":
                    self.current_node = self.find_warphole(int(args[1]))
                    self.process_text(self.current_node["text"])
                    print("...")
                case _:
                    print("nada")
        else:
            print(input_text)
    
    #return input_text

    def run(self):
        while True:
            # Process and print the text of the current node
            self.process_text(self.current_node["text"])

            # If the current node has options, display them and get user input
            if "options" in self.current_node:
                options = list(self.current_node["options"].keys())
                for index, option in enumerate(options):
                    print(f"{"\u001b[33m" if (self.current_node["options"][option]["found"]) else "\033[0m"}{index + 1}) {option}\033[0m")

                choice = input("\nChoose an option: ")

                # Validate the user's choice and navigate to the selected option
                try:
                    choice_index = int(choice) - 1
                    if 0 <= choice_index < len(options):
                        selected_option = options[choice_index]
                        self.current_node = self.current_node["options"][selected_option]
                        self.current_node["found"] = True
                    else:
                        print("Invalid option. Please try again.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
            else:
                # If there are no options, check if the game should end or continue due to a warp
                if "msgid" in self.current_node:
                    continue  # Continue the loop to reprocess the new node after warping
                else:
                    break

        # Print the leaf node or ending node text
        #self.process_text(self.current_node["text"])


test_dialogue = DialogueTree.load_from_file('text adventure project/trees/dialogue_001.json')
test_dialogue.run()
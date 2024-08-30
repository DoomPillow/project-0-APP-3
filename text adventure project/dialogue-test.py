import re
import yaml

class DialogueTree:
    def __init__(self, text_file=None):
        self.text = text_file or {}
        self.current_node = self.text

    @classmethod
    def from_raw_data(cls, raw_data):
        text = raw_data.get('text')
        warpid = raw_data.get('warpid')
        
        # Store the whole raw data structure under 'raw_data'
        return cls(raw_data)

    @staticmethod
    def load_from_file(file_path):
        with open(file_path, 'r') as f:
            file_content = f.read()
        
        raw_data = yaml.safe_load(file_content)
        return DialogueTree.from_raw_data(raw_data)

    def process_text(self, input_text):
        tag_regex = r'\[.*?\]'

        matches = re.search(tag_regex, input_text)

        if matches:

            # remove the tag from the text
            input_text = re.sub(tag_regex, '', input_text)

            print(input_text)

            # Do something with the given command
            match (matches.group(0).replace('[','').replace(']','')):
                case "give pill":
                    print("\n> You were given a 💊 pill!\n")
                case _:
                    print("nada")
        else:
            print(input_text)
    
    #return input_text

    def run(self):
        while "options" in self.current_node:

            self.process_text(self.current_node["text"])

            # Display the available options
            options = list(self.current_node["options"].keys())
            for index, option in enumerate(options):
                print(f"{index + 1}) {option}")


            choice = input("\nChoose an option: ")

            # Make sure the input doesn't explode everything
            try:
                choice_index = int(choice) - 1 
                if 0 <= choice_index < len(options):
                    selected_option = options[choice_index]
                    self.current_node = self.current_node["options"][selected_option] # Move to the next node in the tree
                else:
                    print("Invalid option. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        # Print the leaf node
        self.process_text(self.current_node["text"])


# Load tran_dialogue.txt into a dialogue tree
test_dialogue = DialogueTree.load_from_file('text adventure project/dialogue_001.txt')
print(test_dialogue.text)
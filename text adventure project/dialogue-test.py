import re

dialogue_tree = {
    "text" : """
You walk down the long stretch of hallway through the administration building. You make it about halfway through when suddenly, you spot him.
The school bully, smugly strutting down the hallway as if nothing in this world is capable of stopping him. With no one else in the hallway,
he locks his eyes on you. Sweat starts running down your face as you worry about what he could possibly be plotting. He trots up to you, and
begins speaking.

Mr Chen: Hey! Gimme all your money!!

You don't know how the 60 year old substitute teacher became the school bully, but I suppose no one's life path is set in stone. 
""",
    "options":
        {
            "Nuh-Uh!": {
                "text": """Mr Chen: Wha- what!? HOW COULD YOU DISOBEY ME!? I SAID GIVE ME YOUR MONEY!!

Mr. Chen becomes increasingly flustered as he tries to spit his words out. Clearly no one has ever tried to talk back to him
before."""
            },
            "Yeah, sure": {
                "text": """Mr Chen: Thank you.

He quickly turns around and begins waddling off. He was satisfied pretty easily.""",
                "options": {
                    "Just kidding! (murder him from behind)": {
                        "text": """You two finger tap him in the back of the skull, instantly exploding his head. 
His brains go everywhere, including your mouth. His brains are so succulent and delicious that you fall asleep.

> THE END"""
                    },
                    "Leave": {
                        "text": """Even though you did technically just get robbed, you feel a sense of gratitude, as if you
just donated to charity. Maybe those thirty cents you gave away will be put to a better cause.

> THE END His face contorts into a grin, revealing two rows of teeth made of pure gold, adorned with diamonds (as if them 
being pure gold wasn't enough)."""
                    },
                }
            }
        }                
}

current_node = dialogue_tree  # Start at the root of the dialogue tree

def process_text(input_text):
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

while "options" in current_node:

    process_text(current_node["text"])

    # Display the available options
    options = list(current_node["options"].keys())
    for index, option in enumerate(options):
        print(f"{index + 1}) {option}")


    choice = input("\nChoose an option: ")

    # Make sure the input doesn't explode everything
    try:
        choice_index = int(choice) - 1 
        if 0 <= choice_index < len(options):
            selected_option = options[choice_index]
            current_node = current_node["options"][selected_option] # Move to the next node in the tree
        else:
            print("Invalid option. Please try again.")
    except ValueError:
        print("Invalid input. Please enter a number.")

# Print the leaf node
process_text(current_node["text"])
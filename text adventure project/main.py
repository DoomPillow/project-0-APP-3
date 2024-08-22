
running = True;

help_text = """
help : displays a list of commands
quit : quits the game
travel [location] : travels to a given location
"""

class Location:
    def __init__(self, name, discovered):
        self.name = name;
        self.discovered = discovered;

map_areas = [Location("beach", True), Location("Caves", True), Location("Grotto", False)];

# game loop
while running:

    command = input(": ").lower().partition(' ');

    match (command[0]):
        case "quit": # End the game
            running = False;
        case "travel":
            print("oinga boinga")
        case "help":
            print(help_text)
        case "map":
            for i in map_areas:
                if i.discovered:
                    print(i.name);
        case _:
            print(f"\'{command[0]}\' is not a  recognized command");

print("Game Over")

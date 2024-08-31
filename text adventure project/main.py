"""
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

map_areas = [Location("Quad", True), Location("Admin Building", True), Location("CAMAD", False)];

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
            print(f"'{command[0]}' is not a  recognized command");

print("Game Over")
"""

import time
player_name = "You"

print("""
   	 ____    	 _ _ 	 _              ____              	  _   
  	|  _ \  	| | |   | |            / __ \            	 | |  
  	| |_) |_   _| | | __| | ___   __ _| |  | |_   _  ___  ___| |_
  	|  _ <| | | | | |/ _` |/ _ \ / _` | |  | | | | |/ _ \/ __| __|
  	| |_) | |_| | | | (_| | (_) | (_| | |__| | |_| |  __/\__ \ |_
  	|____/ \__,_|_|_|\__,_|\___/ \__, |\___\_\\__,_|\___||___/\__|
                                  __/ |                      	 
                                 |___/                       	 
                              	 
          	.---== A PHS Adventure of Epic Proportions ==---.
           	 
""")

input("Press ENTER to begin")

print("""

August 19th, 2024. 30 minutes before school starts. You walk down the gloomy corridors of the
PHS Administration building. You give passing glances to the glass cases haphazardly dotting
the hallway, filled with old trophies collecting dust, and framed photos of people that probably
never existed. You stop before a large green door, next to it a faux-brass plaque labeled
“counselors office.” Both the staff present during registration day, and Aeries, have failed to give
you your class schedule, but it’s impossible that the counselors don’t have your schedule for you
by now. It’s literally the first day of school, after all. You pull open the door and walk into the
musty room to see one of the admin behind a shiny wooden desk, guarding an array of doors
leading to the various offices of THE COUNSELORS. She turns to you with a tired expression
completely devoid of emotion.
""")

input("Press Enter to continue...")

print("\nAdmin: What do you need?")
print("\nYou: I’m here to get my schedule.")
print("\nAdmin: Which counselor do you have?")
print("\nYou: Mr. Tran")
print("\nAdmin: First door to your right. ")
print("""
You’re not even fully sure that she actually processed what you said, as it felt like her words came
from more of a matter of instinct, but nevertheless, you follow her directions to a wooden door at the
corner of the room. You grab the handle, and creak open the door. You peer inside to see, oddly enough,
what appears to be no one at the desk. Assuming he’ll arrive soon enough, you sit down on a
large leather couch pushed up against the wall of the room. The cushions of the couch squeak
as they compress, scaring the ever-loving daylights out of Mr. Tran, who jolts up out of his
fully-inclined chair with a gasp. He quickly tears off a nightcap and sleeping mask and throws a
little blue blanket to the ground.
""")

print("Mr. Tran: Sorry! Sorry. I wasn’t expecting someone to come to my office so early. Please, give me a moment…")

input("Press Enter to continue...")

print("Mr. Tran lifts up a finger, and spends almost a full minute taking deep breaths to recover from the jumpscare you gave him.")
time.sleep(5.5)
print(".")
time.sleep(1.3)
print(".")
time.sleep(1.3)
print("..")
time.sleep(1.4)
print("...")
time.sleep(3)


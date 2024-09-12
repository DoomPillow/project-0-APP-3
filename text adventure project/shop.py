import json
from items import item_map
from player import player

def list_shop(data):
    # Extract the item names
    item_list = list(data.keys())

    # Print the items
    for item in item_list:
        print(f" ¢{data[item]["price"]}{" " * (4 - len(str(data[item]["price"])))}|  {item_map[data[item]["id"]]().emojo} {item}")
    print(f"\nYou currently have: ¢{player.money}")

def open_shop(filename):

    print("type `help` for commands")

    # get json data
    with open(f'text adventure project/shop data/{filename}.json', 'r') as file:
        data = json.load(file)

    # initial shop list
    list_shop(data)

    shopping = True
    while shopping:
        choice = input("\n\033[38;5;228mChoose an option: ")
        print("\033[38;5;231m")
        args = choice.split(' ')
        match( args[0] ):
            case "help":
                print("""        - help                      : displays this command
        - list                      : lists the available items to buy
        - buy [amount] [item_name]  : purchases an amount of the given item
        - examine [item_name]       : asks the shopkeep about the given item
        - leave                     : exits the shop
                """)
            case "list":
                list_shop(data)
            case "buy":
                
                try:
                    # Make sure they dont try to purchase 0 or negative items
                    if int(args[1]) < 1:
                        print("❌ You actually suck fr")
                        continue
                    # get the item dict
                    _item = data[" ".join(args[2:]).lower()]
                    # make sure they aren't buying more than what is available
                    if "one-time" in _item and int(args[1]) != 1:
                        print("❌ Only one of these is available for purchase")
                        continue
                    # This runs if the player actually did things correctly
                    # Check if the player has enough money to buy things
                    price = int(args[1]) * _item["price"]
                    if player.money >= price:
                        print(f" > You purchased {args[1]} {item_map[_item["id"]]().emojo} {" ".join(args[2:]).lower()}{"s" if int(args[1]) > 1 else ""}!")
                        player.money -= price
                        # add the items to the inventory
                        for i in range(int(args[1])):
                            player.inventory.append(item_map[_item["id"]]())
                    else:
                        print("❌ You can't afford that")

                except:
                    if len(args) < 2:
                        print("❌ You suck")
                    elif not args[1].isnumeric():
                        print("❌ You need to provide an amount")
                    else:
                        print("❌ You spelled something wrong")
            case "examine":
                
                try:
                    print(f"\033[38;5;231m{data[" ".join(args[1:]).lower()]["desc"]}")
                except:
                    if len(args) < 2:
                        print("❌ You suck")
                    else:
                        print("❌ You spelled something wrong")
            case "leave":
                shopping = False
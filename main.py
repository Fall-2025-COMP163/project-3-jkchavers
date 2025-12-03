"""
COMP 163 - Project 3: Quest Chronicles
Main Game Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This is the main game file that ties all modules together.
Demonstrates module integration and complete game flow.
"""

# Import all our custom modules
import character_manager
import inventory_system
import quest_handler
import combat_system
import game_data
from custom_exceptions import *

# ============================================================================
# GAME STATE
# ============================================================================

# Global variables for game data
current_character = None
all_quests = {}
all_items = {}
game_running = False

# ============================================================================
# MAIN MENU
# ============================================================================

def main_menu():
    """
    Display main menu and get player choice
    
    Options:
    1. New Game
    2. Load Game
    3. Exit
    
    Returns: Integer choice (1-3)
    """
    # TODO: Implement main menu display
    # Show options
    # Get user input
    # Validate input (1-3)
    # Return choice
    print("Options: 1. New Game\n2. Load Game\n3. Exit")
    choice = int(input())
    return choice

def new_game():
    """
    Start a new game
    
    Prompts for:
    - Character name
    - Character class
    
    Creates character and starts game loop
    """
    global current_character
    name = ""

    # TODO: Implement new game creation
    # Get character name from user
    # Get character class from user
    # Try to create character with character_manager.create_character()
    # Handle InvalidCharacterClassError
    # Save character
    # Start game loop
    try:

        print("\n=== New Game ===")

        while True:
            name = input("Enter the name of your character")
            if name != "" and name is not None:
                break
        while True:
            character_class = input("Enter your character class")
            if character_class != "" and character_class is not None:
                break

        character_manager.create_character(name, character_class) #creates character
        game_loop()# starts game loop
    except InvalidCharacterClassError:
        print("Invalid character class")



def load_game():
    """
    Load an existing saved game
    
    Shows list of saved characters
    Prompts user to select one
    """
    global current_character
    
    # TODO: Implement game loading
    # Get list of saved characters
    # Display them to user
    # Get user choice
    # Try to load character with character_manager.load_character()
    # Handle CharacterNotFoundError and SaveFileCorruptedError
    # Start game loop
    print("\n=== Load Game ===")

    try:
        saves = character_manager.list_saves()
    except Exception as e:
        print(f"Error accessing save files: {e}")
        return

    if not saves:
        print("No saved games found.\n")
        return

    # Display saved characters
    print("\nSaved Characters:")
    for i, save in enumerate(saves, start=1):
        print(f" {i}. {save}")

    # User selection
    while True:
        choice = input("\nSelect a character by number: ").strip()
        if not choice.isdigit():
            print("Please enter a valid number.")
            continue

        choice = int(choice)
        if 1 <= choice <= len(saves):
            selected_save = saves[choice - 1]
            break
        else:
            print("Invalid selection. Try again.")

    # Attempt to load the character
    try:
        current_character = character_manager.load_character(selected_save)
        print(f"\nLoaded character: {current_character['name']}")
    except CharacterNotFoundError:
        print(f"Save file '{selected_save}' not found or deleted.")
        return
    except SaveFileCorruptedError:
        print(f"Save file '{selected_save}' is corrupted and cannot be loaded.")
        return

    # Start game
    print("\nStarting game...\n")
    game_loop()


# ============================================================================
# GAME LOOP
# ============================================================================

def game_loop():
    """
    Main game loop - shows game menu and processes actions
    """
    global game_running, current_character
    
    game_running = True
    
    # TODO: Implement game loop
    # While game_running:
    #   Display game menu
    #   Get player choice
    #   Execute chosen action
    #   Save game after each action
    while game_running:
       game_menu()


def game_menu():
    """
    Display game menu and get player choice
    
    Options:
    1. View Character Stats
    2. View Inventory
    3. Quest Menu
    4. Explore (Find Battles)
    5. Shop
    6. Save and Quit
    
    Returns: Integer choice (1-6)
    """
    print("\n=== Game Menu ===")
    print("1. View Character Stats")
    print("2. View Inventory")
    print("3. Quest Menu")
    print("4. Explore (Find Battles)")
    print("5. Shop")
    print("6. Save and Quit")

    choice = input("Choose an action: ").strip()
    if choice == 1:
        view_character_stats()
    if choice == 2:
        view_inventory()
    if choice == 3:
        quest_menu()
    if choice == 4:
        explore()
    if choice == 5:
        shop()
    if choice == 6:
        save_game()
    # TODO: Implement game menu


# ============================================================================
# GAME ACTIONS
# ============================================================================

def view_character_stats():
    """Display character information"""
    global current_character
    
    # TODO: Implement stats display
    # Show: name, class, level, health, stats, gold, etc.
    # Use character_manager functions
    # Show quest progress using quest_handler

    print("=== Character Stats ===")
    print(f"Name: {current_character["name"]}")
    print(f"Name: {current_character["level"]}")
    print(f"Name: {current_character["health"]}")
    print(f"Name: {current_character["gold"]}")
    print(f"Quest progress: {quest_handler.display_character_quest_progress(current_character, current_character)}")


def view_inventory():
    """Display and manage inventory"""
    global current_character, all_items
    
    # TODO: Implement inventory menu
    # Show current inventory
    # Options: Use item, Equip weapon/armor, Drop item
    # Handle exceptions from inventory_system
    print("=== Inventory ===")
    print(current_character["inventory"])

    pass

def quest_menu():
    """Quest management menu"""
    global current_character, all_quests
    
    # TODO: Implement quest menu
    # Show:
    #   1. View Active Quests
    #   2. View Available Quests
    #   3. View Completed Quests
    #   4. Accept Quest
    #   5. Abandon Quest
    #   6. Complete Quest (for testing)
    #   7. Back
    # Handle exceptions from quest_handler
    print("=== Quest Menu ===")
    print("1. View Active Quests")
    print("2. View Available Quests")
    print("3. View Completed Quests")
    print("4. Accept Quest")
    print("5. Abandon Quest")
    print("6. Complete Quest (for testing)")
    print("7. Back")


def explore():
    """Find and fight random enemies"""
    global current_character
    
    # TODO: Implement exploration
    # Generate random enemy based on character level
    # Start combat with combat_system.SimpleBattle
    # Handle combat results (XP, gold, death)
    # Handle exceptions
    print("\nYou venture into the unknown...")

    try:
        # Generate enemy based on character level
        level = current_character["level"]
        enemy = combat_system.get_random_enemy_for_level(level)

        print(f"\nA wild {enemy['name']} appears! (Lv {enemy['level']})")

        # Start combat
        battle = combat_system.SimpleBattle(current_character, enemy)
        result = battle.start_battle()  # must return a dict like {"outcome": "win", "xp": 50, "gold": 10}

        # Handle combat results
        if result["outcome"] == "win":
            xp_gain = result["xp_reward"]
            gold_gain = result["gold_reward"]

            print(f"\nYou defeated the {enemy['name']}!")
            print(f"You gained {xp_gain} XP and {gold_gain} gold.")

            # Apply rewards
            current_character["gold"] = character_manager.add_gold(current_character, gold_gain)
            character_manager.gain_experience(current_character, xp_gain)
        elif result["outcome"] == "lose":
            print("\nYou were defeated...")
            current_character["health"] = 0
            game_running = False
            return

        else:
            print("Unexpected battle result:", result)

    except Exception as e:
        print(f"An error occurred during exploration: {e}")
    pass

def shop():
    """Shop menu for buying/selling items"""
    global current_character, all_items
    
    # TODO: Implement shop
    # Show available items for purchase
    # Show current gold
    # Options: Buy item, Sell item, Back
    # Handle exceptions from inventory_system
    all_items = {
        "Potion": {"price": 10},
        "Hi-Potion": {"price": 25},
        "Sword": {"price": 50},
    }
    #Used ChatGPT to create a starter point for the shop
    if current_character is None:
        print("No character loaded.")
        return

    while True:
        print("\n=== Shop ===")
        print(f"Gold: {current_character['gold']}")
        print("1. Buy Items")
        print("2. Sell Items")
        print("3. Back to Game Menu")

        choice = input("Choose an option: ").strip()

        # ----------------------------
        # BUY MENU
        # ----------------------------
        if choice == "1":
            print("\n--- Items for Sale ---")
            item_list = list(all_items.keys())

            for i, item in enumerate(item_list, start=1):
                price = all_items[item]["price"]
                print(f"{i}. {item} - {price} gold")

            print(f"{len(item_list) + 1}. Back")

            buy_choice = input("\nSelect item to buy: ").strip()

            if not buy_choice.isdigit():
                print("Invalid choice.")
                continue

            buy_choice = int(buy_choice)

            if buy_choice == len(item_list) + 1:
                continue  # back to shop menu

            if not (1 <= buy_choice <= len(item_list)):
                print("Invalid choice.")
                continue

            item = item_list[buy_choice - 1]
            price = all_items[item]["price"]

            # Check gold
            if current_character["gold"] < price:
                print("You don't have enough gold.")
                continue

            # Attempt purchase
            try:
                inventory_system.add_item_to_inventory(current_character, item)
                current_character["gold"] -= price
                print(f"Purchased {item} for {price} gold!")
            except Exception as e:
                print(f"Error purchasing item: {e}")

        # ----------------------------
        # SELL MENU
        # ----------------------------
        elif choice == "2":
            inventory = current_character["inventory"]

            if not inventory:
                print("You have nothing to sell.")
                continue

            print("\n--- Your Inventory ---")
            for i, item in enumerate(inventory, start=1):
                # Sell price = half buy price (override if needed)
                if item in all_items:
                    sell_price = all_items[item]["price"] // 2
                else:
                    sell_price = 1  # fallback

                print(f"{i}. {item} - Sell for {sell_price} gold")

            print(f"{len(inventory) + 1}. Back")

            sell_choice = input("\nSelect item to sell: ").strip()

            if not sell_choice.isdigit():
                print("Invalid choice.")
                continue

            sell_choice = int(sell_choice)

            if sell_choice == len(inventory) + 1:
                continue

            if not (1 <= sell_choice <= len(inventory)):
                print("Invalid choice.")
                continue

            item = inventory[sell_choice - 1]

            # Determine sell price
            if item in all_items:
                sell_price = all_items[item]["price"] // 2
            else:
                sell_price = 1

            try:
                inventory_system.remove_item(current_character, item)
                current_character["gold"] += sell_price
                print(f"Sold {item} for {sell_price} gold!")
            except Exception as e:
                print(f"Error selling item: {e}")

        # ----------------------------
        # EXIT SHOP
        # ----------------------------
        elif choice == "3":
            print("Leaving shop...")
            return

        else:
            print("Invalid choice, try again.")
    pass

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def save_game():
    """Save current game state"""
    global current_character
    
    # TODO: Implement save
    # Use character_manager.save_character()
    # Handle any file I/O exceptions
    try:
        character_manager.save_character(current_character)

    except (IOError, OSError) as e:
        print(f"File error while buying item: {e}")


def load_game_data():
    """Load all quest and item data from files"""
    global all_quests, all_items
    
    # TODO: Implement data loading
    # Try to load quests with game_data.load_quests()
    # Try to load items with game_data.load_items()
    # Handle MissingDataFileError, InvalidDataFormatError
    # If files missing, create defaults with game_data.create_default_data_files()
    try:
        game_data.load_quests()
        game_data.load_items()

    except (MissingDataFileError, InvalidDataFormatError) as e:
        print(f"File error while loading game data: {e}")
        game_data.create_default_data_files()


def handle_character_death():
    """Handle character death"""
    global current_character, game_running
    
    # TODO: Implement death handling
    # Display death message
    # Offer: Revive (costs gold) or Quit
    # If revive: use character_manager.revive_character()
    # If quit: set game_running = False
    print("\n=== YOU HAVE DIED ===")
    print(f"{current_character["name"]} has fallen in battle.")

    # Revive cost (can adjust or scale with level)
    revive_cost = 50

    while True:
        print("\nWhat would you like to do?")
        print(f"1. Revive for {revive_cost} gold")
        print("2. Quit to Main Menu")

        choice = input("Choose an option: ").strip()

        # -------------------------------------------------------
        # REVIVE OPTION
        # -------------------------------------------------------
        if choice == "1":
            if current_character.get("gold", 0) < revive_cost:
                print("You do not have enough gold to revive.")
                continue

            try:
                # Attempt revival
                character_manager.revive_character(current_character)
                current_character["gold"] -= revive_cost

                print("\nYou have been revived!")
                print(f"Gold remaining: {current_character['gold']}")

                # Character revived → resume game loop
                return

            except (IOError, OSError) as e:
                print(f"File error during revival: {e}")
                print("Revival failed due to file corruption or save problems.")

            except Exception as e:
                print(f"Unexpected error during revival: {e}")

            # If revive fails, do NOT let the game crash
            print("Revival attempt failed. You can try again or quit.")
            continue

        # -------------------------------------------------------
        # QUIT OPTION
        # -------------------------------------------------------
        elif choice == "2":
            print("\nReturning to main menu...")
            game_running = False
            return

        # -------------------------------------------------------
        # INVALID INPUT
        # -------------------------------------------------------
        else:
            print("Invalid choice. Try again.")


def display_welcome():
    """Display welcome message"""
    print("=" * 50)
    print("     QUEST CHRONICLES - A MODULAR RPG ADVENTURE")
    print("=" * 50)
    print("\nWelcome to Quest Chronicles!")
    print("Build your character, complete quests, and become a legend!")
    print()

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main game execution function"""
    
    # Display welcome message
    display_welcome()
    
    # Load game data
    try:
        load_game_data()
        print("Game data loaded successfully!")
    except MissingDataFileError:
        print("Creating default game data...")
        game_data.create_default_data_files()
        load_game_data()
    except InvalidDataFormatError as e:
        print(f"Error loading game data: {e}")
        print("Please check data files for errors.")
        return
    
    # Main menu loop
    while True:
        choice = main_menu()
        
        if choice == 1:
            new_game()
        elif choice == 2:
            load_game()
        elif choice == 3:
            print("\nThanks for playing Quest Chronicles!")
            break
        else:
            print("Invalid choice. Please select 1-3.")

if __name__ == "__main__":
    main()


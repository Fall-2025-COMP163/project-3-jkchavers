"""
COMP 163 - Project 3: Quest Chronicles
Character Manager Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This module handles character creation, loading, and saving.
"""

import os
from custom_exceptions import (
    InvalidCharacterClassError,
    CharacterNotFoundError,
    SaveFileCorruptedError,
    InvalidSaveDataError,
    CharacterDeadError
)

# ============================================================================
# CHARACTER MANAGEMENT FUNCTIONS
# ============================================================================

def create_character(name, character_class):
    """
    Create a new character with stats based on class
    
    Valid classes: Warrior, Mage, Rogue, Cleric


    
    Returns: Dictionary with character data including:
            - name, class, level, health, max_health, strength, magic
            - experience, gold, inventory, active_quests, completed_quests
    
    Raises: InvalidCharacterClassError if class is not valid
    """

    # TODO: Implement character creation
    # Validate character_class first
    # Example base stats:
    # Warrior: health=120, strength=15, magic=5
    # Mage: health=80, strength=8, magic=20
    # Rogue: health=90, strength=12, magic=10
    # Cleric: health=100, strength=10, magic=15
    
    # All characters start with:
    # - level=1, experience=0, gold=100
    # - inventory=[], active_quests=[], completed_quests=[]
    
    # Raise InvalidCharacterClassError if class not in valid list

    valid_classes = {
        "Warrior": {"health": 120, "strength": 15, "magic": 5},
        "Mage": {"health": 80, "strength": 8, "magic": 20},
        "Rogue": {"health": 90, "strength": 12, "magic": 10},
        "Cleric": {"health": 100, "strength": 10, "magic": 15},
    }

    if character_class not in valid_classes:
        raise InvalidCharacterClassError(f"Invalid class: {character_class}")

    base = valid_classes[character_class]

    # Return properly shaped, fully-populated character dictionary
    return {
        "name": name,
        "class": character_class,
        "level": 1,
        "health": base["health"],
        "max_health": base["health"],
        "strength": base["strength"],
        "magic": base["magic"],
        "experience": 0,
        "gold": 100,
        "inventory": [],
        "active_quests": [],
        "completed_quests": [],
    }


def save_character(character, save_directory="data/save_games"):
    """
    Save character to file
    
    Filename format: {character_name}_save.txt
    
    File format:
    NAME: character_name
    CLASS: class_name
    LEVEL: 1
    HEALTH: 120
    MAX_HEALTH: 120
    STRENGTH: 15
    MAGIC: 5
    EXPERIENCE: 0
    GOLD: 100
    INVENTORY: item1,item2,item3
    ACTIVE_QUESTS: quest1,quest2
    COMPLETED_QUESTS: quest1,quest2
    
    Returns: True if successful
    Raises: PermissionError, IOError (let them propagate or handle)
    """
    # TODO: Implement save functionality
    os.makedirs(save_directory, exist_ok=True)

    filename = f"{character['name']}_save.txt"
    save_path = os.path.join(save_directory, filename)

    try:
        with open(save_path, "w") as f:
            f.write(f"NAME: {character['name']}\n")
            f.write(f"CLASS: {character['class']}\n")
            f.write(f"LEVEL: {character['level']}\n")
            f.write(f"HEALTH: {character['health']}\n")
            f.write(f"MAX_HEALTH: {character['max_health']}\n")
            f.write(f"STRENGTH: {character['strength']}\n")
            f.write(f"MAGIC: {character['magic']}\n")
            f.write(f"EXPERIENCE: {character['experience']}\n")
            f.write(f"GOLD: {character['gold']}\n")

            # Lists as comma-separated strings
            f.write(f"INVENTORY: {','.join(character['inventory'])}\n")
            f.write(f"ACTIVE_QUESTS: {','.join(character['active_quests'])}\n")
            f.write(f"COMPLETED_QUESTS: {','.join(character['completed_quests'])}\n")

        return True
    except OSError as e:
        print(f"Error:{e}")

def load_character(character_name, save_directory="data/save_games"):
    """
    Load character from save file

    Args:
        character_name: Name of character to load
        save_directory: Directory containing save files

    Returns: Character dictionary
    Raises:
        CharacterNotFoundError if save file doesn't exist
        SaveFileCorruptedError if file exists but can't be read
        InvalidSaveDataError if data format is wrong
    """
    # TODO: Implement load functionality
    save_path = os.path.join(save_directory, f"{character_name}_save.txt")

    if not os.path.exists(save_path):
        raise CharacterNotFoundError(f"Save file for '{character_name}' not found")

    character = {}

    try:
        with open(save_path, "r") as f:
            lines = f.readlines()

        for line in lines:
            if ":" not in line:
                raise InvalidSaveDataError("Malformed save line")

            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()

            # Parse numbers
            if key in ["LEVEL", "HEALTH", "MAX_HEALTH", "STRENGTH",
                       "MAGIC", "EXPERIENCE", "GOLD"]:
                try:
                    character[key.lower()] = int(value)
                except ValueError:
                    raise InvalidSaveDataError(f"{key} must be integer")

            # Parse lists
            elif key in ["INVENTORY", "ACTIVE_QUESTS", "COMPLETED_QUESTS"]:
                character[key.lower()] = value.split(",") if value else []

            else:
                # Strings
                character[key.lower()] = value

        # Final validation
        validate_character_data(character)
        return character

    except OSError:
        raise SaveFileCorruptedError(f"Could not read file: {save_path}")

def list_saved_characters(save_directory="data/save_games"):
    """
    Get list of all saved character names
    
    Returns: List of character names (without _save.txt extension)
    """
    # TODO: Implement this function
    # Return empty list if directory doesn't exist
    # Extract character names from filenames

    try:
        save_files = []
        # Check if the path exists and is a directory
        if not os.path.exists(save_directory):
            raise FileNotFoundError(f"Path does not exist: {save_directory}")
        elif not os.path.isdir(save_directory):
            raise NotADirectoryError(f"Not a directory: {save_directory}")
        else:
            #Directory and path are valid so get file names and remove the last 3 characters of each file name string.
            save_files = os.listdir(save_directory)
            character_names = []
            for index, file in enumerate(save_files):
                file = str(file)
                file = file[:-4] #assuming the filename has a file extension of .txt
                character_names.append(file)
            return character_names


    except Exception as error:
        if isinstance(error, FileNotFoundError):
            print(f"Path does not exist: {save_directory}")
        elif isinstance(error, NotADirectoryError):
            print(f"Not a directory: {save_directory}")




def delete_character(character_name, save_directory="data/save_games"):
    """
    Delete a character's save file

    Returns: True if deleted successfully
    Raises: CharacterNotFoundError if character doesn't exist
    """
    character_file = character_name + ".txt"
    if os.path.exists(character_file):
        os.remove(character_file)
        print(f"{character_file[:-4]} deleted successfully.")
    else:
        print("The file does not exist.")
    # TODO: Implement character deletion
    # Verify file exists before attempting deletion


# ============================================================================
# CHARACTER OPERATIONS
# ============================================================================

def gain_experience(character, xp_amount):
    """
    Add experience to character and handle level ups

    Level up formula: level_up_xp = current_level * 100
    Example when leveling up:
    - Increase level by 1
    - Increase max_health by 10
    - Increase strength by 2
    - Increase magic by 2
    - Restore health to max_health
    
    Raises: CharacterDeadError if character health is 0
    """
    # TODO: Implement experience gain and leveling
    # Check if character is dead first
    # Add experience
    # Check for level up (can level up multiple times)
    # Update stats on level up

    if character["health"] <= 0:
        raise CharacterDeadError
    else:
        while character["experience"] >= (character["level"] * 100): #keeps leveling up until character xp is less than character level * 100
                character["level"] += xp_amount
                character["health"] = character["max_health"] + 10
                character["strength"] = character["strength"] + 2
                character["magic"] = character["magic"] + 2



def add_gold(character, amount):
    """
    Add gold to character's inventory
    
    Args:
        character: Character dictionary
        amount: Amount of gold to add (can be negative for spending)
    
    Returns: New gold total
    Raises: ValueError if result would be negative
    """
    # TODO: Implement gold management
    # Check that result won't be negative
    # Update character's gold

    new_total = character["gold"] + amount
    if new_total < 0:
        raise ValueError("Gold cannot go negative.")

    character["gold"] = new_total
    return character["gold"]


def heal_character(character, amount):
    """
    Heal character by specified amount
    
    Health cannot exceed max_health
    
    Returns: Actual amount healed
    """
    # TODO: Implement healing
    # Calculate actual healing (don't exceed max_health)
    # Update character health
    character["health"] = min(character["health"] + amount, character["max_health"])
    pass

def is_character_dead(character):
    """
    Check if character's health is 0 or below
    
    Returns: True if dead, False if alive

    """
    # TODO: Implement death check
    if character["health"] <= 0:
        raise CharacterDeadError(f"{character['name']} is dead")


def revive_character(character):
    """
    Revive a dead character with 50% health
    
    Returns: True if revived
    """
    # TODO: Implement revival
    # Restore health to half of max_health
    character["health"] = character["max_health"] // 2


# ============================================================================
# VALIDATION
# ============================================================================

def validate_character_data(character):
    """
    Validate that character dictionary has all required fields
    
    Required fields: name, class, level, health, max_health, 
                    strength, magic, experience, gold, inventory,
                    active_quests, completed_quests
    
    Returns: True if valid
    Raises: InvalidSaveDataError if missing fields or invalid types
    """
    # TODO: Implement validation
    # Check all required keys exist
    # Check that numeric values are numbers
    # Check that lists are actually lists

    required_fields = {
        "name": str,
        "class": str,
        "level": int,
        "health": int,
        "max_health": int,
        "strength": int,
        "magic": int,
        "experience": int,
        "gold": int,
        "inventory": list,
        "active_quests": list,
        "completed_quests": list
        }

    if not isinstance(character, dict):# Check if dictionary type
        raise InvalidSaveDataError("Character data must be a dictionary.")

    # Check required keys and types
    for key, expected_type in required_fields.items():
        if key not in character:
            raise InvalidSaveDataError(f"Missing required field: '{key}'")

        if not isinstance(character[key], expected_type):
            raise InvalidSaveDataError(
                f"'{key}' must be of type {expected_type.__name__}"
            )
    return True

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== CHARACTER MANAGER TEST ===")
    
    # Test character creation
    # try:
    #     char = create_character("TestHero", "Warrior")
    #     print(f"Created: {char['name']} the {char['class']}")
    #     print(f"Stats: HP={char['health']}, STR={char['strength']}, MAG={char['magic']}")
    # except InvalidCharacterClassError as e:
    #     print(f"Invalid class: {e}")
    
    # Test saving
    # try:
    #     save_character(char)
    #     print("Character saved successfully")
    # except Exception as e:
    #     print(f"Save error: {e}")
    
    # Test loading
    # try:
    #     loaded = load_character("TestHero")
    #     print(f"Loaded: {loaded['name']}")
    # except CharacterNotFoundError:
    #     print("Character not found")
    # except SaveFileCorruptedError:
    #     print("Save file corrupted")


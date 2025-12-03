"""
COMP 163 - Project 3: Quest Chronicles
Game Data Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This module handles loading and validating game data from text files.
"""

import os
from custom_exceptions import (
    InvalidDataFormatError,
    MissingDataFileError,
    CorruptedDataError
)

# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

def load_quests(filename="data/quests.txt"):
    """
    Load quest data from file
    
    Expected format per quest (separated by blank lines):
    QUEST_ID: unique_quest_name
    TITLE: Quest Display Title
    DESCRIPTION: Quest description text
    REWARD_XP: 100
    REWARD_GOLD: 50
    REQUIRED_LEVEL: 1
    PREREQUISITE: previous_quest_id (or NONE)
    
    Returns: Dictionary of quests {quest_id: quest_data_dict}
    Raises: MissingDataFileError, InvalidDataFormatError, CorruptedDataError
    """
    # TODO: Implement this function
    # Must handle:
    # - FileNotFoundError → raise MissingDataFileError
    # - Invalid format → raise InvalidDataFormatError
    # - Corrupted/unreadable data → raise CorruptedDataError
    if not os.path.exists(filename):
        raise MissingDataFileError(f"Quest file not found: {filename}")

    try:
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read().strip()

        if not content:
            raise CorruptedDataError("Quest file is empty.")

        blocks = content.split("\n\n")  # quests separated by blank lines
        quest_dict = {}

        for block in blocks:
            lines = [line.strip() for line in block.split("\n") if line.strip()]
            quest = parse_quest_block(lines)
            validate_quest_data(quest)
            quest_dict[quest["quest_id"]] = quest

        return quest_dict
    except MissingDataFileError:
        print(f"Quest file not found: {filename}")
    except InvalidDataFormatError:
        print(f"Invalid data format")
    except CorruptedDataError:
        print("Quest data file is unreadable or corrupted.")


def load_items(filename="data/items.txt"):
    """
    Load item data from file
    
    Expected format per item (separated by blank lines):
    ITEM_ID: unique_item_name
    NAME: Item Display Name
    TYPE: weapon|armor|consumable
    EFFECT: stat_name:value (e.g., strength:5 or health:20)
    COST: 100
    DESCRIPTION: Item description
    
    Returns: Dictionary of items {item_id: item_data_dict}
    Raises: MissingDataFileError, InvalidDataFormatError, CorruptedDataError
    """
    # TODO: Implement this function
    # Must handle same exceptions as load_quests
    if not os.path.exists(filename):
        raise MissingDataFileError(f"Item file not found: {filename}")

    try:
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read().strip()

        if not content:
            raise CorruptedDataError("Item file is empty.")

        blocks = content.split("\n\n")
        item_dict = {}

        for block in blocks:
            lines = [line.strip() for line in block.split("\n") if line.strip()]
            item = parse_item_block(lines)
            validate_item_data(item)
            item_dict[item["item_id"]] = item

        return item_dict

    except MissingDataFileError:
        print(f"Item data not found: {filename}")
    except InvalidDataFormatError:
        print("Invalid data format")
    except CorruptedDataError:
        print("Item data file is unreadable or corrupted.")

def validate_quest_data(quest_dict):
    """
    Validate that quest dictionary has all required fields
    
    Required fields: quest_id, title, description, reward_xp, 
                    reward_gold, required_level, prerequisite
    
    Returns: True if valid
    Raises: InvalidDataFormatError if missing required fields
    """
    # TODO: Implement validation
    # Check that all required keys exist
    # Check that numeric values are actually numbers
    required = [
        "quest_id",
        "title",
        "description",
        "reward_xp",
        "reward_gold",
        "required_level",
        "prerequisite",
    ]

    for field in required:
        if field not in quest_dict:
            raise InvalidDataFormatError(f"Quest missing required field: {field}")

    # Check numeric fields
    if not isinstance(quest_dict["reward_xp"], int):
        raise InvalidDataFormatError("REWARD_XP must be an integer.")
    if not isinstance(quest_dict["reward_gold"], int):
        raise InvalidDataFormatError("REWARD_GOLD must be an integer.")
    if not isinstance(quest_dict["required_level"], int):
        raise InvalidDataFormatError("REQUIRED_LEVEL must be an integer.")

    return True


def validate_item_data(item_dict):
    """
    Validate that item dictionary has all required fields
    
    Required fields: item_id, name, type, effect, cost, description
    Valid types: weapon, armor, consumable
    
    Returns: True if valid
    Raises: InvalidDataFormatError if missing required fields or invalid type
    """
    # TODO: Implement validation
    required = ["item_id", "name", "type", "effect", "cost", "description"]

    for field in required:
        if field not in item_dict:
            raise InvalidDataFormatError(f"Item missing required field: {field}")

    # Validate type
    if item_dict["type"] not in ("weapon", "armor", "consumable"):
        raise InvalidDataFormatError(f"Invalid item TYPE: {item['type']}")

    # Validate cost
    if not isinstance(item_dict["cost"], int):
        raise InvalidDataFormatError("COST must be an integer.")

    # effect must contain "stat:value"
    if ":" not in item_dict["effect"]:
        raise InvalidDataFormatError("EFFECT must be in format 'stat:value'.")

    return True

def create_default_data_files():
    """
    Create default data files if they don't exist
    This helps with initial setup and testing
    """
    # TODO: Implement this function
    # Create data/ directory if it doesn't exist
    # Create default quests.txt and items.txt files
    # Handle any file permission errors appropriately
    os.makedirs("data", exist_ok=True)

    # Default quest file
    default_quests = """\
    QUEST_ID: quest_intro
    TITLE: Hi Sunbro
    DESCRIPTION: Begin your adventure by speaking to the shaman of the sun.
    REWARD_XP: 50
    REWARD_GOLD: 10
    REQUIRED_LEVEL: 1
    PREREQUISITE: NONE

    QUEST_ID: quest_infestation
    TITLE: Cockroach army
    DESCRIPTION: Defeat the army of cockroaches, and you will be one step closer to your destiny
    REWARD_XP: 100
    REWARD_GOLD: 25
    REQUIRED_LEVEL: 1
    PREREQUISITE: quest_intro
    """

    # Default items
    default_items = """\
    ITEM_ID: small_potion
    NAME: Small Health Potion
    TYPE: consumable
    EFFECT: health:20
    COST: 15
    DESCRIPTION: Restores a small amount of health.

    ITEM_ID: iron_sword
    NAME: Iron Sword
    TYPE: weapon
    EFFECT: strength:3
    COST: 60
    DESCRIPTION: A basic iron sword.

    ITEM_ID: leather_armor
    NAME: Leather Armor
    TYPE: armor
    EFFECT: max_health:10
    COST: 40
    DESCRIPTION: Light protective armor.
    """

    try:
        if not os.path.exists("data/quests.txt"):
            with open("data/quests.txt", "w", encoding="utf-8") as f:
                f.write(default_quests)

        if not os.path.exists("data/items.txt"):
            with open("data/items.txt", "w", encoding="utf-8") as f:
                f.write(default_items)

    except PermissionError:
        print("Cannot write default data files — permission denied.")


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_quest_block(lines):
    """
    Parse a block of lines into a quest dictionary
    
    Args:
        lines: List of strings representing one quest
    
    Returns: Dictionary with quest data
    Raises: InvalidDataFormatError if parsing fails
    """
    # TODO: Implement parsing logic
    # Split each line on ": " to get key-value pairs
    # Convert numeric strings to integers
    # Handle parsing errors gracefully
    quest = {}

    try:
        for line in lines:
            if ": " not in line:
                raise InvalidDataFormatError(f"Invalid line: {line}")

            key, value = line.split(": ", 1)
            key = key.strip().lower()
            value = value.strip()

            if key == "quest_id":
                quest["quest_id"] = value
            elif key == "title":
                quest["title"] = value
            elif key == "description":
                quest["description"] = value
            elif key == "reward_xp":
                quest["reward_xp"] = int(value)
            elif key == "reward_gold":
                quest["reward_gold"] = int(value)
            elif key == "required_level":
                quest["required_level"] = int(value)
            elif key == "prerequisite":
                quest["prerequisite"] = None if value == "NONE" else value
            else:
                raise InvalidDataFormatError(f"Unknown quest field: {key}")

        return quest

    except InvalidDataFormatError:
        print("Quest numeric field must be an integer.")

def parse_item_block(lines):
    """
    Parse a block of lines into an item dictionary
    
    Args:
        lines: List of strings representing one item
    
    Returns: Dictionary with item data
    Raises: InvalidDataFormatError if parsing fails
    """
    # TODO: Implement parsing logic
    item = {}

    try:
        for line in lines:
            if ": " not in line:
                raise InvalidDataFormatError(f"Invalid line: {line}")

            key, value = line.split(": ", 1)
            key = key.strip().lower()
            value = value.strip()

            if key == "item_id":
                item["item_id"] = value
            elif key == "name":
                item["name"] = value
            elif key == "type":
                item["type"] = value
            elif key == "effect":
                item["effect"] = value
            elif key == "cost":
                item["cost"] = int(value)
            elif key == "description":
                item["description"] = value
            else:
                raise InvalidDataFormatError(f"Unknown item field: {key}")

        return item

    except ValueError:
        raise InvalidDataFormatError("Item COST must be an integer.")

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== GAME DATA MODULE TEST ===")
    
    # Test creating default files
    # create_default_data_files()
    
    # Test loading quests
    # try:
    #     quests = load_quests()
    #     print(f"Loaded {len(quests)} quests")
    # except MissingDataFileError:
    #     print("Quest file not found")
    # except InvalidDataFormatError as e:
    #     print(f"Invalid quest format: {e}")
    
    # Test loading items
    # try:
    #     items = load_items()
    #     print(f"Loaded {len(items)} items")
    # except MissingDataFileError:
    #     print("Item file not found")
    # except InvalidDataFormatError as e:
    #     print(f"Invalid item format: {e}")


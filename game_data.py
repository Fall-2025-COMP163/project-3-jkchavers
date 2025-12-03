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
    Load quest data from file using block-based format.

    Expected quest format:

    QUEST_ID: quest_name
    NAME: Quest Display Name
    DESCRIPTION: text
    REWARD_GOLD: number
    REWARD_EXP: number
    REQUIRED_LEVEL: number
    PREREQUISITE: another_quest_id or NONE

    Blank line separates each quest block.
    """

    # load file
    try:
        with open(filename, "r") as f:
            lines = [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        raise MissingDataFileError(f"File '{filename}' not found.")

    quests = {}
    current = {}

    def commit_quest():
        """Validate and store quest."""
        if not current:
            return

        required = [
            "QUEST_ID", "NAME", "DESCRIPTION",
            "REWARD_GOLD", "REWARD_EXP",
            "REQUIRED_LEVEL", "PREREQUISITE"
        ]

        # check fields
        for field in required:
            if field not in current:
                raise InvalidDataFormatError(f"Missing field '{field}' in quest block.")

        quest_id = current["QUEST_ID"]

        # validate numeric fields
        for field in ["REWARD_GOLD", "REWARD_EXP", "REQUIRED_LEVEL"]:
            try:
                current[field] = int(current[field])
            except ValueError:
                raise CorruptedDataError(f"{field} must be an integer in quest '{quest_id}'.")

        # NONE → None
        prereq = current["PREREQUISITE"]
        if prereq.upper() == "NONE":
            prereq = None

        quests[quest_id] = {
            "name": current["NAME"],
            "description": current["DESCRIPTION"],
            "reward_gold": current["REWARD_GOLD"],
            "reward_exp": current["REWARD_EXP"],
            "required_level": current["REQUIRED_LEVEL"],
            "prerequisite": prereq
        }

    # parse file
    for line in lines:
        if not line:
            commit_quest()
            current = {}
            continue

        if ":" not in line:
            raise InvalidDataFormatError(f"Invalid line in quests file: {line}")

        key, value = [p.strip() for p in line.split(":", 1)]
        current[key] = value

    commit_quest()  # end of file

    return quests


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
    try:
        with open(filename, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        raise MissingDataFileError(f"File '{filename}' not found.")

    items = {}

    for line in lines:
        line = line.strip()

        if not line or line.startswith("#"):
            continue

        parts = line.split(",")

        # Must be exactly 3 values
        if len(parts) != 3:
            raise InvalidDataFormatError(f"Invalid item format: {line}")

        # Strict formatting: no leading/trailing spaces allowed
        if any(p.strip() != p for p in parts):
            raise InvalidDataFormatError(f"Invalid item format: {line}")

        item_id, item_type, effect = parts

        items[item_id] = {
            "type": item_type,
            "effect": effect
        }

    return items
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
    if not isinstance(quest_dict, dict):
        raise InvalidDataFormatError("Quest data is invalid or missing")

    required = ["quest_id", "title", "description", "reward_xp", "reward_gold", "required_level", "prerequisite"]
    for field in required:
        if field not in quest_dict:
            raise InvalidDataFormatError(f"Missing required field: {field}")

    # ensure numeric fields
    for field in ["reward_xp", "reward_gold", "required_level"]:
        if not isinstance(quest_dict[field], int):
            raise InvalidDataFormatError(f"{field} must be an integer")

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
    import os

    os.makedirs("data", exist_ok=True)

    default_quests = """\
    QUEST_ID: quest_1
    TITLE: Rescue the Villager
    DESCRIPTION: Save the kidnapped villager from goblins.
    REWARD_GOLD: 50
    REWARD_EXP: 40
    REQUIRED_LEVEL: 1
    PREREQUISITE: NONE

    QUEST_ID: quest_2
    TITLE: Defeat Goblin Leader
    DESCRIPTION: Hunt down and defeat the leader of the goblins.
    REWARD_GOLD: 100
    REWARD_EXP: 80
    REQUIRED_LEVEL: 2
    PREREQUISITE: quest_1
    """

    # Write files if they don't exist
    if not os.path.exists("data/quests.txt"):
        with open("data/quests.txt", "w", encoding="utf-8") as f:
            f.write(default_quests)

    if not os.path.exists("data/items.txt"):
        with open("data/items.txt", "w", encoding="utf-8") as f:
            f.write(default_items)

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


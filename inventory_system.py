"""
COMP 163 - Project 3: Quest Chronicles
Inventory System Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This module handles inventory management, item usage, and equipment.
"""

from custom_exceptions import (
    InventoryFullError,
    ItemNotFoundError,
    InsufficientResourcesError,
    InvalidItemTypeError
)

# Maximum inventory size
MAX_INVENTORY_SIZE = 20

# ============================================================================
# INVENTORY MANAGEMENT
# ============================================================================

def add_item_to_inventory(character, item_id):
    """
    Add an item to character's inventory
    
    Args:
        character: Character dictionary
        item_id: Unique item identifier
    
    Returns: True if added successfully
    Raises: InventoryFullError if inventory is at max capacity
    """
    # TODO: Implement adding items
    # Check if inventory is full (>= MAX_INVENTORY_SIZE)
    # Add item_id to character['inventory'] list
    if len(character["inventory"]) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory is full.")

    character["inventory"].append(item_id)
    return True


def remove_item_from_inventory(character, item_id):
    """
    Remove an item from character's inventory
    
    Args:
        character: Character dictionary
        item_id: Item to remove
    
    Returns: True if removed successfully
    Raises: ItemNotFoundError if item not in inventory
    """
    # TODO: Implement item removal
    # Check if item exists in inventory
    # Remove item from list
    if item_id not in character["inventory"]:
        raise ItemNotFoundError(f"Item '{item_id}' not found in inventory.")

    character["inventory"].remove(item_id)  # removes first occurrence
    return True

    pass

def has_item(character, item_id):
    """
    Check if character has a specific item
    
    Returns: True if item in inventory, False otherwise
    """
    # TODO: Implement item check
    if item_id in character["inventory"]:
        return True
    else:
        return False


def count_item(character, item_id):
    """
    Count how many of a specific item the character has
    
    Returns: Integer count of item
    """
    # TODO: Implement item counting
    # Use list.count() method
    return character["inventory"].count(item_id)
    pass

def get_inventory_space_remaining(character):
    """
    Calculate how many more items can fit in inventory
    
    Returns: Integer representing available slots
    """
    # TODO: Implement space calculation
    current = len(character["inventory"])
    remaining = MAX_INVENTORY_SIZE - current
    if remaining < 0:
        remaining = 0
    return remaining


def clear_inventory(character):
    """
    Remove all items from inventory
    
    Returns: List of removed items
    """
    # TODO: Implement inventory clearing
    # Save current inventory before clearing
    # Clear character's inventory list
    old_inventory = character["inventory"]  # copy
    character["inventory"] = []
    return old_inventory


# ============================================================================
# ITEM USAGE
# ============================================================================

def use_item(character, item_id, item_data):
    """
    Use a consumable item from inventory
    
    Args:
        character: Character dictionary
        item_id: Item to use
        item_data: Item information dictionary from game_data
    
    Item types and effects:
    - consumable: Apply effect and remove from inventory
    - weapon/armor: Cannot be "used", only equipped
    
    Returns: String describing what happened
    Raises: 
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'consumable'
    """
    # TODO: Implement item usage
    # Check if character has the item
    # Check if item type is 'consumable'
    # Parse effect (format: "stat_name:value" e.g., "health:20")
    # Apply effect to character
    # Remove item from inventory
    if not has_item(character, item_id):
        raise ItemNotFoundError(f"Item '{item_id}' not found in inventory.")

    if item_data["type"] != "consumable":
        raise InvalidItemTypeError(f"Item '{item_id}' is not consumable.")

        # Effects may be a single string or a list; support either
    effect = item_data["effect"]
    if effect is None:
        # No effect: just remove item
        remove_item_from_inventory(character, item_id)
        return f"Used {item_data.get('name', item_id)} (no effect)."

    # parse effect (single "stat:value" string)
    stat_name, value = parse_item_effect(effect)
    apply_stat_effect(character, stat_name, value)

    # remove one instance from inventory
    remove_item_from_inventory(character, item_id)

    return f"Used {item_data.get('name', item_id)}: {stat_name} {'+' if value >= 0 else ''}{value}."


def equip_weapon(character, item_id, item_data):
    """
    Equip a weapon
    
    Args:
        character: Character dictionary
        item_id: Weapon to equip
        item_data: Item information dictionary
    
    Weapon effect format: "strength:5" (adds 5 to strength)
    
    If character already has weapon equipped:
    - Unequip current weapon (remove bonus)
    - Add old weapon back to inventory
    
    Returns: String describing equipment change
    Raises:
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'weapon'
    """
    # TODO: Implement weapon equipping
    # Check item exists and is type 'weapon'
    # Handle unequipping current weapon if exists
    # Parse effect and apply to character stats
    # Store equipped_weapon in character dictionary
    # Remove item from inventory
    if not has_item(character, item_id):
        raise ItemNotFoundError(f"Weapon '{item_id}' not found in inventory.")

    if item_data["type"] != "weapon":
        raise InvalidItemTypeError(f"Item '{item_id}' is not a weapon.")

        # If there's already an equipped weapon, unequip it first
    old_weapon = character["equipped_weapon"]
    if old_weapon is not None:
        # Unequip current weapon (remove bonuses) and return it to inventory
        unequipped = unequip_weapon(character)
        # If unequip_weapon returned None it means no slot available or no weapon; handle above
        # We assume unequip_weapon will add the item back to inventory.

    # Remove the new weapon from inventory and apply its effect
    remove_item_from_inventory(character, item_id)

    effect = item_data["effect"]
    if effect:
        stat_name, value = parse_item_effect(effect)
        apply_stat_effect(character, stat_name, value)

    character["equipped_weapon"] = item_id
    return f"Equipped weapon: {item_data[item_id]}"

def equip_armor(character, item_id, item_data):
    """
    Equip armor
    
    Args:
        character: Character dictionary
        item_id: Armor to equip
        item_data: Item information dictionary
    
    Armor effect format: "max_health:10" (adds 10 to max_health)
    
    If character already has armor equipped:
    - Unequip current armor (remove bonus)
    - Add old armor back to inventory
    
    Returns: String describing equipment change
    Raises:
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'armor'
    """
    # TODO: Implement armor equipping
    # Similar to equip_weapon but for armor
    if not has_item(character, item_id):
        raise ItemNotFoundError(f"Armor '{item_id}' not found in inventory.")

    if item_data["type"] != "armor":
        raise InvalidItemTypeError(f"Item '{item_id}' is not armor.")

        # Unequip current armor if present
    old_armor = character["equipped_armor"]
    if old_armor is not None:
        unequipped = unequip_armor(character)

    # Remove the armor from inventory and apply effect
    remove_item_from_inventory(character, item_id)
    effect = item_data.get("effect")
    if effect:
        stat_name, value = parse_item_effect(effect)
        apply_stat_effect(character, stat_name, value)

    character["equipped_armor"] = item_id
    return f"Equipped armor: {item_data[item_id]}"
    pass

def unequip_weapon(character):
    """
    Remove equipped weapon and return it to inventory
    
    Returns: Item ID that was unequipped, or None if no weapon equipped
    Raises: InventoryFullError if inventory is full
    """
    # TODO: Implement weapon unequipping
    # Check if weapon is equipped
    # Remove stat bonuses
    # Add weapon back to inventory
    # Clear equipped_weapon from character
    weapon_id = character["equipped_weapon"]
    if weapon_id is None:
        return None


    item_data_store = character["inventory"]
    if item_data_store and weapon_id in item_data_store:
        weapon_data = item_data_store[weapon_id]
        effect = weapon_data.get("effect")
        if effect:
            stat_name, value = parse_item_effect(effect)
            # Remove the bonus (apply negative)
            apply_stat_effect(character, stat_name, -value)

    # Try to add weapon back to inventory
    if get_inventory_space_remaining(character) <= 0:
        raise InventoryFullError("No space to unequip weapon.")

    add_item_to_inventory(character, weapon_id)
    character["equipped_weapon"] = None
    return weapon_id

def unequip_armor(character):
    """
    Remove equipped armor and return it to inventory
    
    Returns: Item ID that was unequipped, or None if no armor equipped
    Raises: InventoryFullError if inventory is full
    """
    # TODO: Implement armor unequipping
    armor_id = character["equipped_armor"]
    if armor_id is None:
        return None

    item_data_store = globals().get("item_data_dict", None)
    if item_data_store and armor_id in item_data_store:
        armor_data = item_data_store[armor_id]
        effect = armor_data.get("effect")
        if effect:
            stat_name, value = parse_item_effect(effect)
            apply_stat_effect(character, stat_name, -value)

    if get_inventory_space_remaining(character) <= 0:
        raise InventoryFullError("No space to unequip armor.")

    add_item_to_inventory(character, armor_id)
    character["equipped_armor"] = None
    return armor_id
    pass

# ============================================================================
# SHOP SYSTEM
# ============================================================================

def purchase_item(character, item_id, item_data):
    """
    Purchase an item from a shop
    
    Args:
        character: Character dictionary
        item_id: Item to purchase
        item_data: Item information with 'cost' field
    
    Returns: True if purchased successfully
    Raises:
        InsufficientResourcesError if not enough gold
        InventoryFullError if inventory is full
    """
    # TODO: Implement purchasing
    # Check if character has enough gold
    # Check if inventory has space
    # Subtract gold from character
    # Add item to inventory
    cost = item_data["cost"]

    if character["gold"] < cost:
        raise InsufficientResourcesError("Not enough gold to purchase item.")

    if get_inventory_space_remaining(character) <= 0:
        raise InventoryFullError("Not enough inventory space to purchase item.")

    # Subtract gold and add item
    character["gold"] = character["gold"] - cost
    add_item_to_inventory(character, item_id)
    return True

def sell_item(character, item_id, item_data):
    """
    Sell an item for half its purchase cost
    
    Args:
        character: Character dictionary
        item_id: Item to sell
        item_data: Item information with 'cost' field
    
    Returns: Amount of gold received
    Raises: ItemNotFoundError if item not in inventory
    """
    # TODO: Implement selling
    # Check if character has item
    # Calculate sell price (cost // 2)
    # Remove item from inventory
    # Add gold to character
    if not has_item(character, item_id):
        raise ItemNotFoundError(f"Item '{item_id}' not found in inventory.")

    cost = item_data.get("cost", 0)
    sell_price = cost // 2

    # Remove the item and add gold
    remove_item_from_inventory(character, item_id)
    character["gold"] = character.get("gold", 0) + sell_price
    return sell_price
    pass

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_item_effect(effect_string):
    """
    Parse item effect string into stat name and value
    
    Args:
        effect_string: String in format "stat_name:value"
    
    Returns: Tuple of (stat_name, value)
    Example: "health:20" → ("health", 20)
    """
    # TODO: Implement effect parsing
    # Split on ":"
    # Convert value to integer

    parts = effect_string.split(":", 1)
    stat_name = parts[0].strip()
    try:
        value = int(parts[1].strip())
    except Exception as e:
        print(f"Effect value must be an integer.\nError: {e}")

    return stat_name, value

def apply_stat_effect(character, stat_name, value):
    """
    Apply a stat modification to character
    
    Valid stats: health, max_health, strength, magic
    
    Note: health cannot exceed max_health
    """
    # TODO: Implement stat application
    # Add value to character[stat_name]
    # If stat is health, ensure it doesn't exceed max_health

    #ChatGPT did this entire portion
        # Ensure the stat exists
    if stat_name not in character:
        # initialize missing numeric stats to 0 except health/max_health
        if stat_name in ("health", "max_health"):
            character.setdefault(stat_name, 0)
        else:
            character.setdefault(stat_name, 0)

        # Apply max_health first if needed (so health clamp uses new max)
    if stat_name == "max_health":
        character["max_health"] = character.get("max_health", 0) + value
        # Ensure current health is not greater than new max
        if character.get("health", 0) > character["max_health"]:
            character["health"] = character["max_health"]
        return

    if stat_name == "health":
        character["health"] = character.get("health", 0) + value
        # Clamp
        max_hp = character.get("max_health", character.get("health", 0))
        if character["health"] > max_hp:
            character["health"] = max_hp
        if character["health"] < 0:
            character["health"] = 0
        return

        # For other stats just add/subtract
    character[stat_name] = character.get(stat_name, 0) + value
    return

def display_inventory(character, item_data_dict):
    """
    Display character's inventory in formatted way
    
    Args:
        character: Character dictionary
        item_data_dict: Dictionary of all item data
    
    Shows item names, types, and quantities
    """
    # TODO: Implement inventory display
    # Count items (some may appear multiple times)
    # Display with item names from item_data_dict
    inventory = character.get("inventory", [])
    if not inventory:
        print("\nInventory: (empty)\n")
        return

    # Build counts
    counts = {}
    for item in inventory:
        counts[item] = counts.get(item, 0) + 1

    print("\n=== Inventory ===")
    for item_id, qty in counts.items():
        item_info = item_data_dict.get(item_id, {})
        name = item_info.get("name", item_id)
        item_type = item_info.get("type", "unknown")
        print(f"{name} x{qty} ({item_type})")
    print(f"Slots used: {len(inventory)}/{MAX_INVENTORY_SIZE}\n")

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== INVENTORY SYSTEM TEST ===")
    
    # Test adding items
    # test_char = {'inventory': [], 'gold': 100, 'health': 80, 'max_health': 80}
    # 
    # try:
    #     add_item_to_inventory(test_char, "health_potion")
    #     print(f"Inventory: {test_char['inventory']}")
    # except InventoryFullError:
    #     print("Inventory is full!")
    
    # Test using items
    # test_item = {
    #     'item_id': 'health_potion',
    #     'type': 'consumable',
    #     'effect': 'health:20'
    # }
    # 
    # try:
    #     result = use_item(test_char, "health_potion", test_item)
    #     print(result)
    # except ItemNotFoundError:
    #     print("Item not found")


"""
COMP 163 - Project 3: Quest Chronicles
Quest Handler Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This module handles quest management, dependencies, and completion.
"""
import character_manager
from custom_exceptions import (
    QuestNotFoundError,
    QuestRequirementsNotMetError,
    QuestAlreadyCompletedError,
    QuestNotActiveError,
    InsufficientLevelError
)

# ============================================================================
# QUEST MANAGEMENT
# ============================================================================

def accept_quest(character, quest_id, quest_data_dict):
    """
    Accept a new quest
    
    Args:
        character: Character dictionary
        quest_id: Quest to accept
        quest_data_dict: Dictionary of all quest data
    
    Requirements to accept quest:
    - Character level >= quest required_level
    - Prerequisite quest completed (if any)
    - Quest not already completed
    - Quest not already active
    
    Returns: True if quest accepted
    Raises:
        QuestNotFoundError if quest_id not in quest_data_dict
        InsufficientLevelError if character level too low
        QuestRequirementsNotMetError if prerequisite not completed
        QuestAlreadyCompletedError if quest already done
    """
    # TODO: Implement quest acceptance
    # Check quest exists
    # Check level requirement
    # Check prerequisite (if not "NONE")
    # Check not already completed
    # Check not already active
    # Add to character['active_quests']

    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest '{quest_id}' does not exist")

    quest = quest_data_dict[quest_id]

    if character["level"] < quest["required_level"]:

        raise InsufficientLevelError

    prereq = quest["prerequisite"]
    if prereq != "NONE" and prereq not in character["completed_quests"]:
        raise QuestRequirementsNotMetError(f"Prerequisite quest '{prereq}' not completed")

    if quest_id in character["completed_quests"]:
        raise QuestAlreadyCompletedError(f"Quest '{quest_name}' already completed.")


    if quest_id in character["active_quests"]: # Check quest is not already active
        return False

    return True



def complete_quest(character, quest_id, quest_data_dict):
    """
    Complete an active quest and grant rewards
    
    Args:
        character: Character dictionary
        quest_id: Quest to complete
        quest_data_dict: Dictionary of all quest data
    
    Rewards:
    - Experience points (reward_xp)
    - Gold (reward_gold)
    
    Returns: Dictionary with reward information
    Raises:
        QuestNotFoundError if quest_id not in quest_data_dict
        QuestNotActiveError if quest not in active_quests
    """
    # TODO: Implement quest completion
    # Check quest exists
    # Check quest is active
    # Remove from active_quests
    # Add to completed_quests
    # Grant rewards (use character_manager.gain_experience and add_gold)
    # Return reward summary
    # 1. Check quest exists
    quest = quest_data_dict.get(quest_id)
    if quest is None:
        raise QuestNotFoundError()
        return None

    # 2. Check it is active
    if quest_id not in character["active_quests"]:
        raise QuestNotActiveError()


    # 3. Remove from active quests
    character["active_quests"].remove(quest_id)

    # 4. Add to completed
    character["completed_quests"].append(quest_id)

    # 5. Grant rewards
    reward_xp = quest["reward_xp"]
    reward_gold = quest["reward_gold"]


    character["experience"] = character_manager.gain_experience(character, reward_xp)
    character["gold"] = character_manager.add_gold(character, reward_gold)

    return {
        "xp": reward_xp,
        "gold": reward_gold,
        "quest_name": quest.get("name", quest_id)
    }


def abandon_quest(character, quest_id):
    """
    Remove a quest from active quests without completing it
    
    Returns: True if abandoned
    Raises: QuestNotActiveError if quest not active
    """
    # TODO: Implement quest abandonment

    try:
        if quest_id not in character["active_quests"]:
            return False
        elif quest_id in character["active_quests"]:
            character["active_quests"].remove(quest_id)
            return True
    except QuestNotActiveError:
        print("Quest not active")

def get_active_quests(character, quest_data_dict):
    """
    Get full data for all active quests
    
    Returns: List of quest dictionaries for active quests
    """
    # TODO: Implement active quest retrieval
    # Look up each quest_id in character['active_quests']
    # Return list of full quest data dictionaries
    quest_list = []
    for id in character["active_quests"]:
        quest_list.append(quest_data_dict[id])
    return quest_list

def get_completed_quests(character, quest_data_dict):
    """
    Get full data for all completed quests
    
    Returns: List of quest dictionaries for completed quests
    """
    # TODO: Implement completed quest retrieval
    quest_list = []
    for id in character["completed_quests"]:
        quest_list.append(quest_data_dict[id])
    return quest_list


def get_available_quests(character, quest_data_dict):
    """
    Get quests that character can currently accept
    
    Available = meets level req + prerequisite done + not completed + not active
    
    Returns: List of quest dictionaries
    """
    # TODO: Implement available quest search
    # Filter all quests by requirements
    available = []

    for id in quest_data_dict:
        quest = quest_data_dict[id]

        # 1. Level requirement
        if character["level"] < quest["required_level"]:
            continue

        # 2. Prerequisite check
        prereq = quest["prerequisite"]
        if prereq not in (None, "NONE"):
            if prereq not in character["completed_quests"]:
                continue

        if id in character["completed_quests"]:
            continue

        # 4. Already active?
        if id in character["active_quests"]:
            continue

        # If all conditions pass, add the quest dict
        available.append(quest)

    return available
    pass

# ============================================================================
# QUEST TRACKING
# ============================================================================

def is_quest_completed(character, quest_id):
    """
    Check if a specific quest has been completed
    
    Returns: True if completed, False otherwise
    """
    # TODO: Implement completion check
    if quest_id in character["completed_quests"]:
        return True
    else:
        return False


def is_quest_active(character, quest_id):
    """
    Check if a specific quest is currently active
    
    Returns: True if active, False otherwise
    """
    # TODO: Implement active check
    if quest_id in character["active_quests"]:
        return True
    else:
        return False


def can_accept_quest(character, quest_id, quest_data_dict):
    """
    Check if character meets all requirements to accept quest
    
    Returns: True if can accept, False otherwise
    Does NOT raise exceptions - just returns boolean
    """
    # TODO: Implement requirement checking
    # Check all requirements without raising exceptions

    if quest_id not in quest_data_dict:
        return False

    quest = quest_data_dict[quest_id]


    if character["level"] < quest["required_level"]:
        return False


    prereq = quest["prerequisite"]
    if prereq not in (None, "NONE"):
        if prereq not in character["completed_quests"]:
            return False


    if quest_id in character["completed_quests"]:
        return False


    if quest_id in character["active_quests"]:
        return False

    return True



def get_quest_prerequisite_chain(quest_id, quest_data_dict):
    """
    Get the full chain of prerequisites for a quest
    
    Returns: List of quest IDs in order [earliest_prereq, ..., quest_id]
    Example: If Quest C requires Quest B, which requires Quest A:
             Returns ["quest_a", "quest_b", "quest_c"]
    
    Raises: QuestNotFoundError if quest doesn't exist
    """
    # TODO: Implement prerequisite chain tracing
    # Follow prerequisite links backwards
    # Build list in reverse order
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError
        return []

    chain = []
    current = quest_id

    while True:
        if current not in quest_data_dict:
            # Invalid data breaks the chain safely
            break

        quest = quest_data_dict[current]
        chain.insert(0, current)

        prereq = quest["prerequisite"]

        # Stop if no prerequisite
        if prereq in (None, "NONE"):
            break

        # Continue to earlier prerequisite
        current = prereq

    return chain
    pass

# ============================================================================
# QUEST STATISTICS
# ============================================================================

def get_quest_completion_percentage(character, quest_data_dict):
    """
    Calculate what percentage of all quests have been completed
    
    Returns: Float between 0 and 100
    """
    # TODO: Implement percentage calculation
    # total_quests = len(quest_data_dict)
    # completed_quests = len(character['completed_quests'])
    # percentage = (completed / total) * 100
    total_quests = len(quest_data_dict)


    if total_quests == 0:
        return 0.0

    completed_count = len(character["completed_quests"])

    return (completed_count / total_quests) * 100
    pass

def get_total_quest_rewards_earned(character, quest_data_dict):
    """
    Calculate total XP and gold earned from completed quests
    
    Returns: Dictionary with 'total_xp' and 'total_gold'
    """
    # TODO: Implement reward calculation
    # Sum up reward_xp and reward_gold for all completed quests
    total_xp = 0
    total_gold = 0

    for quest_id in character["completed_quests"]:
        if quest_id in quest_data_dict:
            quest = quest_data_dict[quest_id]
            total_xp += quest["reward_xp"]
            total_gold += quest["reward_gold"]

    return {
        "total_xp": total_xp,
        "total_gold": total_gold
    }




def get_quests_by_level(quest_data_dict, min_level, max_level):
    """
    Get all quests within a level range
    
    Returns: List of quest dictionaries
    """
    # TODO: Implement level filtering
    results = []

    for quest_id in quest_data_dict:
        quest = quest_data_dict[quest_id]

        req = quest["required_level"]
        if req >= min_level and req <= max_level:
            results.append(quest)

    return results


# ============================================================================
# DISPLAY FUNCTIONS
# ============================================================================

def display_quest_info(quest_data):
    """
    Display formatted quest information
    
    Shows: Title, Description, Rewards, Requirements
    """
    # TODO: Implement quest display
    print(f"\n=== {quest_data['title']} ===")
    print(f"Description: {quest_data['description']}")
    print("\n==============================")
    print(f"Prerequisite: {quest_data['prerequisite']}")
    print(f"Reward XP: {quest_data['reward_xp']}")
    print(f"Reward Gold: {quest_data['reward_gold']}")
    print("==============================\n")


def display_quest_list(quest_list):
    """
    Display a list of quests in summary format
    
    Shows: Title, Required Level, Rewards
    """
    # TODO: Implement quest list display
    if len(quest_list) == 0:
        print("\n(No quests found.)\n")
        return

    print("\n=== Quest List ===")
    for quest in quest_list:
        print(f"- {quest['title']} (Lvl {quest['required_level']}) "
              f"XP: {quest['reward_xp']} | Gold: {quest['reward_gold']}")



def display_character_quest_progress(character, quest_data_dict):
    """
    Display character's quest statistics and progress
    
    Shows:
    - Active quests count
    - Completed quests count
    - Completion percentage
    - Total rewards earned
    """
    # TODO: Implement progress display
    active_count = len(character["active_quests"])
    completed_count = len(character["completed_quests"])
    percent = get_quest_completion_percentage(character, quest_data_dict)
    total_rewards = get_total_quest_rewards_earned(character, quest_data_dict)

    print("\n=== Quest Progress ===")
    print(f"Active Quests: {active_count}")
    print(f"Completed Quests: {completed_count}")
    print(f"Completion: {percent:.2f}%")
    print(f"Total XP Earned From Quests: {total_rewards['total_xp']}")
    print(f"Total Gold Earned From Quests: {total_rewards['total_gold']}\n")



# ============================================================================
# VALIDATION
# ============================================================================

def validate_quest_prerequisites(quest_data_dict):
    """
    Validate that all quest prerequisites exist
    
    Checks that every prerequisite (that's not "NONE") refers to a real quest
    
    Returns: True if all valid
    Raises: QuestNotFoundError if invalid prerequisite found
    """
    # TODO: Implement prerequisite validation
    # Check each quest's prerequisite
    # Ensure prerequisite exists in quest_data_dict
    try:
        for quest_id in quest_data_dict:
            quest = quest_data_dict[quest_id]
            prereq = quest["prerequisite"]

            if prereq not in (None, "NONE"):
                if prereq not in quest_data_dict:
                    raise QuestNotFoundError(f"Prerequisite '{prereq}' missing for quest '{quest_id}'")


        return True
    except QuestNotFoundError as error:
        if error == isinstance(QuestNotFoundError):
            print("Prerequisite not found.")



# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== QUEST HANDLER TEST ===")
    
    # Test data
    # test_char = {
    #     'level': 1,
    #     'active_quests': [],
    #     'completed_quests': [],
    #     'experience': 0,
    #     'gold': 100
    # }
    #
    # test_quests = {
    #     'first_quest': {
    #         'quest_id': 'first_quest',
    #         'title': 'First Steps',
    #         'description': 'Complete your first quest',
    #         'reward_xp': 50,
    #         'reward_gold': 25,
    #         'required_level': 1,
    #         'prerequisite': 'NONE'
    #     }
    # }
    #
    # try:
    #     accept_quest(test_char, 'first_quest', test_quests)
    #     print("Quest accepted!")
    # except QuestRequirementsNotMetError as e:
    #     print(f"Cannot accept: {e}")


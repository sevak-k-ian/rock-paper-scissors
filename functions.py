# Random selector for the bot
import random


def bot_random_choice(available_choices: list) -> str:
    return random.choice(available_choices)


def get_choices(human_choice: str, human_choice_label: str, bot_choice_label: str, available_choices: list,
                choices_made: dict, register_party_score: dict, register_game_score: dict) -> dict:
    choices_made["human"]: str = human_choice
    human_choice_label: str = human_choice
    choices_made["bot"] = bot_random_choice(available_choices)
    bot_choice_label: str = choices_made["bot"]
    count_party_score(choices_made, register_party_score, register_game_score)
    return choices_made


# Function to count score of the mini party
def count_party_score(choices_made: dict, register_party_score: dict, register_game_score: dict) -> dict:
    # Store in dict all the game combination possible. Key is a tuple that stores the combination (p1Choice, p2Choice)
    # & value is the winner according to the combination.
    outcomes: dict = {
        ("rock", "scissors"): "human",
        ("paper", "rock"): "human",
        ("scissors", "paper"): "human",
        ("paper", "scissors"): "bot",
        ("scissors", "rock"): "bot",
        ("rock", "paper"): "bot"
    }
    # TESTING
    print(choices_made)

    if choices_made["human"] == choices_made["bot"]:
        register_party_score["human"] = 0
        register_party_score["bot"] = 0
        print(register_party_score)
        count_game_score(register_party_score, register_game_score)
        return register_party_score
    else:
        party_outcome: tuple = (choices_made["human"], choices_made["bot"])
        winner: str = outcomes.get(party_outcome)
        register_party_score["human"] = 0
        register_party_score["bot"] = 0
        register_party_score[f"{winner}"] += 1

        print(register_party_score)
        count_game_score(register_party_score, register_game_score)
        return register_party_score


# Function to compute entire game score
def count_game_score(register_party_score: dict, register_game_score: dict) -> dict:
    register_game_score["human"] += register_party_score["human"]
    register_game_score["bot"] += register_party_score["bot"]
    print(register_game_score)
    return register_game_score

# TODO Function to display the correct image according to choice

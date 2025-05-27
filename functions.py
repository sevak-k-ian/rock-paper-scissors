# Random selector for the bot
import random


def bot_random_choice(available_choices: list) -> str:
    """
    Selects a random choice of one item from a provided list
    :param available_choices: list of strings (rock, paper, scissors)
    :return: the string-item randomly selected
    """
    return random.choice(available_choices)

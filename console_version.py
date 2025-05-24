# 1 human user / 1 robot-random user
# 3 possibilities of choice for each
# Once human made choice, robot make its owns
# Display the 2 results
# Compute the result
# Display the final resultat by closing the game looping


#########################################################
# Variables to store data over top of loops
#########################################################
game_options: list = ["rock", "paper", "scissors"]
scores: dict = {"player1": 0, "player2": 0}
players_name: dict = {"player1": "", "player2": ""}


#########################################################
# Functions used to simulate the game logic and looping
#########################################################
def ask_players_name() -> dict:
    """
        Ask and store players name, with keys-string that could be used in other dict (like scores dict)
        :return: dict[str, str]
    """
    player1_name_input: str = input("Player 1, what's your name? : ")
    players_name["player1"]: str = player1_name_input
    player2_name_input: str = input("Player 2, what's your name? : ")
    players_name["player2"]: str = player2_name_input


def ask_users_choice(name1: str, name2: str) -> dict:
    """
        Ask the two users, one by one, to input their choice among the game options. If not expected input received,
        warning message is printed and correct input demand asked again.
        :return: dict[str, str] which are the two valid user choices.
    """
    while True:
        player1_choice: str = input(f"{name1} rock, paper or scissors? : ").strip().lower()
        if player1_choice in game_options:
            break
        else:
            print("Wrong input")

    while True:
        player2_choice: str = input(f"{name2} rock, paper or scissors? : ").strip().lower()
        if player2_choice in game_options:
            break
        else:
            print("Wrong input")

    return {"player1": player1_choice, "player2": player2_choice}


def scoring(choice_player_1: str, choice_player_2: str, name1: str, name2: str) -> None:
    """
        Take 2 strings (expected 2 valid ones coming from game_options) and add points, or not, in a dictionary
        that stores the player1 and player2 scores.
        :param choice_player_1:
        :param choice_player_2:
        :return: None
    """
    # Store in dict all the game combination possible. Key is a tuple that stores the combination (p1Choice, p2Choice)
    # & value is the winner according to the combination.
    outcomes: dict = {
        ("rock", "scissors"): "player1",
        ("paper", "rock"): "player1",
        ("scissors", "paper"): "player1",
        ("paper", "scissors"): "player2",
        ("scissors", "rock"): "player2",
        ("rock", "paper"): "player2"
    }

    if choice_player_1 == choice_player_2:
        print(f"{name1} & {name2} equal game 😐")
    else:
        party_outcome: tuple = (choice_player_1, choice_player_2)
        winner: str = outcomes.get(party_outcome)
        scores[f"{winner}"] += 1
        print(f"{players_name[winner]} you won 💪")


def display_final_result() -> str:
    if scores["player1"] > scores["player2"]:
        return f"{players_name["player1"]} you won 👏"
    elif scores["player1"] < scores["player2"]:
        return f"{players_name["player2"]} you won 👏"
    else:
        return f"{players_name["player1"]} and {players_name["player2"]} it's a draw match for today 🙏"


#########################################################
# Game looping session / Main logic
#########################################################
def gaming_session() -> None:
    """
        Use play() and scoring() functions to simulate a game which continues until user says "stop"
        :return: None
    """
    ask_players_name()

    play_together: bool = True
    while play_together:
        # Ask choices and score them which modifies the scores dict (global variable)
        choices: dict = ask_users_choice(name1=players_name["player1"], name2=players_name["player2"])
        scoring(choice_player_1=choices["player1"], choice_player_2=choices["player2"],
                name1=players_name["player1"], name2=players_name["player2"])

        yes_or_stop: list = ["yes", "stop"]

        # Ask after that logic if still want to continue, continue the following loop until answer is "stop"
        while True:
            still_want_play: str = input("Another throw❓(yes/stop): ").strip().lower()

            if still_want_play in yes_or_stop:
                if still_want_play == "yes":
                    play_together = True
                    break
                elif still_want_play == "stop":
                    # Break the upper loop (choices/scoring) by turning the upper_scope play_together to False
                    play_together = False
                    break
            else:
                print("Wrong input")

    print(f"------------------------------\n"
          f"Here are the final results:\n"
          f"- {players_name["player1"]} you got {scores["player1"]} points\n"
          f"- {players_name["player2"]} you got {scores["player2"]} points\n"
          f"→ {display_final_result()}\n"
          f"👋👋👋 See you next time!\n"
          f"------------------------------")


# gaming_session()
gaming_session()

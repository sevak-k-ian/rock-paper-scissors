################################################
# GLOBAL VARIABLES
################################################
# TODO Add a ui.button('Exit', on_click=ui.shutdown) if you want to fully stop the server.
# TODO Implement web images that will be called when a console button is selected (instead of text)
# TODO Add a "fake" waiting animation every time a console button is selected (to give impression there is thinking in the choice of the bot)
# TODO Store the result in an online database
# TODO Push online my game (on armelys, onestensemble)

from nicegui import ui
import functions

################################################
# GLOBAL VARIABLES
################################################
# Constant variables
possible_choices: list = ["rock", "paper", "scissors"]

# Variables to store data modified by user actions
players_name: dict = {"human": "", "bot": "Robot"}
players_party_choices: dict = {"human": "", "bot": ""}
party_score: dict = {"human": 0, "bot": 0}
game_scores: dict = {"human": 0, "bot": 0}  # A game is made of several parties

# Variables to display data on screen
# Main layout that will be cleared after
main_layout = ui.column().classes("w-full justify-center h-screen items-center")
# Popup box that opens at program start to get user's name
get_user_name_dialog_box = ui.dialog()  # 1st dialog box to start every game
human_choice_label: ui.label = None  # Displays the choice made by use which is stored in players_party_choices via get_choices() triggered by on_click (3 cards)
bot_choice_label: ui.label = None  # Displays the choice made by the bot via functions.bot_random_choice(possible_choices) and stored in players_party_choices
party_score_label: ui.label = None  # Displays the score of the current party stored in party_score via get_choices() using count_party_score()
final_score_display: ui.label = None  # Displays the final score when End Session triggers on_click handle_end_game()
end_game_window: ui.card = None  # Element that appears with handle_end_game()


################################################
# GUI / INTERACTION FUNCTIONS
################################################
# Function to count score of the mini party
def count_party_score(choices_made: dict = players_party_choices, current_party_score: dict = party_score,
                      running_game_score: dict = game_scores) -> dict:
    """
    Determines the winner of a single round (party) based on human and bot choices.
    Updates the party score (points for this round) and subsequently the overall game score.

    This function, by default, directly modifies the global `party_score` and `game_scores`
    dictionaries if they are used as `current_party_score` and `running_game_score` respectively.

    :param choices_made: Dictionary containing "human" and "bot" choices.
                         Defaults to the global `players_party_choices`.
    :param current_party_score: Dictionary to store the score of the current party (round).
                                 Defaults to the global `party_score`.
    :param running_game_score: Dictionary to store the cumulative game score.
                                Defaults to the global `game_scores`.
    :return: The updated `current_party_score` dictionary for the current round.
    """
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

    # Reset party scores for the current round before assigning points
    current_party_score["human"]: int = 0
    current_party_score["bot"]: int = 0

    if choices_made["human"] == choices_made["bot"]:
        # It's a tie, no points awarded for this party
        pass  # Scores remain 0,0 for this party
    else:
        party_outcome: tuple = (choices_made["human"], choices_made["bot"])
        winner: str = outcomes.get(party_outcome)
        if winner:  # Ensure a winner was found (should always be the case with valid inputs)
            current_party_score[winner] += 1

    print(f"Party Score Updated: {current_party_score}")  # For debugging
    count_game_score(current_party_score, running_game_score)
    return current_party_score


# Function to compute entire game score
def count_game_score(current_party_score: dict, running_game_score: dict = game_scores) -> dict:
    """
    Updates the overall game score using the results from the most recent party (round).

    This function, by default, directly modifies the global `game_scores` dictionary
    if it's used as `running_game_score`.

    :param current_party_score: Dictionary containing the scores ("human", "bot") for the just-concluded party.
    :param running_game_score: Dictionary to accumulate the total game scores.
                               Defaults to the global `game_scores`.
    :return: The updated `running_game_score` dictionary.
    """
    running_game_score["human"] += current_party_score["human"]
    running_game_score["bot"] += current_party_score["bot"]
    print(f"Game Score Updated: {running_game_score}")  # For debugging
    return running_game_score


def get_choices(human_choice: str) -> dict:
    """
    Processes the human player's choice, generates the bot's choice, updates UI labels,
    calculates party scores, and updates the party score display.

    Modifies global variables: `players_party_choices`, `human_choice_label`,
    `bot_choice_label`, `party_score`, `game_scores`, and `party_score_label`.

    :param human_choice: The choice made by the human player (e.g., "rock", "paper", "scissors").
    :return: The dictionary `players_party_choices` containing both human and bot choices for the round.
    """
    global players_party_choices, human_choice_label, possible_choices, bot_choice_label, party_score, game_scores, party_score_label

    players_party_choices[
        "human"]: str = human_choice  # human_choice will be given by (rock eg) rock_btn = ui.button("🪨", on_click=lambda: get_choices(human_choice="rock"))
    if human_choice_label:
        human_choice_label.set_text(human_choice)  # Provided by the string contained by the button clicked

    players_party_choices["bot"] = functions.bot_random_choice(possible_choices)
    if bot_choice_label:
        bot_choice_label.set_text(players_party_choices["bot"])

    # Calculate scores for this round, updating global party_score and game_scores
    count_party_score(choices_made=players_party_choices, current_party_score=party_score,
                      running_game_score=game_scores)

    if party_score_label:
        party_score_label.set_text(f"{party_score["human"]} - {party_score["bot"]}")
    return players_party_choices


def clear_data_for_new_session() -> None:
    """
    Resets all session-specific global variables to their initial states.
    This includes player names (partially), choices, party scores, game scores,
    and UI label references. Intended to be called before starting a new game.

    Modifies global variables: `players_name`, `players_party_choices`, `party_score`,
    `game_scores`, `human_choice_label`, `bot_choice_label`, `party_score_label`,
    `final_score_display`, `end_game_window`.

    :return: None
    :rtype: None
    """
    global players_name, players_party_choices, party_score, game_scores
    # Reset data stores (human name kept if already set, bot name is constant)
    # Variables to store data modified by user actions
    players_name["human"]: str = ""
    players_party_choices: dict = {"human": "", "bot": ""}
    party_score: dict = {"human": 0, "bot": 0}
    game_scores: dict = {"human": 0, "bot": 0}

    # Reset UI element references (they will be recreated or reassigned)
    global human_choice_label, bot_choice_label, party_score_label, final_score_display, end_game_window
    human_choice_label = None
    bot_choice_label = None
    party_score_label = None
    final_score_display = None
    end_game_window = None


def handle_end_game() -> None:
    """
    Displays the end-of-game screen with final scores and options to restart or quit.
    Creates a new UI card (`end_game_window`) for this purpose.
    This function calls `clear_data_for_new_session` to prepare for a potential new game
    *after* displaying the current game's results.

    Modifies global variables: `end_game_window`, `final_score_display`.
    Uses global variables: `players_name`, `game_scores`.

    :return: None
    :rtype: None
    """
    global end_game_window
    end_game_window = ui.card(align_items="center")

    with end_game_window:
        ui.label("Résultat de la session")
        global players_name, game_scores, final_score_display
        final_score_display = ui.label(
            f"{players_name["human"]}: {game_scores["human"]} - {players_name["bot"]}: {game_scores["bot"]}")
        restart_session_btn = ui.button(text="Jouer de nouveau", on_click=launch_new_session)
        stop_all_btn = ui.button(text="Stop all", on_click=end_session)
        clear_data_for_new_session()


def launch_new_session() -> None:
    """
    Initiates a new game session by opening the dialog box to get the user's name.

    Opens up by overlaying the existing layout.

    :return: None
    :rtype: None
    """
    get_user_name_dialog_box.open()


def end_session() -> None:
    """
    Clears the main UI layout and displays a "Thank you" message, effectively ending the application's interactive part.

    Modifies global `main_layout`.

    :return: None
    :rtype: None
    """
    global main_layout
    main_layout.clear()
    main_layout.classes("text-xl font-bold")
    with main_layout:
        ui.label("Merci d'avoir joué !")
        ui.label("A bientôt !")


################################################
# MAIN LAYOUT FUNCTION TO SHOW AFTER DIALOG BOX CLOSED
################################################
with get_user_name_dialog_box:  # Dialog box to save user's name to global variable
    with ui.card().classes(
            "p-6"):  # get_user_name_dialog_box is a variable that store ui.dialog() element so so I can control it later with .open() or .close().
        ui.label("Bienvenue au jeu ! Quel est ton prénom ?")
        player_name_input = ui.input("Ecris")
        player_name_input_btn = ui.button("Valider", on_click=lambda: save_name_and_close())


def save_name_and_close():
    """
    Saves the player's name entered in the dialog box to a global variable,
    closes the dialog, and then calls `show_main_layout` to display the main game interface.

    Uses `player_name_input` to get value.

    :return: None
    :rtype: None
    """
    global player_name_input
    players_name["human"]: str = player_name_input.value
    get_user_name_dialog_box.close()
    show_main_layout()


def show_main_layout():
    """
    Clears and rebuilds the main game interface within the `main_layout` container.
    This includes score displays, choice cards, and game control buttons.

    Modifies global `main_layout` and various global UI element references
    (`party_score_label`, `human_choice_label`, `bot_choice_label`, `final_score_display`).
    Uses global `players_name`.

    :return: None
    :rtype: None
    """
    global main_layout
    main_layout.clear()

    with main_layout:
        # == Main page column that centers all its children both horizontally and vertically (full screen) ==
        with ui.column().classes("w-1/2 justify-center h-screen items-center"):
            # === Score header section ===
            # Displays the title and current score of the party
            with ui.row().classes("mb-12"):
                with ui.column().classes("text-xl font-bold"):
                    # Centered label: title of the score section
                    with ui.row().classes("w-full justify-center"):
                        title_score = ui.label("Score de la partie")

                    # Centered label: actual score
                    with ui.row().classes("w-full justify-center"):
                        global party_score_label
                        party_score_label = ui.label()

            # === Card display section ===
            # Grid with 4 columns: player name (left), 2 cards (center), bot name (right)
            with ui.row().classes('grid grid-cols-4 gap-4 w-full mb-12'):
                # Left-aligned human player name in first column
                with ui.column().classes('items-start text-xl font-bold'):
                    ui.label(f"{players_name["human"]}")

                # First card, human-player choice
                with ui.card().classes('p-4 items-center'):
                    global human_choice_label
                    human_choice_label = ui.label()  # At game start, it is empty. Then will display choice thanks to get_choices()
                    # ui.image('https://example.com/rock.png').classes('w-16 h-16')  # Image en dessous

                # Second card, human-player choice
                with ui.card().classes('p-4 items-center'):
                    global bot_choice_label
                    bot_choice_label = ui.label()  # At game start, it is empty. Then will display choice thanks to get_choices()
                    # ui.image('https://example.com/scissors.png').classes('w-16 h-16')

                # Right-aligned bot name in fourth column
                with ui.column().classes('items-end text-xl font-bold'):
                    ui.label(f"{players_name["bot"]}")

            # === Game controls section ===
            # Row with 3 columns storing: Rock button choice, Paper button choice, Scissors button choice
            with ui.row().classes('grid grid-cols-3 gap-3 w-full'):
                # Player chooses rock / paper / scissors
                rock_btn = ui.button("🪨", on_click=lambda: get_choices(human_choice="rock"))
                paper_btn = ui.button("📄", on_click=lambda: get_choices(human_choice="paper"))
                scissors_btn = ui.button("✂️", on_click=lambda: get_choices(human_choice="scissors"))

            # Row with End Session button
            with ui.row().classes('grid grid-cols-1 w-full'):
                # End the current session
                end_session_btn = ui.button(text="End session",
                                            on_click=lambda: handle_end_game())

            # === Final score display ===
            # Only shown when session ends
            with ui.row().classes("w-full justify-center "):
                global final_score_display
                final_score_display = ui.label()


get_user_name_dialog_box.open()
ui.run()

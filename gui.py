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
game_scores: dict = {"human": 0, "bot": 0}

# Variables to display data on screen
# Main layout that will be cleared after
main_layout = ui.column().classes("w-full justify-center h-screen items-center")
# Popup box that opens at program start to get user's name
get_user_name_dialog_box = ui.dialog()
human_choice_label: str = None
bot_choice_label: str = None
party_score_label: str = None
final_score_display: str = None
end_game_window = None


# player_name_input: str = None
# player_name_input_btn = None


################################################
# GUI / INTERACTION FUNCTIONS
################################################
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
    # TESTING PURPOSE
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


def get_choices(human_choice: str) -> dict:
    global players_party_choices
    players_party_choices["human"]: str = human_choice
    global human_choice_label
    human_choice_label.set_text(human_choice)
    global possible_choices
    players_party_choices["bot"] = functions.bot_random_choice(possible_choices)
    global bot_choice_label
    bot_choice_label.set_text(players_party_choices["bot"])
    global party_score, game_scores
    count_party_score(choices_made=players_party_choices, register_party_score=party_score,
                      register_game_score=game_scores)
    party_score_label.set_text(f"{party_score["human"]} - {party_score["bot"]}")
    return players_party_choices


def clear_data_for_new_session() -> None:
    global players_name, players_party_choices, party_score, game_scores
    # Variables to store data modified by user actions
    players_name = {"human": "", "bot": "Robot"}
    players_party_choices = {"human": "", "bot": ""}
    party_score = {"human": 0, "bot": 0}
    game_scores = {"human": 0, "bot": 0}

    global human_choice_label, bot_choice_label, party_score_label, final_score_display, end_game_window
    human_choice_label = None
    bot_choice_label = None
    party_score_label = None
    final_score_display = None
    end_game_window = None


def handle_end_game() -> None:
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
    get_user_name_dialog_box.open()


def end_session() -> None:
    global main_layout
    main_layout.clear()
    with main_layout:
        ui.label("Bye bye")


################################################
# MAIN LAYOUT FUNCTION TO SHOW AFTER DIALOG BOX CLOSED
################################################
with get_user_name_dialog_box:  # Dialog box to save user's name to global variable
    with ui.card():  # get_user_name_dialog_box is a variable that store ui.dialog() element so so I can control it later with .open() or .close().
        ui.label("Bienvenue au jeu ! Quel est ton prénom ?")
        # global player_name_input, player_name_input_btn
        player_name_input = ui.input("Ecris")
        player_name_input_btn = ui.button("Valider", on_click=lambda: save_name_and_close())


# Function to handle opening and closing starting dialog box
def save_name_and_close():
    players_name["human"] = player_name_input.value
    get_user_name_dialog_box.close()
    show_main_layout()


def show_main_layout():
    global main_layout
    main_layout.clear()

    with main_layout:
        # Column that centers all its children both horizontally and vertically (full screen)
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
                # Left-aligned player name in first column
                with ui.column().classes('items-start text-xl font-bold'):
                    ui.label(f"{players_name["human"]}")

                # First card
                with ui.card().classes('p-4 items-center'):
                    global human_choice_label
                    human_choice_label = ui.label()
                    # ui.image('https://example.com/rock.png').classes('w-16 h-16')  # Image en dessous

                # Second card
                with ui.card().classes('p-4 items-center'):
                    global bot_choice_label
                    bot_choice_label = ui.label()
                    # ui.image('https://example.com/scissors.png').classes('w-16 h-16')

                # Right-aligned bot name in fourth column
                with ui.column().classes('items-end text-xl font-bold'):
                    ui.label(f"{players_name["bot"]}")

            # === Game controls section ===
            # Row with 3 columns: New party button, Option toggle, End session button
            with ui.row().classes('grid grid-cols-3 gap-3 w-full'):
                # Player chooses rock / paper / scissors
                rock_btn = ui.button("🪨", on_click=lambda: get_choices(human_choice="rock"))
                paper_btn = ui.button("📄", on_click=lambda: get_choices(human_choice="paper"))
                scissors_btn = ui.button("✂️", on_click=lambda: get_choices(human_choice="scissors"))

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

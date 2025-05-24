from nicegui import ui
import functions

# GLOBAL VARIABLES
players_name: dict = {"human": "", "bot": "Robot"}
party_score: dict = {"human": 0, "bot": 0}
game_scores: dict = {"human": 0, "bot": 0}

human_choice_label: str = ui.label("Caca").classes('text-lg font-bold')
bot_choice_label: str = ui.label("Caca").classes('text-lg font-bold')

# GLOBAL VARIABLES USED BY FUNCTIONS.PY
possible_choices: list = ["rock", "paper", "scissors"]
players_party_choices: dict = {"human": "", "bot": ""}

# Main layout that will be cleared after
main_layout = ui.column().classes("w-full justify-center h-screen items-center")

# POPUP BOX AFTER GAME IS LAUNCHED TO GET USER'S FIRST NAME
get_user_name = ui.dialog()
with get_user_name:  # Dialog box to save user's name to global variable
    with ui.card():  # get_user_name is a variable that store ui.dialog() element so so I can control it later with .open() or .close().
        ui.label("Bienvenue au jeu ! Quel est ton prénom ?")
        player_name_input = ui.input("Ecris")
        player_name_input_btn = ui.button("Valider", on_click=lambda: save_name_and_close())


# Function to handle "Valider" button click
def save_name_and_close():
    players_name["human"] = player_name_input.value
    get_user_name.close()
    show_main_layout()


# FUNCTION TO SHOW MAIN LAYOUT WHEN DIALOG BOX IS CLOSED
def show_main_layout():
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
                        display_party_score = ui.label(f"{party_score["human"]} - {party_score["bot"]}")

            # === Card display section ===
            # Grid with 4 columns: player name (left), 2 cards (center), bot name (right)
            with ui.row().classes('grid grid-cols-4 gap-4 w-full mb-12'):
                # Left-aligned player name in first column
                with ui.column().classes('items-start text-xl font-bold'):
                    ui.label(f"{players_name["human"]}")

                # First card
                with ui.card().classes('p-4 items-center'):
                    global human_choice_label
                    # ui.image('https://example.com/rock.png').classes('w-16 h-16')  # Image en dessous

                # Second card
                with ui.card().classes('p-4 items-center'):
                    global bot_choice_label
                    # ui.image('https://example.com/scissors.png').classes('w-16 h-16')

                # Right-aligned bot name in fourth column
                with ui.column().classes('items-end text-xl font-bold'):
                    ui.label(f"{players_name["bot"]}")

            # === Game controls section ===
            # Row with 3 columns: New party button, Option toggle, End session button
            with ui.row().classes('grid grid-cols-3 gap-3 w-full'):
                # Player chooses rock / paper / scissors
                rock_btn = ui.button("🪨", on_click=lambda: functions.get_choices(human_choice="rock",
                                                                                 available_choices=possible_choices,
                                                                                 choices_made=players_party_choices,
                                                                                 register_party_score=party_score,
                                                                                 register_game_score=game_scores,
                                                                                 human_choice_label=human_choice_label,
                                                                                 bot_choice_label=bot_choice_label))
                paper_btn = ui.button("📄", on_click=lambda: functions.get_choices(human_choice="paper",
                                                                                  available_choices=possible_choices,
                                                                                  choices_made=players_party_choices,
                                                                                  register_party_score=party_score,
                                                                                  register_game_score=game_scores,
                                                                                  human_choice_label=human_choice_label,
                                                                                  bot_choice_label=bot_choice_label))
                scissors_btn = ui.button("✂️", on_click=lambda: functions.get_choices(human_choice="scissors",
                                                                                      available_choices=possible_choices,
                                                                                      choices_made=players_party_choices,
                                                                                      register_party_score=party_score,
                                                                                      register_game_score=game_scores,
                                                                                      human_choice_label=human_choice_label,
                                                                                      bot_choice_label=bot_choice_label))

            with ui.row().classes('grid grid-cols-1 w-full'):
                # End the current session
                end_session_btn = ui.button(text="End session",
                                            on_click=lambda: final_score_display.set_text(
                                                f"{players_name["human"]}: {game_scores["human"]} - {players_name["bot"]}: {game_scores["bot"]}"))

            # === Final score display ===
            # Only shown when session ends
            with ui.row().classes("w-full justify-center "):
                final_score_display = ui.label("")


get_user_name.open()
ui.run()

import PySimpleGUI as sg
import random

# Function to create the GUI layout
def create_layout():
    layout = [
        [sg.Text("Guess a number between 1 and 100")],
        [sg.InputText(key='-GUESS-', size=(10, 1))],
        [sg.Button("Submit"), sg.Button("Exit")],
        [sg.Text("", size=(30, 1), key='-FEEDBACK-')]
    ]
    return layout

# Main game function
def number_guessing_game():
    sg.theme('LightBlue')
    layout = create_layout()
    window = sg.Window("Number Guessing Game", layout)

    # Randomly select a number between 1 and 100
    secret_number = random.randint(1, 100)
    attempts = 0

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == "Exit":
            break
        if event == "Submit":
            try:
                guess = int(values['-GUESS-'])
                attempts += 1
                
                if guess < 1 or guess > 100:
                    feedback = "Please enter a number between 1 and 100."
                elif guess < secret_number:
                    feedback = "Too low! Try again."
                elif guess > secret_number:
                    feedback = "Too high! Try again."
                else:
                    feedback = f"Congratulations! You've guessed the number {secret_number} in {attempts} attempts!"
                    # Reset the game
                    secret_number = random.randint(1, 100)
                    attempts = 0
            
            except ValueError:
                feedback = "Please enter a valid number."

            window['-FEEDBACK-'].update(feedback)
            window['-GUESS-'].update('')  # Clear input field

    window.close()

if __name__ == "__main__":
    number_guessing_game()

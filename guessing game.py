import random
import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)

def number_guessing_game():
    name = input(Fore.CYAN + Style.BRIGHT + "🎉 Welcome to the Number Guessing Game! 🎉\nWhat's your name? ")

    while True:
        print(Fore.YELLOW + f"\nHi {name}, I have chosen a number between 1 and 100. Let's see if you can guess it!")
        print(Fore.GREEN + "Type 'exit' at any time to quit the game.")

        
        number_to_guess = random.randint(1, 100)
        attempts = 0
        low_range, high_range = 1, 100

        while True:
            print(f"\n{Fore.MAGENTA}Guess a number between {low_range} and {high_range}:")
            user_input = input(Fore.WHITE + "Your guess: ").strip()

            
            if user_input.lower() == 'exit':
                print(Fore.RED + "Game Over! Thanks for playing. See you next time!")
                return

            
            if not user_input.isdigit():
                print(Fore.RED + "Please enter a valid number!")
                continue

            user_guess = int(user_input)
            attempts += 1

            
            if user_guess < number_to_guess:
                print(Fore.BLUE + "Too low! Try a higher number.")
                low_range = max(low_range, user_guess + 1)
            elif user_guess > number_to_guess:
                print(Fore.YELLOW + "Too high! Try a lower number.")
                high_range = min(high_range, user_guess - 1)
            else:
                print(Fore.GREEN + Style.BRIGHT + f"🎉 Congratulations, {name}! You've guessed the correct number {number_to_guess}!")
                print(Fore.CYAN + f"It took you {attempts} attempts.")
                break

        
        play_again = input(Fore.YELLOW + "Do you want to play again? (yes/no): ").strip().lower()
        if play_again != 'yes':
            print(Fore.CYAN + f"Thanks for playing, {name}! See you next time!")
            break

if __name__ == "__main__":
    number_guessing_game()

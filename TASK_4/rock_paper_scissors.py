import random

def get_user_choice():
    """Prompt the user to choose rock, paper, or scissors."""
    while True:
        print("\n" + "="*40)
        choice = input("Choose rock (r), paper (p), or scissors (s): ").lower().strip()
        
        # Allow single letter inputs for convenience
        if choice == 'r':
            return 'rock'
        elif choice == 'p':
            return 'paper'
        elif choice == 's':
            return 'scissors'
        elif choice in ['rock', 'paper', 'scissors']:
            return choice
        else:
            print("❌ Invalid choice! Please enter: rock, paper, scissors (or r, p, s)")

def get_computer_choice():
    """Generate a random choice for the computer."""
    choices = ['rock', 'paper', 'scissors']
    return random.choice(choices)

def determine_winner(user_choice, computer_choice):
    """Determine the winner based on the choices."""
    if user_choice == computer_choice:
        return "tie"
    
    winning_combinations = {
        'rock': 'scissors',      # Rock beats scissors
        'scissors': 'paper',     # Scissors beat paper
        'paper': 'rock'          # Paper beats rock
    }
    
    if winning_combinations[user_choice] == computer_choice:
        return "user"
    else:
        return "computer"

def display_choice(choice):
    """Display choice with an emoji for better visual feedback."""
    emojis = {
        'rock': '🪨',
        'paper': '📄',
        'scissors': '✂️'
    }
    return f"{choice.capitalize()} {emojis.get(choice, '')}"

def display_result(user_choice, computer_choice, winner, user_score, computer_score):
    """Display the choices and the result in a user-friendly way."""
    print("\n" + "="*40)
    print("GAME RESULTS")
    print("="*40)
    print(f"Your choice:      {display_choice(user_choice)}")
    print(f"Computer's choice: {display_choice(computer_choice)}")
    print("-"*40)
    
    if winner == "tie":
        print("🤝 It's a tie!")
    elif winner == "user":
        print("🎉 You win!")
    else:
        print("💻 Computer wins!")
    
    print("-"*40)
    print(f"📊 SCORE: You {user_score} - {computer_score} Computer")

def display_welcome():
    """Display welcome message and rules."""
    print("🎮" + "="*38 + "🎮")
    print("      WELCOME TO ROCK-PAPER-SCISSORS!")
    print("🎮" + "="*38 + "🎮")
    print("\n📋 GAME RULES:")
    print("- Rock 🪨 beats Scissors ✂️")
    print("- Scissors ✂️ beat Paper 📄")
    print("- Paper 📄 beats Rock 🪨")
    print("\n💡 TIP: You can type 'r', 'p', 's' for quick selection!")

def play_game():
    """Main function to play the game."""
    user_score = 0
    computer_score = 0
    ties = 0
    rounds_played = 0
    
    display_welcome()
    
    while True:
        rounds_played += 1
        print(f"\n\n🔔 ROUND {rounds_played}")
        print("-"*40)
        
        user_choice = get_user_choice()
        computer_choice = get_computer_choice()
        winner = determine_winner(user_choice, computer_choice)
        
        # Update scores
        if winner == "user":
            user_score += 1
        elif winner == "computer":
            computer_score += 1
        else:
            ties += 1
        
        display_result(user_choice, computer_choice, winner, user_score, computer_score)
        
        # Ask if user wants to play again
        while True:
            print("\n" + "-"*40)
            play_again = input("Do you want to play another round? (yes/no): ").lower().strip()
            
            if play_again in ['yes', 'y', 'no', 'n']:
                break
            print("❌ Please enter 'yes' or 'no'")
        
        if play_again in ['no', 'n']:
            # Display final statistics
            print("\n" + "="*50)
            print("🏁 GAME OVER - FINAL STATISTICS")
            print("="*50)
            print(f"Total Rounds Played: {rounds_played}")
            print(f"Your Wins: {user_score}")
            print(f"Computer Wins: {computer_score}")
            print(f"Ties: {ties}")
            print(f"Win Rate: {user_score/rounds_played*100:.1f}%" if rounds_played > 0 else "Win Rate: 0.0%")
            
            if user_score > computer_score:
                print("\n🏆 FINAL RESULT: YOU WIN THE GAME! 🏆")
            elif user_score < computer_score:
                print("\n💻 FINAL RESULT: COMPUTER WINS THE GAME!")
            else:
                print("\n🤝 FINAL RESULT: IT'S A TIE!")
            
            print("\nThanks for playing! 👋")
            print("="*50)
            break

if __name__ == "__main__":
    try:
        play_game()
    except KeyboardInterrupt:
        print("\n\n👋 Game interrupted. Thanks for playing!")
    except Exception as e:
        print(f"\n⚠️ An error occurred: {e}")
def ai_choice():
    import random
    choice_number = random.randint(1, 3)
    if choice_number == 1:
        return "rock"
    elif choice_number == 2:
        return "paper"
    elif choice_number == 3:
        return "scissors"

def win_logic(ai, player_choice):
    if player_choice == "rock":
        if ai == "rock":
            return ("d", ai)
        elif ai == "paper":
            return ("l", ai)
        elif ai == "scissors":
            return ("w", ai)
    elif player_choice == "paper":
        if ai == "rock":
            return ("w", ai)
        elif ai == "paper":
            return ("d", ai)
        elif ai == "scissors":
            return ("l", ai)
    elif player_choice == "scissors":
        if ai == "rock":
            return ("l", ai)
        elif ai == "paper":
            return ("w", ai)
        elif ai == "scissors":
            return ("d", ai)
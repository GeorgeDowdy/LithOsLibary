import tkinter as tk
import random

# Initialize the main window
root = tk.Tk()
root.title("Blackjack")
root.geometry("400x500")

# Card values and suits
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}

# Initialize player and dealer hands
player_hand = []
dealer_hand = []
balance = 100

# UI labels for displaying game status
balance_label = tk.Label(root, text=f"Balance: ${balance}", font=("Arial", 14))
balance_label.pack()

player_label = tk.Label(root, text="Your Hand:", font=("Arial", 14))
player_label.pack()

player_hand_label = tk.Label(root, text="", font=("Arial", 14))
player_hand_label.pack()

dealer_label = tk.Label(root, text="Dealer's Hand:", font=("Arial", 14))
dealer_label.pack()

dealer_hand_label = tk.Label(root, text="", font=("Arial", 14))
dealer_hand_label.pack()

result_label = tk.Label(root, text="", font=("Arial", 18), pady=20)
result_label.pack()

# Functions to manage the card deck and game mechanics
def get_card():
    """Return a random card from the deck."""
    suit = random.choice(suits)
    rank = random.choice(ranks)
    return (rank, suit)

def hand_value(hand):
    """Calculate the total value of a hand. Handle aces as 1 or 11."""
    value = sum(values[card[0]] for card in hand)
    aces = sum(1 for card in hand if card[0] == 'A')
    while value > 21 and aces:
        value -= 10
        aces -= 1
    return value

def deal():
    """Start a new game and deal two cards each to player and dealer."""
    global player_hand, dealer_hand, balance
    player_hand = [get_card(), get_card()]
    dealer_hand = [get_card(), get_card()]
    update_ui()
    result_label.config(text="")

def update_ui():
    """Update the displayed hand values and balance."""
    player_hand_label.config(text=" ".join([f"{card[0]} of {card[1]}" for card in player_hand]))
    dealer_hand_label.config(text=" ".join([f"{card[0]} of {card[1]}" for card in dealer_hand[:1]]) + " [Hidden]")
    balance_label.config(text=f"Balance: ${balance}")

def player_hit():
    """Player takes another card. Check for bust after drawing."""
    global balance
    player_hand.append(get_card())
    update_ui()
    if hand_value(player_hand) > 21:
        result_label.config(text="Bust! You lose!", fg="red")
        balance -= 10

def player_stand():
    """Player ends their turn. Dealer plays and winner is determined."""
    global balance
    # Reveal dealer's full hand and play dealer's turn
    while hand_value(dealer_hand) < 17:
        dealer_hand.append(get_card())
    dealer_hand_label.config(text=" ".join([f"{card[0]} of {card[1]}" for card in dealer_hand]))

    player_total = hand_value(player_hand)
    dealer_total = hand_value(dealer_hand)

    # Determine winner
    if dealer_total > 21 or player_total > dealer_total:
        result_label.config(text="You win!", fg="green")
        balance += 10
    elif player_total < dealer_total:
        result_label.config(text="Dealer wins!", fg="red")
        balance -= 10
    else:
        result_label.config(text="It's a tie!", fg="black")
    update_ui()

# Game control buttons
deal_button = tk.Button(root, text="Deal", command=deal, font=("Arial", 14))
deal_button.pack(pady=10)

hit_button = tk.Button(root, text="Hit", command=player_hit, font=("Arial", 14))
hit_button.pack(pady=10)

stand_button = tk.Button(root, text="Stand", command=player_stand, font=("Arial", 14))
stand_button.pack(pady=10)

# Initialize a new game
deal()
root.mainloop()
 
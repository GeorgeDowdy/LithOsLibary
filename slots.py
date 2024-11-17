import tkinter as tk
import random

# Create the main window
root = tk.Tk()
root.title("Slot Machine")

# Window size
WIDTH, HEIGHT = 400, 300
root.geometry(f"{WIDTH}x{HEIGHT}")

# Symbols and prize settings
symbols = ["🍒", "🍋", "🔔", "💎", "7️⃣"]
balance = 100
bet = 10

# Labels for slot machine display and balance
result_label = tk.Label(root, text="Good Luck!", font=("Arial", 24), pady=10)
result_label.pack()

slots_frame = tk.Frame(root)
slots_frame.pack()

# Create slot labels for display
slot1 = tk.Label(slots_frame, text="🍒", font=("Arial", 48))
slot2 = tk.Label(slots_frame, text="🍒", font=("Arial", 48))
slot3 = tk.Label(slots_frame, text="🍒", font=("Arial", 48))
slot1.grid(row=0, column=0, padx=10)
slot2.grid(row=0, column=1, padx=10)
slot3.grid(row=0, column=2, padx=10)

balance_label = tk.Label(root, text=f"Balance: ${balance}", font=("Arial", 14))
balance_label.pack()

# Function to update slots and check for wins
def spin():
    global balance
    if balance < bet:
        result_label.config(text="Not enough balance!", fg="red")
        return

    # Deduct bet and update balance
    balance -= bet
    balance_label.config(text=f"Balance: ${balance}")

    # Randomly select symbols
    slot1_text = random.choice(symbols)
    slot2_text = random.choice(symbols)
    slot3_text = random.choice(symbols)

    # Update slot labels
    slot1.config(text=slot1_text)
    slot2.config(text=slot2_text)
    slot3.config(text=slot3_text)

    # Check for wins
    if slot1_text == slot2_text == slot3_text:
        prize = bet * 10
        balance += prize
        result_label.config(text=f"Jackpot! You win ${prize}!", fg="green")
    else:
        result_label.config(text="Try Again!", fg="black")

    # Update balance display
    balance_label.config(text=f"Balance: ${balance}")

# Spin button
spin_button = tk.Button(root, text="Spin", font=("Arial", 18), command=spin)
spin_button.pack(pady=20)

# Run the main loop
root.mainloop()
 
import tkinter as tk
from src.Hackenbush import HackenbushGame


def test_Hackenbush_game():
    player1 = input("Player 1 :")
    player2 = input("Player 2 :")
    window = tk.Tk()
    HackenbushGame(window, player1, player2)
    window.mainloop()

# ================================
# Main
# ================================

test_Hackenbush_game()
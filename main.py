# main.py
import sys
import tkinter as tk
from gui import DurakGUI
from evaluate import evaluate_bots

def run_gui(bot_strategy="random"):
    root = tk.Tk()
    app = DurakGUI(root, bot_strategy=bot_strategy)
    root.mainloop()

def run_evaluation(strategies=["random", "aggressive", "defensive"], num_games=1000):
    evaluate_bots(strategies, num_games)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py [gui|evaluate] [bot_strategy|num_games]")
        print("Examples:")
        print("  python main.py gui aggressive")
        print("  python main.py evaluate 1000")
        sys.exit(1)

    mode = sys.argv[1].lower()
    if mode == "gui":
        bot_strategy = sys.argv[2].lower() if len(sys.argv) > 2 else "random"
        run_gui(bot_strategy)
    elif mode == "evaluate":
        num_games = int(sys.argv[2]) if len(sys.argv) > 2 else 1000
        strategies = ["random", "aggressive", "defensive"]
        run_evaluation(strategies, num_games)
    else:
        print(f"Unknown mode: {mode}. Use 'gui' or 'evaluate'.")
        sys.exit(1)
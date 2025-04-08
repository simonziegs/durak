# gui.py
import tkinter as tk
from tkinter import messagebox
from game import DurakGame
from bots import get_bot_action

class DurakGUI:
    def __init__(self, root, bot_strategy="random"):
        self.game = DurakGame()
        self.root = root
        self.root.title(f"Reversible Durak vs {bot_strategy.capitalize()} Bot")
        self.selected_cards = []
        self.bot_strategy = bot_strategy

        self.trump_label = tk.Label(root, text=f"Trump Suit: {self.game.trump_suit}")
        self.trump_label.pack()

        self.bottom_card_label = tk.Label(root, text=f"Bottom Card: {self.game.bottom_card}")
        self.bottom_card_label.pack()

        self.bot_hand_label = tk.Label(root, text=f"Bot Hand: {len(self.game.hands[1])} cards")
        self.bot_hand_label.pack()

        self.table_label = tk.Label(root, text="Table: []")
        self.table_label.pack()

        self.unbeaten_label = tk.Label(root, text="Unbeaten Attack: None")
        self.unbeaten_label.pack()

        self.discard_label = tk.Label(root, text="Discard Pile: []")
        self.discard_label.pack()

        self.deck_label = tk.Label(root, text=f"Deck Size: {len(self.game.deck)}")
        self.deck_label.pack()

        self.your_hand_frame = tk.Frame(root)
        self.your_hand_frame.pack()
        self.your_hand_label = tk.Label(self.your_hand_frame, text="Your Hand:")
        self.your_hand_label.pack()
        self.card_buttons = []

        self.action_frame = tk.Frame(root)
        self.action_frame.pack()
        self.attack_button = tk.Button(self.action_frame, text="Attack", command=self.attack)
        self.stop_button = tk.Button(self.action_frame, text="Stop", command=self.stop)
        self.beat_button = tk.Button(self.action_frame, text="Beat", command=self.beat)
        self.take_button = tk.Button(self.action_frame, text="Take", command=self.take)
        self.transfer_button = tk.Button(self.action_frame, text="Transfer", command=self.transfer)

        self.update_gui()

    def update_gui(self):
        self.bot_hand_label.config(text=f"Bot Hand: {len(self.game.hands[1])} cards")
        self.table_label.config(text=f"Table: {sorted(self.game.table)}")
        self.unbeaten_label.config(text=f"Unbeaten Attack: {self.game.unbeaten_attack if self.game.unbeaten_attack else 'None'}")
        self.discard_label.config(text=f"Discard Pile: {sorted(self.game.discard_pile)}")
        self.deck_label.config(text=f"Deck Size: {len(self.game.deck)}")

        for btn in self.card_buttons:
            btn.destroy()
        self.card_buttons = []
        for card in sorted(self.game.hands[0]):
            btn = tk.Button(self.your_hand_frame, text=card, command=lambda c=card: self.toggle_card(c))
            btn.pack(side=tk.LEFT)
            self.card_buttons.append(btn)

        for widget in self.action_frame.winfo_children():
            widget.pack_forget()
        if self.game.attacker == 0 and self.game.unbeaten_attack is None:
            self.attack_button.pack(side=tk.LEFT)
            if self.game.table:
                self.stop_button.pack(side=tk.LEFT)
        elif self.game.defender == 0 and self.game.unbeaten_attack:
            self.beat_button.pack(side=tk.LEFT)
            self.take_button.pack(side=tk.LEFT)
            self.transfer_button.pack(side=tk.LEFT)

        winner = self.game.check_winner()
        if winner is not None:
            messagebox.showinfo("Game Over", f"{'You' if winner == 0 else 'Bot'} wins!")
            self.root.quit()

    def toggle_card(self, card):
        if card in self.selected_cards:
            self.selected_cards.remove(card)
        else:
            self.selected_cards.append(card)
        for btn in self.card_buttons:
            btn.config(relief="raised" if btn["text"] not in self.selected_cards else "sunken")

    def attack(self):
        if not self.selected_cards:
            messagebox.showwarning("Invalid Action", "Select at least one card!")
            return
        actions = self.game.get_legal_actions()
        action = sorted(self.selected_cards[:])  # Sort attempted action
        # Convert legal actions to sorted lists for comparison
        sorted_actions = [sorted(a) if isinstance(a, list) else a for a in actions]
        print(f"Debug - Hand: {self.game.hands[0]}, Legal actions: {actions}, Attempted: {action}")
        if action not in sorted_actions:
            messagebox.showwarning("Invalid Action", "Illegal attack!")
            self.selected_cards = []
            self.update_gui()
            return
        self.game.apply_action(self.selected_cards[:])  # Apply original order
        self.selected_cards = []
        self.update_gui()
        if self.game.defender == 1 and not self.game.is_terminal():
            self.bot_turn()

    def stop(self):
        self.game.apply_action(["stop"])
        self.selected_cards = []
        self.update_gui()
        if self.game.attacker == 1 and not self.game.is_terminal():
            self.bot_turn()

    def beat(self):
        if not self.selected_cards or len(self.selected_cards) != len(self.game.unbeaten_attack):
            messagebox.showwarning("Invalid Action", f"Select exactly {len(self.game.unbeaten_attack)} card(s)!")
            return
        actions = self.game.get_legal_actions()
        action = self.selected_cards[:]
        print(f"Debug - Your hand: {self.game.hands[0]}, Unbeaten: {self.game.unbeaten_attack}, Legal actions: {actions}, Attempted: {action}")
        if len(action) == 1:
            if action not in actions:
                messagebox.showwarning("Invalid Action", "Cannot beat with this card!")
                self.selected_cards = []
                self.update_gui()
                return
        else:  # Multi-card beating
            action_set = set(action)
            legal_action_sets = [set(a) for a in actions if a != ["take"] and a[0] != "transfer"]
            if not any(action_set == legal_set for legal_set in legal_action_sets):
                messagebox.showwarning("Invalid Action", "Cannot beat with these cards!")
                self.selected_cards = []
                self.update_gui()
                return
        self.game.apply_action(action)
        self.selected_cards = []
        self.update_gui()
        if self.game.attacker == 1 and self.game.unbeaten_attack is None and not self.game.is_terminal():
            self.bot_turn()

    def take(self):
        self.game.apply_action(["take"])
        self.selected_cards = []
        self.update_gui()
        if self.game.attacker == 1 and not self.game.is_terminal():
            self.bot_turn()

    def transfer(self):
        if len(self.selected_cards) != 1:
            messagebox.showwarning("Invalid Action", "Select exactly one card to transfer!")
            return
        actions = self.game.get_legal_actions()
        action = ["transfer", self.selected_cards[0]]
        print(f"Debug - Your hand: {self.game.hands[0]}, Unbeaten: {self.game.unbeaten_attack}, Legal actions: {actions}, Attempted: {action}")
        if action not in actions:
            messagebox.showwarning("Invalid Action", "Cannot transfer with this card!")
            self.selected_cards = []
            self.update_gui()
            return
        self.game.apply_action(action)
        self.selected_cards = []
        self.update_gui()
        if self.game.defender == 1 and not self.game.is_terminal():
            self.bot_turn()

    def bot_turn(self):
        actions = self.game.get_legal_actions()
        action = get_bot_action(self.game, actions, self.bot_strategy)
        print(f"Bot ({self.bot_strategy}) hand: {self.game.hands[1]}, Actions: {actions}, Plays: {action}")
        self.game.apply_action(action)
        self.update_gui()
        if self.game.attacker == 1 and self.game.unbeaten_attack is None and not self.game.is_terminal():
            self.root.after(500, self.bot_turn)
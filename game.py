# game.py
import random
from itertools import combinations, permutations
from collections import defaultdict

RANKS = ["6", "7", "8", "9", "10", "J", "Q", "K", "A"]
SUITS = ["H", "D", "C", "S"]

class DurakGame:
    def __init__(self):
        self.deck = [rank + suit for rank in RANKS for suit in SUITS]
        random.shuffle(self.deck)
        self.trump_suit = self.deck[-1][-1]
        self.bottom_card = self.deck[-1]
        if self.trump_suit not in SUITS:
            raise ValueError(f"Invalid trump suit: {self.trump_suit}")
        self.hands = [self.deck[:6], self.deck[6:12]]
        self.deck = self.deck[12:]
        self.discard_pile = []
        self.attacker = 0
        self.defender = 1
        self.table = []
        self.unbeaten_attack = None
        self.turns = 0

    def beats(self, card1, card2):
        suit1, rank1 = card1[-1], RANKS.index(card1[:-1])
        suit2, rank2 = card2[-1], RANKS.index(card2[:-1])
        if suit2 == self.trump_suit:
            return suit1 == self.trump_suit and rank1 > rank2
        return (suit1 == suit2 and rank1 > rank2) or suit1 == self.trump_suit

    def can_beat(self, A, S):
        if len(A) != len(S):
            return False
        for s_perm in permutations(S):
            if all(self.beats(s_perm[i], A[i]) for i in range(len(A))):
                return True
        return False

    def get_legal_actions(self):
        current_player = self.attacker if self.unbeaten_attack is None else self.defender
        hand = self.hands[current_player]
        if self.unbeaten_attack is None:
            if not self.table:
                groups = defaultdict(list)
                for card in hand:
                    groups[card[:-1]].append(card)
                actions = []
                for rank_cards in groups.values():
                    max_combinations = min(len(rank_cards), len(self.hands[self.defender]))
                    for r in range(1, max_combinations + 1):
                        actions.extend(combinations(rank_cards, r))
                actions = [list(action) for action in actions]
                print(f"Debug - Attacker: Hand: {hand}, Defender hand size: {len(self.hands[self.defender])}, Groups: {dict(groups)}, Actions: {actions}")
                return actions
            else:
                table_ranks = {card[:-1] for card in self.table}
                actions = [["stop"]]
                groups = defaultdict(list)
                for card in hand:
                    groups[card[:-1]].append(card)
                for rank in table_ranks:
                    if rank in groups:
                        # Changed from 6 to 12 to allow 6 attacks + 6 defenses
                        remaining_slots = max(0, min(12 - len(self.table), len(self.hands[self.defender])))
                        max_combinations = min(len(groups[rank]), remaining_slots)
                        for r in range(1, max_combinations + 1):
                            actions.extend(combinations(groups[rank], r))
                actions = [list(action) for action in actions]
                print(f"Debug - Attacker (post-table): Hand: {hand}, Table: {self.table}, Actions: {actions}")
                return actions
        else:
            k = len(self.unbeaten_attack)
            actions = [["take"]]
            for S_tuple in combinations(hand, k):
                S = list(S_tuple)
                if self.can_beat(self.unbeaten_attack, S):
                    actions.append(S)
            next_player = (self.defender + 1) % 2
            attack_ranks = {card[:-1] for card in self.unbeaten_attack}
            groups = defaultdict(list)
            for card in hand:
                groups[card[:-1]].append(card)
            for rank in attack_ranks:
                if rank in groups and len(self.unbeaten_attack) < len(self.hands[next_player]):
                    for card in groups[rank]:
                        actions.append(["transfer", card])
            print(f"Debug - Defender: Hand: {hand}, Unbeaten: {self.unbeaten_attack}, Actions: {actions}")
            return actions

    def apply_action(self, action):
        self.turns += 1
        if self.unbeaten_attack is None:
            if action == ["stop"]:
                self.discard_pile.extend(self.table)
                self.table = []
                self.unbeaten_attack = None
                self.attacker, self.defender = self.defender, self.attacker
                self.draw_cards()
                return self.check_winner()
            else:
                for card in action:
                    if card not in self.hands[self.attacker]:
                        raise ValueError(f"Card {card} not in attacker's hand: {self.hands[self.attacker]}")
                    self.hands[self.attacker].remove(card)
                self.table.extend(action)
                self.unbeaten_attack = action
                return None
        else:
            if action == ["take"]:
                self.hands[self.defender].extend(self.table)
                self.table = []
                self.unbeaten_attack = None
                self.draw_cards()
                return self.check_winner()
            elif action[0] == "transfer":
                card = action[1]
                self.hands[self.defender].remove(card)
                self.table.append(card)
                self.unbeaten_attack.append(card)
                self.attacker, self.defender = self.defender, (self.defender + 1) % 2
                return None
            else:
                assert self.can_beat(self.unbeaten_attack, action), "Invalid beat"
                self.table.extend(action)
                for card in action:
                    self.hands[self.defender].remove(card)
                self.unbeaten_attack = None
                return None

    def draw_cards(self):
        for player in [self.attacker, self.defender]:
            while len(self.hands[player]) < 6 and self.deck:
                self.hands[player].append(self.deck.pop(0))

    def check_winner(self):
        if len(self.hands[0]) == 0:
            return 0
        elif len(self.hands[1]) == 0:
            return 1
        return None

    def is_terminal(self):
        return len(self.hands[0]) == 0 or len(self.hands[1]) == 0
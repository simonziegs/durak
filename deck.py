from cards import Card

class Deck:
    def __init__(self):
        self.cards = self.create_deck()

    def create_deck(self):
        ranks = ['6','7','8','9','T','J','Q','K','A']
        suits = ['hearts','diamonds','spades','clubs']

        return [Card(rank, suit, False) for rank in ranks for suit in suits]
    
    def shuffle(self):
        import random
        random.shuffle(self.cards)
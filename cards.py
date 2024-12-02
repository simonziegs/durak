class Card:
    def __init__(self, rank, suit, trump):
        self.rank = rank
        self.suit = suit
        self.trump = trump
    
    def __repr__(self):
        return f"{self.rank} of {self.suit} ({'Trump' if self.trump else 'Non-trump'})"
"""A deck of playing cards (port of ch14/Deck.java)."""
from .card import Card
from .card_collection import CardCollection


class Deck(CardCollection):

    def __init__(self, label):
        super().__init__(label)
        for suit in range(4):
            for rank in range(1, 14):
                self.add_card(Card(rank, suit))

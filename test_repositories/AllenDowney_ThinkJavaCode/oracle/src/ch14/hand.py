"""A hand of playing cards (port of ch14/Hand.java)."""
from .card_collection import CardCollection


class Hand(CardCollection):

    def __init__(self, label):
        super().__init__(label)

    def display(self):
        print(self.get_label() + ": ")
        for i in range(self.size()):
            print(self.get_card(i))
        print()

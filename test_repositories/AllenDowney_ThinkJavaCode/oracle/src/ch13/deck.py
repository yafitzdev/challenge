"""A deck of playing cards of fixed size (port of ch13/Deck.java).

The Java original is an exercise skeleton: shuffle and the sort methods
are empty stubs, randomInt/indexLowest return 0, merge returns null and
mergeSort returns this.  This port keeps that behavior.
"""
from .card import Card


class Deck:

    def __init__(self, n=None):
        if n is None:
            self.cards = []
            for suit in range(4):
                for rank in range(1, 14):
                    self.cards.append(Card(rank, suit))
        else:
            self.cards = [None] * n

    def get_cards(self):
        return self.cards

    def print(self):
        for card in self.cards:
            print("null" if card is None else card)

    def __str__(self):
        return "[" + ", ".join("null" if c is None else str(c)
                               for c in self.cards) + "]"

    def random_int(self, low, high):
        return 0

    def swap_cards(self, i, j):
        pass

    def shuffle(self):
        pass

    def index_lowest(self, low, high):
        return 0

    def selection_sort(self):
        pass

    def subdeck(self, low, high):
        sub = Deck(high - low + 1)
        for i in range(len(sub.cards)):
            sub.cards[i] = self.cards[low + i]
        return sub

    @staticmethod
    def merge(d1, d2):
        return None

    def merge_sort(self):
        return self

    def insertion_sort(self):
        pass

    def check_sorted(self):
        """Port of ch13/Test.checkSorted: prints unsorted positions."""
        cards = self.cards
        for i in range(len(cards) - 1):
            if cards[i].compare_to(cards[i + 1]) >= 0:
                print("Card #%d not sorted!" % i)

    def is_sorted(self):
        """Boolean form of Test.checkSorted."""
        cards = self.cards
        for i in range(len(cards) - 1):
            if cards[i].compare_to(cards[i + 1]) >= 0:
                return False
        return True

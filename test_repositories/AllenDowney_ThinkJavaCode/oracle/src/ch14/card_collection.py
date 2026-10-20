"""A collection of playing cards (port of ch14/CardCollection.java)."""
import random


class CardCollection:

    def __init__(self, label):
        self._label = label
        self._cards = []

    def get_label(self):
        return self._label

    def add_card(self, card):
        self._cards.append(card)

    def pop_card(self, i=None):
        if i is None:
            i = self.size() - 1
        return self._cards.pop(i)

    def size(self):
        return len(self._cards)

    def __len__(self):
        return self.size()

    def empty(self):
        return len(self._cards) == 0

    def deal(self, that, n):
        for _ in range(n):
            card = self.pop_card()
            that.add_card(card)

    def deal_all(self, that):
        n = self.size()
        self.deal(that, n)

    def get_card(self, i):
        return self._cards[i]

    def last(self):
        return self._cards[self.size() - 1]

    def swap_cards(self, i, j):
        self._cards[i], self._cards[j] = self._cards[j], self._cards[i]

    def shuffle(self):
        for i in range(self.size() - 1, 0, -1):
            j = random.randrange(i)
            self.swap_cards(i, j)

    def __str__(self):
        return self._label + ": [" + ", ".join(str(c) for c in self._cards) + "]"

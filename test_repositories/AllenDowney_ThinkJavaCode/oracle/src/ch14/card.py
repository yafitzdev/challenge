"""A standard playing card (port of ch12/Card.java, used by ch13)."""


class Card:

    RANKS = [None, "Ace", "2", "3", "4", "5", "6", "7",
             "8", "9", "10", "Jack", "Queen", "King"]

    SUITS = ["Clubs", "Diamonds", "Hearts", "Spades"]

    def __init__(self, rank, suit):
        self._rank = rank
        self._suit = suit

    def compare_to(self, that):
        if self._suit < that._suit:
            return -1
        if self._suit > that._suit:
            return 1
        if self._rank < that._rank:
            return -1
        if self._rank > that._rank:
            return 1
        return 0

    def equals(self, that):
        return self._rank == that._rank and self._suit == that._suit

    def __eq__(self, other):
        if not isinstance(other, Card):
            return NotImplemented
        return self.equals(other)

    __hash__ = object.__hash__

    def get_rank(self):
        return self._rank

    def get_suit(self):
        return self._suit

    def position(self):
        return self._suit * 13 + self._rank - 1

    def __str__(self):
        return Card.RANKS[self._rank] + " of " + Card.SUITS[self._suit]

    __repr__ = __str__

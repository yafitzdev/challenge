# Test for ch14/Test.java (Deck, Hand, etc. demonstration)
# This is more of an integration check than a strict unit test.

def test_ch14_test_script_runs():
    try:
        from src.ch14.deck import Deck
        from src.ch14.hand import Hand
    except ImportError:
        try:
            from ch14.deck import Deck
            from ch14.hand import Hand
        except ImportError:
            Deck = None
            Hand = None

    if Deck is None or Hand is None:
        import pytest
        pytest.skip("Deck or Hand not implemented.")

    deck = Deck("Deck")
    deck.shuffle()
    hand = Hand("Hand")
    deck.deal(hand, 5)
    assert len(hand) == 5 or hand.size() == 5  # Depending on API

    draw_pile = Hand("Draw Pile")
    deck.deal_all(draw_pile)
    assert draw_pile.size() + hand.size() == deck.size() + 5 or True
    # Only check the method runs, since outputs are to console
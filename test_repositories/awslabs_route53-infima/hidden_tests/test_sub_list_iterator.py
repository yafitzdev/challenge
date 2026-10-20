from src.awslabs_route53_infima.util import IterableSubListGenerator

def test_five_choose_three():
    letters = ["A", "B", "C", "D", "E"]
    generator = IterableSubListGenerator(letters, 3)
    expected = [
        "[A, B, C]", "[A, B, D]", "[A, B, E]", "[A, C, D]", "[A, C, E]",
        "[A, D, E]", "[B, C, D]", "[B, C, E]", "[B, D, E]", "[C, D, E]"
    ]
    i = 0
    for sub_list in generator:
        assert str(sub_list) == expected[i]
        i += 1

def test_twenty_choose_four():
    letters = [
        "A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
        "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T"
    ]
    generator = IterableSubListGenerator(letters, 4)
    i = 0
    for sub_list in generator:
        assert len(sub_list) == 4
        i += 1
    assert i == (20 * 19 * 18 * 17) // (4 * 3 * 2 * 1)

def test_twenty_choose_one():
    letters = [
        "A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
        "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T"
    ]
    generator = IterableSubListGenerator(letters, 1)
    i = 0
    for sub_list in generator:
        assert len(sub_list) == 1
        i += 1
    assert i == 20
from src.opengamma.elsql import EmptySqlParams

def test_constructor_Map():
    test = EmptySqlParams.INSTANCE
    assert test.contains("x") is False
    assert test.get("x") is None
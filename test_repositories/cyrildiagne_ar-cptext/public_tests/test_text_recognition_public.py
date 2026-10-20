import pytest
from src.arcopypaste.research.prototypes.text import TextRecognition

def test_degrees_to_firebase_rotation_valid_public():
    obj = TextRecognition.TextRecognition()
    assert obj.degreesToFirebaseRotation(0) == 0
    assert obj.degreesToFirebaseRotation(90) == 1
    assert obj.degreesToFirebaseRotation(180) == 2
    assert obj.degreesToFirebaseRotation(270) == 3

def test_degrees_to_firebase_rotation_invalid_public():
    obj = TextRecognition.TextRecognition()
    with pytest.raises(ValueError):
        obj.degreesToFirebaseRotation(135)
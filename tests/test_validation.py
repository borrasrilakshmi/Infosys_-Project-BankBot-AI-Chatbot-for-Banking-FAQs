def validate_input(text):
    return bool(text and len(text) > 2)

def test_input_validation():
    assert validate_input("Transfer money") is True
    assert validate_input("") is False

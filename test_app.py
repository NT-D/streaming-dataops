import pytest
from app import add

def test_add():
    """add returns added value"""
    result = add(1,2)
    assert result == 3

if __name__ == "__main__":
    unittest.main()
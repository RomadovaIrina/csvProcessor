import pytest
from app.normalization import normalize_phone, normalize_amount, normalize_name
from app.parser_csv import parse_csv


def testphone():
    assert normalize_phone("+71111111111") == "+7(111)111-11-11"
    assert normalize_phone("8-111-111-11-11") == "+7(111)111-11-11"
    assert normalize_phone("+8 111 1111111") == "+7(111)111-11-11"
    assert normalize_phone("7(111)111-11 11") == "+7(111)111-11-11"


def test_name():
    assert normalize_name("Абдуллаев Рамиль Ахмед оглы") == "Абдуллаев Рамиль Ахмед оглы"
    assert normalize_name("Иванов   Иван Иванович ") == "Иванов Иван Иванович"
    assert normalize_name("  Иванов     Иван") == "Иванов Иван"
    assert normalize_name(
        "Иванов-Петров Иван   Иванович ") == "Иванов-Петров Иван Иванович"


def test_amount():
    assert normalize_amount("5432") == 5432.0
    assert normalize_amount("1577.93") == 1577.93
    assert normalize_amount("7 311.63") == 7311.63
    assert normalize_amount("35 567.92") == 35567.92
    assert normalize_amount("13.2") == 13.2


def test_parse_csv():
    raw_data = """phone, fullname, some_amount, rating_position
    +71111111111, Иванов-Петров Иван Иванович, 34 350.5, 1
    8(111)111-11-11, Иванов     Иван Иванович, 1577.93, 2
    """

    expected_output = [
        {
            "phone": "+71111111111",
            "fullname": "Иванов-Петров Иван Иванович",
            "some_amount": "34 350.5",
            "rating_position": "1"
        },
        {
            "phone": "8(111)111-11-11",
            "fullname": "Иванов     Иван Иванович",
            "some_amount": "1577.93",
            "rating_position": "2"
        }
    ]

    assert parse_csv(raw_data) == expected_output

from algorithms.functions import multiples_of_3, non_repeating_character


def test_non_repeating_character_1():
    char = non_repeating_character("submission")
    assert char == "u"


def test_non_repeating_character_2():
    char = non_repeating_character("asEREERdfasdfdasdASDFADDFG")
    assert char == "G"


def test_multiples_1():
    char = multiples_of_3(3)
    assert char == [1, 3]


def test_multiples_2():
    char = multiples_of_3(94471298)
    assert char == [5426, 9987441]

# Tests para non_repeating_character
def test_non_repeating_character_submission():
    assert non_repeating_character("submission") == "u"

def test_non_repeating_character_all_repeat():
    assert non_repeating_character("nnn") == ""

def test_non_repeating_character_case_sensitive():
    assert non_repeating_character("SUbMission") == "U"

def test_non_repeating_character_empty():
    assert non_repeating_character("") == ""

def test_non_repeating_character_single():
    assert non_repeating_character("A") == "A"

# Tests para multiples_of_3
def test_multiples_3_example_1():
    assert multiples_of_3(39) == [4, 93]  # 3, 9, 39, 93

def test_multiples_3_example_2():
    assert multiples_of_3(330) == [5, 330]  # 3, 30, 33, 303, 330

def test_multiples_3_example_3():
    assert multiples_of_3(23) == [1, 3]  # only 3

def test_multiples_3_none_valid():
    assert multiples_of_3(1) == [0, None]

def test_multiples_3_zero():
    assert multiples_of_3(0) == [0, None]

def test_multiples_3_large():
    result = multiples_of_3(123)
    assert isinstance(result, list) and len(result) == 2
    assert result[0] >= 1  # there are several like 3, 12, 123 etc.

def test_multiples_3_avoid_duplicates():
    assert multiples_of_3(111) == [1, 111]  # only 111
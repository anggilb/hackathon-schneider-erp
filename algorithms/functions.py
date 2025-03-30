from collections import Counter
from itertools import permutations

def non_repeating_character(string):
    """
    Given a string, return the first non-repeating character. If there is no such character, return an empty string.
    Character comparisions are case-insentive (e.g. 'A' and 'a' are considered the same), but you should return the character in its original case as it appears in the input string.

    Examples:
        string = 'submission' -> return 'u'
        string = 'nnn' -> return ''
        string = 'SUbMission' -> return 'U'

    """
    counts = Counter(c.lower() for c in string)
    for c in string:
        if counts[c.lower()] == 1:
            return c
    return ''


def multiples_of_3(num):
    """
    Given an integer (num), return a list containing two values:
    - The total number of unique numbers that are divisible by 3, formed from the combinations of the digits of num.
    - From the combinations, the maximum number divisible by 3.
    - Note:
        - 0 is excluded from the count.
        - The numbers must be formed from the digits of `num` and the combinations can have different lengths.
        - If there is no number that has all the properties, return [0, None]

    Example:
        num = 39 -> return [4, 93] . All possible numbers are 3,9,39,93 , as all of them are multiples of 3, the total number of multiples is 4 and the maximum number is 93.
        num = 330 -> return [5,330] . The numbers are 3,30,33,303,330 , as all of them are multiples of 3, the total number of multiples is 5 and the maximum number is 330.
        num = 23 -> return [1,3] . The numbers are 2,3,23,32. The only number multiple of 3 in this case is 3 itself.

    """

    digits = list(str(num))
    seen = set()
    valid = set()

    for i in range(1, len(digits) + 1):
        for perm in permutations(digits, i):
            val = int(''.join(perm))
            if val != 0 and val not in seen:
                seen.add(val)
                if val % 3 == 0:
                    valid.add(val)

    if not valid:
        return [0, None]
    return [len(valid), max(valid)]

def highestToLowest(numbers: list[int]) -> list[int]:
    """Sort numbers Highest to Lowest, expects array to be passed returns array."""
    result = []
    lastNumber = None

    for a in range(len(numbers)):
        highestNumber = None
        for b in range(len(numbers)):
            if highestNumber is None or numbers[b] > highestNumber:
                if lastNumber is None or numbers[b] < lastNumber:
                    highestNumber = numbers[b]
        if highestNumber is None:
            break
        lastNumber = highestNumber
        result.append(highestNumber)

    return result


def lowestToHighest(numbers: list[int]) -> list[int]:
    """Sort numbers Lowest to Highest, expects array to be passed returns array."""
    result = []
    lastNumber = None

    for a in range(len(numbers)):
        highestNumber = None
        for b in range(len(numbers)):
            if highestNumber is None or numbers[b] < highestNumber:
                if lastNumber is None or numbers[b] > lastNumber:
                    highestNumber = numbers[b]
        if highestNumber is None:
            break
        lastNumber = highestNumber
        result.append(highestNumber)

    return result


def getLargest(numbers: list[int]) -> int:
    """Get the largest number from a list of integers, expects array returns int."""
    lastNumber = 0

    for a in range(len(numbers)):
        if numbers[a] >= lastNumber:
            lastNumber = numbers[a]

    return lastNumber


def getSmallest(numbers: list[int]) -> int:
    """Get the smallest number from a list of integers, expects array returns int."""
    lastNumber = float('inf')

    for a in range(len(numbers)):
        if numbers[a] <= lastNumber:
            lastNumber = numbers[a]

    return lastNumber


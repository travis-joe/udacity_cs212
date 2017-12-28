import random
import math
import itertools

myDeck = [r + s for r in '23456789TJQKA' for s in 'SHDC']


# 发牌
def deal(num_hands, n=5, deck=myDeck):
    random.shuffle(deck)
    return [deck[n * i:n * (i + 1)] for i in range(num_hands)]


def poker(hands):
    """Return the best hand: poker([hand,...]) => hand
    处理手牌"""
    return allmax(hands, key=hand_rank)


def allmax(iterable, key=None):
    """处理平手"""
    result, maxval = [], None
    key = key or (lambda x: x)
    for x in iterable:
        xval = key(x)
        if not result or xval > maxval:
            result, maxval = [x], xval
        elif xval == maxval:
            result.append(x)
    return result


def hand_rank(hand):
    # 手牌比较处理规则
    ranks = card_ranks(hand)
    if straight(ranks) and flush(hand):  # straight flush
        return 8, max(ranks)
    elif kind(4, ranks):  # 4 of a kind
        return 7, kind(4, ranks), kind(1, ranks)
    elif kind(3, ranks) and kind(2, ranks):  # full house
        return 6, kind(3, ranks), kind(2, ranks)
    elif flush(hand):  # flush
        return 5, ranks
    elif straight(ranks):  # straight
        return 4, max(ranks)
    elif kind(3, ranks):  # 3 of a kind
        return 3, kind(3, ranks), ranks
    elif two_pair(ranks):  # 2 pair
        return 2, two_pair(ranks), ranks
    elif kind(2, ranks):  # kind
        return 1, kind(2, ranks), ranks
    else:  # high card
        return 0, ranks


def card_ranks(cards):
    """Return a list of the ranks, sorted with higher first.
    card_ranks(['AC', '3D', '4S', 'KH']) should output [14, 13, 4, 3]
    手牌提取数值"""
    ranks = ["--23456789TJQKA".index(r) for r, s in cards]
    ranks.sort(reverse=True)
    return [1, 2, 3, 4, 5] if ranks == [14, 5, 4, 3, 2] else ranks


def straight(ranks):
    """Return True if the ordered ranks form a 5-card straight."""
    return (max(ranks) - min(ranks) == 4) and len(set(ranks)) == 5


def flush(hand):
    """Return True if all the cards have the same suit."""
    suits = [s for r, s in hand]
    return len(set(suits)) == 1


def kind(n, ranks):
    """Return the first rank that this hand has exactly n of.
    Return None if there is no n-of-a-kind in the hand."""
    for r in ranks:
        if ranks.count(r) == n:
            return r
    return None


def two_pair(ranks):
    """If there are two pair, return the two ranks as a
    tuple: (highest, lowest); otherwise return None."""
    pair = kind(2, ranks)
    low_pair = kind(2, list(reversed(ranks)))
    if pair and low_pair != pair:
        return pair, low_pair
    else:
        return None


def test():
    """Test cases for the functions in poker program"""
    sf = "6C 7C 8C 9C TC".split()  # Straight Flush
    fk = "9D 9H 9S 9C 7D".split()  # Four of a Kind
    fh = "TD TC TH 7C 7D".split()  # Full House
    tp = "5S 5D 9H 9C 6S".split()  # Two pairs
    al = "AC 2D 4H 3D 5S".split()  # Ace-Low Straight

    fkranks = card_ranks(fk)
    tpranks = card_ranks(tp)

    assert card_ranks(sf) == [10, 9, 8, 7, 6]
    assert card_ranks(fk) == [9, 9, 9, 9, 7]
    assert card_ranks(fh) == [10, 10, 10, 7, 7]

    assert poker([sf, fk, fh]) == sf
    assert poker([fk, fh]) == fk
    assert poker([fh, fh]) == fh

    assert poker([sf]) == sf
    assert poker([sf] + 99 * [fh]) == sf

    assert hand_rank(sf) == (8, 10)
    assert hand_rank(sf) == (8, 10)
    assert hand_rank(fk) == (7, 9, 7)
    assert hand_rank(fh) == (6, 10, 7)

    assert card_ranks(['AC', '3D', '4S', 'KH']) == [14, 13, 4, 3]

    assert straight([9, 8, 7, 6, 5]) is True
    assert straight([9, 8, 8, 6, 5]) is False
    assert straight(card_ranks(al)) is True

    assert flush(sf) is True
    assert flush(fk) is False

    assert kind(4, fkranks) == 9
    assert kind(3, fkranks) is None
    assert kind(2, fkranks) is None
    assert kind(1, fkranks) == 7

    assert two_pair(tpranks) == (9, 5)
    assert two_pair(fkranks) is None

    return 'tests pass'


print(test())

hand_names = [
    'High Card',
    'Pair',
    '2 Pair',
    '3 Kind',
    'Straight',
    'Flush',
    'Full House',
    '4 Kind',
    'Straight Flush',
]


def hand_percentages(n=700 * 1000):
    """Sample n random hands and print a table of percentages for each type of hand"""
    counts = [0] * 9
    for i in range(n // 10):
        for hand in deal(10):
            ranking = hand_rank(hand)[0]
            counts[ranking] += 1
    for i in reversed(range(9)):
        print('%14s: %6.3f' % (hand_names[i], 100. * counts[i] / n))


def all_hand_percentages():
    # Print an exhaustive table of frequencies for each type of hand
    counts = [0] * 9
    n = 0
    deck = [r + s for r in '23456789TJQKA' for s in 'SHDC']
    for hand in itertools.combinations(deck, 5):
        n += 1
        ranking = hand_rank(hand)[0]
        counts[ranking] += 1
    for i in reversed(range(9)):
        print('%14s: %7d %6.3f' % (hand_names[i], counts[i], 100. * counts[i] / n))


def shuffle1(deck):
    # O(N**2)
    # incorrect distribution
    N = len(deck)
    swapped = [False] * N
    while not all(swapped):
        i, j = random.randrange(N), random.randrange(N)
        swapped[i] = swapped[j] = True
        deck[i], deck[j] = deck[j], deck[i]


def shuffle2(deck):
    # O(N**2)
    # incorrect distribution?
    N = len(deck)
    swapped = [False] * N
    while not all(swapped):
        i, j = random.randrange(N), random.randrange(N)
        swapped[i] = True
        deck[i], deck[j] = deck[j], deck[i]


def shuffle2a(deck):
    # http://forums.udacity.com/cs212-april2012/questions/3462/better-implementation-of-shuffle2
    N = len(deck)
    swapped = [False] * N
    while not all(swapped):
        i = random.choice(filter(lambda idx: not swapped[idx], range(N)))
        j = random.choice(filter(lambda idx: not swapped[idx], range(N)))
        swapped[i] = True
        deck[i], deck[j] = deck[j], deck[i]


def shuffle3(deck):
    # O(N)
    # incorrect distribution
    N = len(deck)
    for i in range(N):
        j = random.randrange(N)
        deck[i], deck[j] = deck[j], deck[i]


def knuth(deck):
    n = len(deck)
    for i in range(n - 1):
        j = random.randrange(i, n)
        deck[i], deck[j] = deck[j], deck[i]

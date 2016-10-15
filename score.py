from collections import Counter
import card
import play
from enum import IntEnum

def aces_as_low(card_values):
    return [ 1 if v == 14 else v for v in card_values ]

def card_values(cards): 
    return [ card.value(c) for c in cards ]

def card_value_counts(cards): 
    return dict(Counter(card_values(cards)))

def high_card(cards):
    return max(card_values(cards))

def is_pair(cards):
    return 2 in set(card_value_counts(cards).values())

def is_two_pair(cards):
    counts = card_value_counts(cards)
    return Counter(counts.values())[2] == 2

def highest_pair_value(cards):
    pairs = [ v for (v, c) in card_value_counts(cards).iteritems() if c == 2 ]
    return max(pairs) if pairs else None

def is_trips(cards):
    return 3 in set(card_value_counts(cards).values())

def trips_value(cards):
    trips = [ v for (v, c) in card_value_counts(cards).iteritems() if c == 3 ]
    return max(trips) if trips else None

def is_consecutive(l): 
    return all([ l[i] + 1 == l[i+1] for i in range(len(l)-1)])

def is_straight(cards):
    card_vals = card_values(cards)
    return is_consecutive(sorted(card_vals)) or is_consecutive(sorted(aces_as_low(card_vals)))

def is_flush(cards):
    return len(set([ card.suit(c) for c in cards ])) == 1

def is_full_house(cards):
    return set(card_value_counts(cards).values()) == {2, 3}

def is_quads(cards):
    return 4 in set(card_value_counts(cards).values())

def is_straight_flush(cards): 
    return is_flush(cards) and is_straight(cards)

def is_royal_flush(cards):
    return is_straight_flush(cards) and min(card_values(cards)) == 10

Hand = IntEnum('Hand', 'Nothing Pair TwoPair Trips Straight Flush FullHouse Quads StraightFlush RoyalFlush')

def classify_hand(cards):
    def any_length(cards):
        if is_trips(cards): return Hand.Trips
        elif is_two_pair(cards): return Hand.TwoPair
        elif is_pair(cards): return Hand.Pair
        else: return Hand.Nothing
    if len(cards) == 5:
        if is_royal_flush(cards): return Hand.RoyalFlush
        elif is_straight_flush(cards): return Hand.StraightFlush
        elif is_quads(cards): return Hand.Quads
        elif is_full_house(cards): return Hand.FullHouse
        elif is_flush(cards): return Hand.Flush
        elif is_straight(cards): return Hand.Straight
        else: return any_length(cards)
    else:
        return any_length(cards)

def test():
    # CR mrussell: try out unittest
    full_house = ['9h','9d','9c', '8d', '8c']
    two_pair = ['9h','9d','11c', '8d', '8c']
    print "is_pair:", is_pair(['9h','9d','9c', '8d', '8c'])
    print "is_two_pair:", is_two_pair(full_house) # is false - should I change that?
    print "is_two_pair:", is_two_pair(two_pair) # is false - should I change that?
    print "hand:", classify_hand(full_house)
    print "hand:", classify_hand(two_pair)
    print "is_trips:", is_trips(['9h','9d','9c', '8d', '8c'])
    print "is_straight:", is_straight(['9h', '10h', '11h'])
    print "is_straight:", is_straight(['13h', '12h', '1h'])
    print "is_full_house:", is_full_house(['9h','9d','9c', '8d', '8c'])
    print "is_full_house:", is_full_house(['10h','9d','9c', '8d', '8c'])
    print "is_royal_flush:", is_royal_flush(['10h','11h','12h', '13h', '1h'])

test()

bottom_scores = { 
    Hand.RoyalFlush : 25,
    Hand.StraightFlush : 15,
    Hand.Quads : 10,
    Hand.FullHouse : 6,
    Hand.Flush : 4,
    Hand.Straight : 2,
}

middle_scores = { 
    Hand.RoyalFlush : 50,
    Hand.StraightFlush : 30,
    Hand.Quads : 20,
    Hand.FullHouse : 12,
    Hand.Flush : 8,
    Hand.Straight : 4,
    Hand.Trips : 2,
}

def top_trip_scores(cards):
    # 2 = 10 and it goes up by one from there 
    return 8 + trips_value(cards)

def top_pair_scores(cards):
    # 6 = 1 and it goes up by one from there 
    return max(0, highest_pair_value(cards) - 5)
    
top_scores = { 
    Hand.Trips : lambda cards: top_trip_scores(cards),
    Hand.Pair : lambda cards: top_pair_scores(cards),
}

def score_simple(cards, score_map):
    hand = classify_hand(cards)
    return score_map[hand] if hand in score_map else 0

def score_bottom(cards): return score_simple(cards, bottom_scores)
def score_middle(cards): return score_simple(cards, middle_scores)
def score_top(cards): 
    hand = classify_hand(cards)
    return top_scores[hand](cards) if hand in top_scores else 0

score_by_level = { 
    play.Level.bottom : score_bottom,
    play.Level.middle : score_middle,
    play.Level.top : score_top,
}

def score(cards, level): return score_by_level[level](cards)


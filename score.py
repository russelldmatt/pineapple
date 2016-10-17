from collections import Counter
from level import Level
import card
from enum import IntEnum

def aces_as_low(card_values):
    return [ 1 if v == 14 else v for v in card_values ]

def card_values(cards): 
    return [ card.value(c) for c in cards ]

def sorted_card_values_highest_first(cards):
    return sorted(card_values(cards), reverse = True)

def card_value_counts(cards): 
    return dict(Counter(card_values(cards)))

def high_card(cards):
    return max(card_values(cards))

def is_pair(cards):
    return 2 in set(card_value_counts(cards).values())

def is_two_pair(cards):
    counts = card_value_counts(cards)
    return Counter(counts.values())[2] == 2

def sorted_pair_values_highest_first(cards):
    return sorted([ v for (v, c) in card_value_counts(cards).iteritems() if c == 2 ], reverse = True)

def highest_pair_value(cards):
    pairs = sorted_pair_values_highest_first(cards)
    return pairs[0] if pairs else None

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

def quads_value(cards):
    quads = [ v for (v, c) in card_value_counts(cards).iteritems() if c == 4 ]
    return max(quads) if quads else None

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

tie_breaker_value_functions = {
    Hand.Nothing       : [sorted_card_values_highest_first],
    Hand.Pair          : [highest_pair_value, sorted_card_values_highest_first],
    Hand.TwoPair       : [sorted_pair_values_highest_first, sorted_card_values_highest_first],
    Hand.Trips         : [trips_value, sorted_card_values_highest_first],
    Hand.Straight      : [sorted_card_values_highest_first],
    Hand.Flush         : [sorted_card_values_highest_first],
    Hand.FullHouse     : [trips_value, highest_pair_value],
    Hand.Quads         : [quads_value, sorted_card_values_highest_first],
    Hand.StraightFlush : [sorted_card_values_highest_first],
    Hand.RoyalFlush    : [sorted_card_values_highest_first],
}

def compare_hands_with_fun(cards1, cards2, value_fun):
    cards1_value = value_fun(cards1) 
    cards2_value = value_fun(cards2) 
    if cards1_value > cards2_value: 
        return 1
    elif cards2_value > cards1_value: 
        return -1
    else: 
        return 0

def compare_hands_waterfall(cards1, cards2, value_functions):
    if len(value_functions) == 0: 
        return 0
    else:
        return (compare_hands_with_fun(cards1, cards2, value_functions[0]) 
                or compare_hands_waterfall(cards1, cards2, value_functions[1:])
        )

def compare_hands(cards1, cards2): 
    hand1 = classify_hand(cards1)
    hand2 = classify_hand(cards2)
    if hand1 > hand2: 
        return 1
    elif hand2 > hand1:
        return -1
    elif hand1 == hand2: 
        tie_breakers = tie_breaker_value_functions[hand1]
        return compare_hands_waterfall(cards1, cards2, tie_breakers)
    else: 
        assert(False)

def hand_is_better(cards, than):
    return compare_hands(cards, than) > 0

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
    Hand.Trips : top_trip_scores,
    Hand.Pair : top_pair_scores,
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
    Level.bottom : score_bottom,
    Level.middle : score_middle,
    Level.top : score_top,
}

def score_level(cards, level): return score_by_level[level](cards)


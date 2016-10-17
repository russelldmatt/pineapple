import card
from level import Level
import score
import play
import fantasy_land

full_house = ['9h','9d','9c', '8d', '8c']
two_pair = ['9h','9d','11c', '8d', '8c']
worse_two_pair = ['9h','9d','11c', '7d', '7c']
pair_of_aces = ['14h','14d','11c', '7d', '6c']

def score_tests():
    # CR mrussell: try out unittest
    print "is_pair:", score.is_pair(['9h','9d','9c', '8d', '8c'])
    print "is_two_pair:", score.is_two_pair(full_house) # is false - should I change that?
    print "is_two_pair:", score.is_two_pair(two_pair) # is false - should I change that?
    print "hand:", score.classify_hand(full_house)
    print "hand:", score.classify_hand(two_pair)
    print "is_trips:", score.is_trips(['9h','9d','9c', '8d', '8c'])
    print "is_straight:", score.is_straight(['9h', '10h', '11h'])
    print "is_straight:", score.is_straight(['13h', '12h', '1h'])
    print "is_full_house:", score.is_full_house(['9h','9d','9c', '8d', '8c'])
    print "is_full_house:", score.is_full_house(['10h','9d','9c', '8d', '8c'])
    print "is_royal_flush:", score.is_royal_flush(['10h','11h','12h', '13h', '1h'])
    print "aces vs. worse_two_pair:", score.compare_hands(pair_of_aces, worse_two_pair)
    print "worse_two_pair vs. aces:", score.compare_hands(worse_two_pair, pair_of_aces)
    print "two_pair vs. worse_two_pair:", score.compare_hands(two_pair, worse_two_pair)
    print "worse_two_pair vs. two_pair:", score.compare_hands(worse_two_pair, two_pair)

score_tests()

p = play.create(full_house, two_pair, two_pair)
print play.is_valid(p)

def test_fantasy_land():
    cards = card.n_random_cards(14)

    # override
    cards_human = ['As', 'Ah', 'Ad', 'Kh', 'Js', '10h', '9c', '9d', '8c', '7s', '7c', '6s', '4s', '4d'] 
    cards_human = ['Ah', 'Ad', 'Qh', 'Jd', '10c', '10d', '9s', '8d', '7h', '5s', '4c', '3c', '2s', '2d']

    cards = [ card.of_human(c) for c in cards_human ]

    print "Testing fantasy_land best play:"
    print cards
    (best_p, best_score) = fantasy_land.best_play(cards)
    print "Best play:"
    play.pp(best_p)
    print "Best score:", best_score

# test_fantasy_land()

import itertools
import card
import helpers as hlp

def possible_plays(cards):
    for (bottom, rest) in hlp.partition(cards, 5):
        for (middle, top) in hlp.partition(rest, 5):
            assert(len(top) == 3)
            yield (bottom, middle, top)

def first_n_chars(n):
    return [chr(x) for x in range(97,97+n) ]

cards = card.n_random_cards(13)
print cards

for (i, play) in enumerate(itertools.islice(possible_plays(cards), 10)):
    print "play", i
    (bottom, middle, top) = play
    print "bottom:", bottom
    print "middle:", middle
    print "top:", top

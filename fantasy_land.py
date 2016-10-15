import itertools
import random
import helpers as hlp

def possible_plays(cards):
    for (bottom, rest) in hlp.partition(cards, 5):
        for (middle, top) in hlp.partition(rest, 5):
            assert(len(top) == 3)
            yield (bottom, middle, top)

def convert_play((bottom, middle, top)):
    def c(l): return [ list(x) for x in l ]
    return (c(bottom), c(middle), c(top)) 

def first_n_chars(n):
    return [chr(x) for x in range(97,97+n) ]

card_numbers = range(1, 14)
suits = [ 'h', 'd', 's', 'c' ]
all_cards = [ (n, s) for n in card_numbers for s in suits ]

def shuffle(x): return random.sample(x, len(x))

cards = shuffle(all_cards)[:13]
print cards

for (i, play) in enumerate(itertools.islice(possible_plays(cards), 10)):
    print "play", i
    (bottom, middle, top) = convert_play(play)
    print "bottom:", bottom
    print "middle:", middle
    print "top:", top

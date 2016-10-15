import itertools
import card
import helpers as hlp
import play

def possible_plays(cards):
    for (bottom, rest) in hlp.partition(cards, 5):
        for (middle, rest) in hlp.partition(rest, 5):
            for (top, rest) in hlp.partition(rest, 3):
                assert(len(rest) == 1)
                yield (bottom, middle, top)

def first_n_chars(n):
    return [chr(x) for x in range(97,97+n) ]

def best_play(cards, verbose = False):
    best_p = None
    best_score = -1
    num_play_evaluated = 0
    for p in possible_plays(cards):
        num_play_evaluated += 1
        (bottom, middle, top) = p
        p = play.create(bottom, middle, top)
        score = play.score_play(p)
        if score > best_score:
            best_p = p
            best_score = score
            if verbose:
                print "new best play:"
                play.pp(best_p)
                print "new best score:", best_score
    if verbose:
        print "Results:"
        print "Num plays evaluated:", num_play_evaluated
        print "best play:"
        play.pp(best_p)
        print "best score:", best_score
    return (best_p, best_score)


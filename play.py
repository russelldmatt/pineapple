from enum import Enum
from level import Level
import score

# play is a map from level -> cards
def create(bottom, middle, top):
    return { 
        Level.bottom : bottom,
        Level.middle : middle,
        Level.top : top,
    }
         
def is_valid(p):
    # from https://www.pokernews.com/poker-rules/chinese-poker.htm:
    # There is a strict rule that the bottom hand must be *at least as
    # good* as the middle hand, and that the middle hand must be *at
    # least as good* as the top hand
    return (score.compare_hands(p[Level.bottom], p[Level.middle]) >= 0
            and score.compare_hands(p[Level.middle], p[Level.top]) >= 0
    )

def score_play(p):
    # CR mrussell: valuing fantasy land @ 0
    return sum([score.score_level(cards, level) for (level, cards) in p.iteritems()]) if is_valid(p) else 0

def pp(p):
    """pretty print"""
    for level in [Level.top, Level.middle, Level.bottom]:
        print level, ":", p[level]

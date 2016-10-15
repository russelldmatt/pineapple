import random

def shuffle(x): return random.sample(x, len(x))

card_numbers = range(2, 15) # aces as high by default
suits = [ 'h', 'd', 's', 'c' ]
all_cards = [ str(n) + s for n in card_numbers for s in suits ]

def n_random_cards(n):
    """Returns n random cards"""
    return shuffle(all_cards)[:n]

def suit(card): return card[-1]
def value(card): return int(card[:-1])
    

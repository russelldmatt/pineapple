import random

def shuffle(x): return random.sample(x, len(x))

card_numbers = range(2, 15) # aces as high by default
suits = [ 'h', 'd', 's', 'c' ]

def create(value, suit): return str(value) + suit

all_cards = [ create(n, s) for n in card_numbers for s in suits ]

def n_random_cards(n):
    """Returns n random cards"""
    return shuffle(all_cards)[:n]

def suit(card): return card[-1]
def value(card): return int(card[:-1])
    
class InvalidCard(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def is_valid(card):
    return suit(card) in suits and value(card) >= 2 and value(card) <= 14

human_map = {
    'A' : 14,
    'K' : 13,
    'Q' : 12,
    'J' : 11,
}

def of_human_raw(card):
    first_char = card[0]
    if first_char.isalpha():
        if first_char not in human_map:
            raise InvalidCard(card)
        else:
            return create(human_map[first_char], suit(card))
    else:
        return card

def of_human(card):
    card = of_human_raw(card)
    if is_valid(card):
        return card
    else: 
        raise InvalidCard(card)

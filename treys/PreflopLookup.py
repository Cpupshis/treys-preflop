from collections.abc import Iterator
import itertools
from typing import Sequence

from .card import Card

class LookupTable:

    TWO_CARD_MAX_PAIR_HIGH: int = 8
    TWO_CARD_MAX_DRAW_SUIT_HIGH: int = 28
    TWO_CARD_MAX_ACE_SUIT: int = 4
    TWO_CARD_MAX_PAIR_LOW: int = 5
    TWO_CARD_MAX_DRAW_OFF_HIGH: int = 28
    TWO_CARD_MAX_ACE_OFF: int = 4
    TWO_CARD_MAX_DRAW_SUIT_LOW: int = 18
    TWO_CARD_MAX_SUIT: int = 28
    TWO_CARD_MAX_DRAW_OFF_LOW: int = 18
    TWO_CARD_MAX_OFF: int = 28

    TWO_CARD_MAX_TO_RANK: dict[int, int] = {
        TWO_CARD_MAX_PAIR_HIGH: 0,
        TWO_CARD_MAX_DRAW_SUIT_HIGH: 1,
        TWO_CARD_MAX_ACE_SUIT: 2,
        TWO_CARD_MAX_PAIR_LOW: 3,
        TWO_CARD_MAX_DRAW_OFF_HIGH: 4,
        TWO_CARD_MAX_ACE_OFF: 5,
        TWO_CARD_MAX_DRAW_SUIT_LOW: 6,
        TWO_CARD_MAX_SUIT: 7,
        TWO_CARD_MAX_DRAW_OFF_LOW: 8,
        TWO_CARD_MAX_OFF: 9
    }

    def __init__(self) -> None:

        self.pair_lookup: dict[int,int] = {}
        self.suited_lookup: dict[int,int] = {}
        self.offsuit_lookup: dict[int,int] = {}

        self.pairs()
        # self.suits()
        # self.offsuits()

    def pairs(self) -> None:
        rank = 1
        for highpair in range(LookupTable.TWO_CARD_MAX_PAIR_HIGH):
            for s in itertools.combinations(Card.CHAR_SUIT_TO_INT_SUIT,2):
                hand = []
                suit = Card.CHAR_SUIT_TO_INT_SUIT[s[0]]
                c1 = (
                        (rank << 16) |
                        (suit <<16) |
                        (Card.INT_RANKS[-rank] << 12) |
                        (Card.PRIMES[-rank])
                      )
                suit = Card.CHAR_SUIT_TO_INT_SUIT[s[1]]
                c2 =  (
                        (rank << 16) |
                        (suit <<16) |
                        (Card.INT_RANKS[-rank] << 12) |
                        (Card.PRIMES[-rank])
                      )
                hand.append(c1)
                hand.append(c2)
                self.pair_lookup[Card.prime_product_from_hand(hand)]=rank
            rank += 1

        #low pairs
        rank = sum(list(LookupTable.TWO_CARD_MAX_TO_RANK.keys())[:LookupTable.TWO_CARD_MAX_TO_RANK[LookupTable.TWO_CARD_MAX_PAIR_LOW]])
        for lowpair in range(LookupTable.TWO_CARD_MAX_PAIR_LOW):
            self.pair_lookup[Card.PRIMES[4-lowpair]**2] = rank
            rank += 1

    def suits(self):
        rank = sum(list(LookupTable.TWO_CARD_MAX_TO_RANK.keys())[:LookupTable.TWO_CARD_MAX_TO_RANK[LookupTable.TWO_CARD_MAX_DRAW_SUIT_HIGH]])
        for drawhighS in range(LookupTable.TWO_CARD_MAX_DRAW_SUIT_HIGH):
            for suit,idx in Card.CHAR_SUIT_TO_INT_SUIT:

from collections.abc import Iterator
import itertools
from typing import Sequence

from .card import Card

class LookupTable:

    TWO_CARD_MAX_PAIR_HIGH: int = 8
    TWO_CARD_MAX_DRAW_HIGH_SUIT: int = 14 + TWO_CARD_MAX_PAIR_HIGH
    TWO_CARD_MAX_ACE_DRAW_SUIT: int = 2 + TWO_CARD_MAX_DRAW_HIGH_SUIT
    TWO_CARD_MAX_ACE_SUIT: int = 6 + TWO_CARD_MAX_ACE_DRAW_SUIT
    TWO_CARD_MAX_PAIR_MID: int = 3 + TWO_CARD_MAX_ACE_SUIT
    TWO_CARD_MAX_DRAW_HIGH_OFF: int = 14 + TWO_CARD_MAX_PAIR_MID
    TWO_CARD_MAX_ACE_DRAW_OFF: int = 2 + TWO_CARD_MAX_DRAW_HIGH_OFF
    TWO_CARD_MAX_PAIR_LOW: int = 2 + TWO_CARD_MAX_ACE_DRAW_OFF
    TWO_CARD_MAX_ACE_OFF: int = 6 + TWO_CARD_MAX_PAIR_LOW
    TWO_CARD_MAX_SUIT_HIGH: int = 13 + TWO_CARD_MAX_ACE_OFF
    TWO_CARD_MAX_DRAW_SUIT_MID: int = 17 + TWO_CARD_MAX_SUIT_HIGH
    TWO_CARD_MAX_OFF_HIGH: int = 15 + TWO_CARD_MAX_DRAW_SUIT_MID
    TWO_CARD_MAX_SUIT_MID: int = 10 + TWO_CARD_MAX_OFF_HIGH
    TWO_CARD_MAX_OFF_MID: int = 10 + TWO_CARD_MAX_SUIT_MID
    TWO_CARD_MAX_DRAW_OFF_MID: int = 15 + TWO_CARD_MAX_OFF_MID
    TWO_CARD_MAX_SUIT_LOW: int = 10 + TWO_CARD_MAX_DRAW_OFF_MID
    TWO_CARD_MAX_DRAW_SUIT_LOW: int = 6 + TWO_CARD_MAX_SUIT_LOW
    TWO_CARD_MAX_OFF_LOW: int = 10 + TWO_CARD_MAX_DRAW_SUIT_LOW
    TWO_CARD_MAX_DRAW_OFF_LOW: int = 6 + TWO_CARD_MAX_OFF_LOW

    # TWO_CARD_MAX_TO_RANK: dict[int, int] = {
    #     TWO_CARD_MAX_PAIR_HIGH: 0,
    #     TWO_CARD_MAX_DRAW_SUIT_HIGH: 1,
    #     TWO_CARD_MAX_ACE_SUIT: 2,
    #     TWO_CARD_MAX_PAIR_LOW: 3,
    #     TWO_CARD_MAX_DRAW_OFF_HIGH: 4,
    #     TWO_CARD_MAX_ACE_OFF: 5,
    #     TWO_CARD_MAX_DRAW_SUIT_MID: 6,
    #     TWO_CARD_MAX_SUIT: 7,
    #     TWO_CARD_MAX_DRAW_OFF_MID: 8,
    #     TWO_CARD_MAX_OFF: 9
    # }

    def __init__(self) -> None:

        self.pair_lookup: dict[int,int] = {}
        self.suited_lookup: dict[int,int] = {}
        self.offsuit_lookup: dict[int,int] = {}

        # self.pairs()
        # self.highCards()
        # self.draws()
        # self.midLow()

    def pairs(self) -> None:

        # high pairs A-7
        rank = 1
        lst_num = [-(i+1) for i in range(13)]
        for i in lst_num:
            self.pair_lookup[Card.PRIMES[i]**2]  = rank
            rank += 1
        del lst_num[:8]

        #mid pairs 6-4
        rank = LookupTable.TWO_CARD_MAX_ACE_SUIT + 1
        for i in lst_num[:3]:
            self.pair_lookup[Card.PRIMES[i]**2] = rank
            rank += 1
        del lst_num[:3]

        # low pairs 3-2
        rank = LookupTable.TWO_CARD_MAX_ACE_DRAW_OFF + 1
        for i in lst_num:
            self.pair_lookup[Card.PRIMES[i]**2] = rank
            rank +=1
        del lst_num
    def aces(self) -> None:

        # A-9
        suited_rank = LookupTable.TWO_CARD_MAX_PAIR_HIGH + 1
        offsuit_rank = LookupTable.TWO_CARD_MAX_PAIR_MID + 1
        lst_num = [-(i+1) for i in range(13)]
        for i,j in itertools.combinations(lst_num[:6],2):
            h = [Card.PRIMES[i],Card.PRIMES[j]]
            if Card.prime_product_from_hand(h) != 779:
                self.suited_lookup[Card.prime_product_from_hand(h)] = suited_rank
                self.offsuit_lookup[Card.prime_product_from_hand(h)] = offsuit_rank
                suited_rank += 1
                offsuit_rank += 1
        del lst_num[:5]
        print(self.suited_lookup)
        # A5, A4
        for i in lst_num[4:6]:
            h = [Card.PRIMES[-1],Card.PRIMES[i]]
            self.suited_lookup[Card.prime_product_from_hand(h)] = suited_rank
            self.offsuit_lookup[Card.prime_product_from_hand(h)] = offsuit_rank
            suited_rank += 1
            offsuit_rank += 1
        del lst_num[4:6]
        print(self.suited_lookup)

        # rest of aces
        offsuit_rank = LookupTable.TWO_CARD_MAX_PAIR_LOW + 1
        for i in lst_num:
            h = [Card.PRIMES[-1], Card.PRIMES[i]]
            self.suited_lookup[Card.prime_product_from_hand(h)] = suited_rank
            self.offsuit_lookup[Card.prime_product_from_hand(h)] = offsuit_rank
            suited_rank += 1
            offsuit_rank += 1
        print(self.suited_lookup)

        # rest 8s
        suited_rank = LookupTable.TWO_CARD_MAX_ACE_OFF + 1
        offsuit_rank = LookupTable.TWO_CARD_MAX_DRAW_SUIT_MID + 1
        lst_num = [-(i+2) for i in range(2)]
        for i in lst_num:
            h = [Card.PRIMES[-7], Card.PRIMES[i]]
            self.suited_lookup[Card.prime_product_from_hand(h)] = suited_rank
            self.offsuit_lookup[Card.prime_product_from_hand(h)] = offsuit_rank
            suited_rank += 1
            offsuit_rank += 1
        print(self.suited_lookup)

    def highCards(self):
        #high cards suited
        suited_rank = LookupTable.TWO_CARD_MAX_ACE_OFF + 3
        offsuit_rank = LookupTable.TWO_CARD_MAX_DRAW_SUIT_MID + 1
        low_num = [5,4,3,2,1]
        for high_iter in range(4):
            for low_iter in low_num:
                h = [Card.PRIMES[-(2+high_iter)],Card.PRIMES[low_iter]]
                if Card.prime_product_from_hand(h) != 299 and Card.prime_product_from_hand(h) != 247:
                    self.suited_lookup[Card.prime_product_from_hand(h)] = suited_rank
                    suited_rank += 1
            del low_num[-1]

        low_lst = [-7,-8,-9,-10,-11,-12]
        high_lst = [-2,-3,-4,-5,-6]
        for low_iter in low_lst:
            if low_iter <= -9:
                del high_lst[-1]
            for high_iter in high_lst:
                h = [Card.PRIMES[high_iter],Card.PRIMES[low_iter]]
                self.offsuit_lookup[Card.prime_product_from_hand(h)] = offsuit_rank
                offsuit_rank += 1

    def draws(self):

        # straight draws mid (adj./semi-adj.)
        suited_rank = LookupTable.TWO_CARD_MAX_SUIT_HIGH + 1
        offsuit_rank = LookupTable.TWO_CARD_MAX_OFF_MID
        low_num = [-7,-8,-9,-10,-11]
        high_iter = 0
        for lowPrime in low_num:
            for highPrime in range(3):
                h=[Card.PRIMES[-4-highPrime-high_iter], Card.PRIMES[lowPrime]]
                self.suited_lookup[Card.prime_product_from_hand(h)] = suited_rank
                self.offsuit_lookup[Card.prime_product_from_hand(h)] = offsuit_rank
                suited_rank += 1
                offsuit_rank += 1
            high_iter += 1
        #low draw
        suited_rank = LookupTable.TWO_CARD_MAX_SUIT_LOW + 1
        low_num = [1,0]
        high_iter = 0
        for lowPrime in low_num:
            for highPrime in range(3):
                h = [Card.PRIMES[4 - highPrime - high_iter], Card.PRIMES[lowPrime]]
                self.suited_lookup[Card.prime_product_from_hand(h)] = suited_rank
                self.offsuit_lookup[Card.prime_product_from_hand(h)] = offsuit_rank
                suited_rank += 1
                offsuit_rank += 1
            high_iter += 1

    def midLow(self):

        #mid cards
        suited_rank = LookupTable.TWO_CARD_MAX_OFF_MID - 1
        offsuit_rank = LookupTable.TWO_CARD_MAX_DRAW_OFF_MID - 1
        high_lst = [-5,-4,-3,-2]
        low_lst = [i for i in range(4)]
        for high_iter in high_lst:
            for low_iter in low_lst:
                print(low_iter)
                h=[Card.PRIMES[high_iter], Card.PRIMES[low_iter]]
                self.suited_lookup[Card.prime_product_from_hand(h)] = suited_rank
                self.offsuit_lookup[Card.prime_product_from_hand(h)] = offsuit_rank
                suited_rank -= 1
                offsuit_rank -= 1
            del low_lst[-1]

        #low cards
        suited_rank = LookupTable.TWO_CARD_MAX_DRAW_OFF_MID + 1
        offsuit_rank = LookupTable.TWO_CARD_MAX_DRAW_SUIT_LOW + 1
        high_lst = [-6,-7,-8,-9]
        low_lst = [3,2,1,0]
        for high_iter in high_lst:
            for low_iter in low_lst:
                h=[Card.PRIMES[high_iter], Card.PRIMES[low_iter]]
                self.suited_lookup[Card.prime_product_from_hand(h)] = suited_rank
                self.offsuit_lookup[Card.prime_product_from_hand(h)] = offsuit_rank
                suited_rank += 1
                offsuit_rank += 1
            del low_lst[0]
    def checkRanks(self) -> list:
        row = Card.PRIMES
        column = Card.PRIMES
        row = row[::-1]
        column = column[::-1]
        matrix = []
        for column_iter in column:
            pair_switch = False
            for row_iter in row:
                if (row_iter*column_iter) in list(self.pair_lookup.keys()):
                    matrix.append(self.pair_lookup[(column_iter*row_iter)])
                    pair_switch = True
                elif (row_iter*column_iter) in list(self.suited_lookup.keys()) and not pair_switch:
                    matrix.append(self.suited_lookup[(column_iter*row_iter)])
                elif (row_iter*column_iter) in list(self.offsuit_lookup.keys()) and pair_switch:
                    matrix.append(self.offsuit_lookup[(column_iter * row_iter)])

        return matrix

    def checkLookup(self):
        for i in list(self.pair_lookup.keys()):
            for j in list(self.suited_lookup.keys()):
                if i==j:
                    print(i)
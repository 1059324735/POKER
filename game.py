import pandas as pd
import numpy as np
import logging
import random
import time
import collections
from random import shuffle
from random import choice
from itertools import combinations

Card = collections.namedtuple('Card',['rank','suit'])
Initial_Actions = ['Small Blind', 'Big Blind', 'Fold', 'Raise', 'Call','Check','Re-raise']
usual_Actions = ['Fold', 'Raise', 'Call','Check','Re-raise']
After_raise = ['Fold','Call','Re-raise']
chips = [5, 10, 20, 50, 100]

#概率表为，1326种起手牌组合+81144000种后面4轮的可能。（稳健型，考虑后面的概率，variance小）（另一种为variance大，只是看概率）

def Calc_winrate(hand,showed):#计算胜率
    deck = Deck()
    win = 0 
    Cards = hand+showed
    for i in Cards:
        deck.__deleteitem__(i)
    possible_other_hand = list(combinations(deck, 2))
    
    for i in possible_other_hand:
        Possible_Cards = showed+i
        result = Winner(Cards,Possible_Cards)
        if result == 0 or result == 2:
            win+=1
    return win/len(possible_other_hand)
    
    
def Find_max_rank(ranks):#寻找最大面值
    maxrank = ranks[0][0]
    maxrankind = 0
    feed = 0
    for i in range(len(ranks)-1):
        
        feed = distinguish(maxrank, ranks[i+1][0])
        if feed == 1:
            maxrank = ranks[i+1][0]
            maxrankind = i+1
    return maxrank, maxrankind
        

def Same_value(cards1,cards2,typ):#同样牌型比较大小
    winner = 0
    ranks1, suits1 = divide_rank_suit(cards1)
    ranks2, suits2 = divide_rank_suit(cards2)
    if typ == '两对':
        winner = distinguish(ranks1[0][0],ranks2[0][0])
        if winner == 2:
            temp1 = distinguish(ranks1[1][0],ranks2[1][0])
            if temp1 == 2:
                maxrank1, maxrankind1 = Find_max_rank(ranks1[2:])
                maxrank2, maxrankind2 = Find_max_rank(ranks2[2:])
                return distinguish(maxrank1,maxrank2)
            else:
                return temp1
        else:
            return winner
    elif typ == '葫芦':
        winner = distinguish(ranks1[0][0],ranks2[0][0])
        if winner == 2:
            return distinguish(ranks1[1][0],ranks2[1][0])
        else:
            return winner
    elif typ == '高牌':
        maxrank1, maxrankind1 = Find_max_rank(ranks1)
        maxrank2, maxrankind2 = Find_max_rank(ranks2)
        winner = distinguish(maxrank1,maxrank2)
        return winner
    elif typ == '一对':
        winner = distinguish(ranks1[0][0],ranks2[0][0])
        if winner == 2:
            maxrank1, maxrankind1 = Find_max_rank(ranks1[1:])
            maxrank2, maxrankind2 = Find_max_rank(ranks2[1:])
            temp1 = distinguish(maxrank1,maxrank2)
            if temp1 == 2:
                temprank1 = ranks1[1:]
                temprank1.pop(maxrankind1)
                temprank2 = ranks2[1:]
                temprank2.pop(maxrankind2)
                maxrank11, maxrankind11 = Find_max_rank(temprank1)
                maxrank22, maxrankind22 = Find_max_rank(temprank2)
                temp2 = distinguish(maxrank11,maxrank22)
                if temp2 == 2:
                    temprank1.pop(maxrankind11)
                    temprank2.pop(maxrankind22)
                    maxrank111, maxrankind111 = Find_max_rank(temprank1)
                    maxrank222, maxrankind222 = Find_max_rank(temprank2)
                    return distinguish(maxrank111,maxrank222)
            else:
                return temp1
        else:
            return winner
    elif typ == '四条':
        winner = distinguish(ranks1[0][0],ranks2[0][0])
        if winner == 2:
            maxrank1, maxrankind1 = Find_max_rank(ranks1[1:])
            maxrank2, maxrankind2 = Find_max_rank(ranks2[1:])
            return distinguish(maxrank11,maxrank22)
        else:
            return winner
    elif typ == '三条':
        winner = distinguish(ranks1[0][0],ranks2[0][0])
        if winner == 2:
            maxrank1, maxrankind1 = Find_max_rank(ranks1[1:])
            maxrank2, maxrankind2 = Find_max_rank(ranks2[1:])
            temp1 = distinguish(maxrank1,maxrank2)
            if temp1 == 2:
                temprank1 = ranks1[1:]
                temprank1.pop(maxrankind1)
                temprank2 = ranks2[1:]
                temprank2.pop(maxrankind2)
                maxrank11, maxrankind11 = Find_max_rank(temprank1)
                maxrank22, maxrankind22 = Find_max_rank(temprank2)
                return distinguish(maxrank11,maxrank22)
            else:
                return temp1
        else:
            return winner
    elif typ == '同花':
        maxrank1, maxrankind1 = Find_max_rank(ranks1)
        maxrank2, maxrankind2 = Find_max_rank(ranks2)
        winner = distinguish(maxrank1,maxrank2)
        return winner
    else:
        tier1 = Is_row(cards1)
        tier2 = Is_row(cards2)
        if tier1 < tier2:
            return 0
        elif tier1 == tier2:
            return 2
        else:
            return 1
    
    
def Is_row(cards):#分辨是不是顺子
    cards_rank = []
    tier = 0
    for i in range(len(cards)):
        cards_rank.append(cards[i].rank)
    a1 = set(['A','K','Q','J','10'])
    a2 = set(['K','Q','J','10','9'])
    a3 = set(['Q','J','10','9','8'])
    a4 = set(['J','10','9','8','7'])
    a5 = set(['10','9','8','7','6'])
    a6 = set(['9','8','7','6','5'])
    a7 = set(['8','7','6','5','4'])
    a8 = set(['7','6','5','4','3'])
    a9 = set(['6','5','4','3','2'])
    a10 = set(['A','2','3','4','5'])
    b = set(cards_rank)
    if a1.difference(b) == set():
        tier = 1
    elif a2.difference(b) == set():
        tier = 2
    elif a3.difference(b) == set():
        tier = 3
    elif a4.difference(b) == set():
        tier = 4
    elif a5.difference(b) == set():
        tier = 5
    elif a6.difference(b) == set():
        tier = 6
    elif a7.difference(b) == set():
        tier = 7
    elif a8.difference(b) == set():
        tier = 8
    elif a9.difference(b) == set():
        tier = 9
    elif a10.difference(b) == set():
        tier = 10
    return tier
    
def distinguish(rank1,rank2):#分辨哪个面值大
    value1 = 0
    value2 = 0
    if rank1 == 'A':
        value1 = 14
    elif rank1 == 'K':
        value1 = 13
    elif rank1 == 'Q':
        value1 = 12
    elif rank1 == 'J':
        value1 == 11
    else:
        value1 == int(rank1)
#分别给两个牌赋值
    if rank2 == 'A':
        value2 = 14
    elif rank2 == 'K':
        value2 = 13
    elif rank2 == 'Q':
        value2 = 12
    elif rank2 == 'J':
        value2 == 11
    else:
        value2 == int(rank2)
    if value1 > value2:
        return 0
    elif value2 > value1:
        return 1
    elif value1 == value2:
        return 2
def divide_rank_suit(Cards):
    rank_list = []
    suit_list = []
    ranks = []
    suits = []
    
    typ = ''
    row_tier = Is_row(Cards)
    for i in Cards:
        rank_list.append(i.rank)
        suit_list.append(i.suit)
    rankset = set(rank_list)
    suitset = set(suit_list)
    for rank in rankset:
        ranks.append([rank,rank_list.count(rank)])
    for suit in suitset:
        suits.append([suit,suit_list.count(suit)])
    ranks = sorted(ranks, key = lambda x:x[1],reverse = True)
    suits = sorted(suits, key = lambda x:x[1],reverse = True)
    return ranks, suits
def Recog_type_value(Cards):#给卡组赋值方便比大小,对子1.5,三条3.5,顺子4,同花4.5,四条5.5。例如葫芦就是三条+一对儿,5分
    ranks, suits = divide_rank_suit(Cards)
    row_tier = Is_row(Cards)
    value = 0
    if ranks[0][1] == 4:
        value = 5.5
        typ = '四条'
    if ranks[0][1] == 3:
        value = 3.5
        typ = '三条'
        if ranks[1][1] == 2:
            value += 1.5
            typ = '葫芦'
    if ranks[0][1] == 2:
        value = 1.5
        typ = '一对'
        if ranks[1][1] == 2:
            value += 1.5
            typ = '两对'
    if row_tier > 0:
        value = 4
        typ = '顺子'
    if suits[0][1] >= 5:
        value += 4.5
        typ = '同花'
    if value == 8.5:
        typ = '同花顺'
    if value == 0:
        typ = '高牌'
    return value,typ
    
def Winner(Cards1, Cards2):#给出两组手牌+底牌的大小
    value1, typ1 = Recog_type_value(Cards1)
    value2, typ2 = Recog_type_value(Cards2)
    if value1 > value2:
        return 0
    elif value1 < value2:
        return 1
    elif value1 == value2:
        return Same_value(Cards1,Cards2,typ1)

class Deck():
    ranks = [str(n) for n in range(2,11)] + list('JQKA')
    suits = '黑桃 红桃 梅花 方片'.split()
    def __init__(self):
        self.cards = [Card(rank,suit) for suit in self.suits 
                        for rank in self.ranks]
    def __len__(self):
        return len(self.cards)
    def __getitem__(self, position):
        return self.cards[position]
    def __setitem__(deck, position, card):
        deck.cards[position] = card
    def __deleteitem__(self, item):
        cards = []
        for card in self.cards:
            if item.suit != card.suit or item.rank != card.rank:
                cards.append(card)
        self.cards = cards
class Texas_Player:
    def __init__(self, chips = 10000):
        self._chips = chips
        self._cards = []
        self._winrate = 0
        self._expectation = 0
        self._single_cost = 0
        self._strategy = ''
    def change_chips(self,changing):
        self._chips += changing
    def get_card(self, card):
        self._cards.append(card)
    def Bet(self):
        self

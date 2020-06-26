import numpy as np
import pandas as pd
import random
# import matplotlib.pyplot as plt
# import seaborn as sns

# Create deck(s) (blackjack can be played w/ multiple decks)
def create_decks(num_decks, card_types):
    new_deck = []
    for i in range(num_decks):
        for j in range(4):
            new_deck.extend(card_types)
    random.shuffle(new_deck)
    return new_deck

# List out all permutations of ace values in the
# array sum_array.
# Ex: if you have 2 aces, there are 4 permutations:
#     [[1,1], [1,11], [11,1], [11,11]]
# Out of these permutations there are 3 unique sums: [2, 12, 22]
# Return only the valid ones so: [2, 12]
def get_ace_values(temp_list):
    sum_array = np.zeros((2**len(temp_list), len(temp_list)))
    # Get the permutations
    for i in range(len(temp_list)):
        n = len(temp_list) - i
        half_len = int(2**n * 0.5)
        for rep in range(int(sum_array.shape[0]/half_len/2)):
            sum_array[rep*2**n : rep*2**n+half_len, i] = 1
            sum_array[rep*2**n+half_len : rep*2**n+half_len*2, i] = 11
    # Only return values that are valid (<=21)
    return list(set([int(s) for s in np.sum(sum_array, axis=1)
                     if s<=21]))

# Convert int to a list of lists
# Ex: if num_aces=2, the output should be [[1,11],[1,11]]
# helper function for the get_ace_values function
def ace_values(num_aces):
    temp = []
    for i in range(num_aces):
        temp.append([1,11])
    return get_ace_values(temp)

# Sum up value of hand
def sum_up(hand):
    aces = 0
    total = 0    
    for card in hand:
        if card != 'A':
            total += card
        else:
            aces += 1

    ace_value_list = ace_values(aces)
    final_totals = [i+total for i in ace_value_list if i+total<=21]
    
    if final_totals == []:
        return min(ace_value_list) + total
    else:
        return max(final_totals)


simulations = 20000
players = 1
num_decks = 1
card_types = ['A',2,3,4,5,6,7,8,9,10,10,10,10]
# 'J' 'Q' 'K' are all 10

dealer_card_feature = []
player_card_feature = []
player_results = []

# 1 = win 
# 0 = tie 
# -1 = loss

for stack in range(simulations):
    blackjack = set(['A',10])
    dealer_cards = create_decks(num_decks, card_types)
    # Once there are less than 20 cards left in the deck
    # move onto another simulation
    while len(dealer_cards) > 20:
        curr_player_results = np.zeros((1,players))
        
        dealer_hand = []
        player_hands = [[] for player in range(players)]
        # Deal FIRST card
        for player, hand in enumerate(player_hands):
            player_hands[player].append(dealer_cards.pop(0))
        dealer_hand.append(dealer_cards.pop(0))
        # Deal SECOND card
        for player, hand in enumerate(player_hands):
            player_hands[player].append(dealer_cards.pop(0))
        dealer_hand.append(dealer_cards.pop(0))

        # check for blackjack
        if set(dealer_hand) == blackjack:
            for player in range(players):
                if set(player_hands[player]) != blackjack:
                    curr_player_results[0,player] = -1
                else:
                    curr_player_results[0,player] = 0

        else:
            for player in range(players):
                if set(player_hands[player]) == blackjack:
                    curr_player_results[0,player] = 1
                else:
                    # Hit randomly so if its >= 0.5 player hits else stay
                    # Why do we make the player dumb? 
                    # We get to observe all kinds of situations from lucky
                    # to bonehead to big brain
                    while (random.random() >= 0.5) and \
                    (sum_up(player_hands[player]) <= 11):
                        player_hands[player].append(dealer_cards.pop(0))
                        if sum_up(player_hands[player]) > 21:
                            curr_player_results[0,player] = -1
                            break
                        
                    # This section is for smarter plays
                    # while sum_up(player_hands[player]) <= 11:
                    #     player_hands[player].append(dealer_cards.pop(0))
                    #     if sum_up(player_hands[player]) > 21:
                    #         curr_player_results[0,player] = -1
                    #         break
        
        # House has to hit if under 17
        while sum_up(dealer_hand) < 17:
            dealer_hand.append(dealer_cards.pop(0))

        # Compare dealer hand to players hand 
        if sum_up(dealer_hand) > 21:
            for player in range(players):
                if curr_player_results[0,player] != -1:
                    curr_player_results[0,player] = 1
        else:
            for player in range(players):
                if sum_up(player_hands[player]) > sum_up(dealer_hand):
                    if sum_up(player_hands[player]) <= 21:
                        curr_player_results[0,player] = 1
                elif sum_up(player_hands[player]) == sum_up(dealer_hand):
                    curr_player_results[0,player] = 0
                else:
                    curr_player_results[0,player] = -1

        # Track features
        dealer_card_feature.append(dealer_hand[0])
        player_card_feature.append(player_hands)
        player_results.append(list(curr_player_results[0]))


print(sum(pd.DataFrame(player_results)[0].value_counts()))

print(pd.DataFrame(player_results)[0].value_counts())
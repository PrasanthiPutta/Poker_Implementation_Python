#!/usr/bin/env python
# coding: utf-8

# In[1]:


# card.py
"""Card class that represents a playing card and its image file name."""

class Card:
    FACES = ['Ace', '2', '3', '4', '5', '6',
             '7', '8', '9', '10', 'Jack', 'Queen', 'King']
    SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']

    def __init__(self, face, suit):
        """Initialize a Card with a face and suit."""
        self._face = face
        self._suit = suit

    @property
    def face(self):
        """Return the Card's self._face value."""
        return self._face

    @property
    def suit(self):
        """Return the Card's self._suit value."""
        return self._suit

    @property
    def image_name(self):
        """Return the Card's image file name."""
        return str(self).replace(' ', '_') + '.png'

    def __repr__(self):
        """Return string representation for repr()."""
        return f"Card(face='{self.face}', suit='{self.suit}')"     

    def __str__(self):
        """Return string representation for str()."""
        return f'{self.face} of {self.suit}'

    def __format__(self, format):
        """Return formatted string representation."""
        return f'{str(self):{format}}'


# In[2]:


# deck.py
"""Deck class represents a deck of Cards."""
import random 

class DeckOfCards:
    NUMBER_OF_CARDS = 52  # constant number of Cards

    def __init__(self):
        """Initialize the deck."""
        self._current_card = 0
        self._deck = []

        for count in range(DeckOfCards.NUMBER_OF_CARDS):  
            self._deck.append(Card(Card.FACES[count % 13], Card.SUITS[count // 13]))

    def shuffle(self):
        """Shuffle deck."""
        self._current_card = 0
        random.shuffle(self._deck)    

    def deal_card(self):
        """Return one Card."""
        try:
            card = self._deck[self._current_card]
            self._current_card += 1
            return card
        except:
            return None  

    def __str__(self):
        """Return a string representation of the current _deck."""
        s = ''

        for index, card in enumerate(self._deck):
            s += f'{self._deck[index]:<19}'
            if (index + 1) % 4 == 0:
                s += '\n'
        
        return s


# In[3]:


import numpy as np

class Hand:
    NUM_OF_CARDS = 5
    HANDS = ['high card', 'pair', 'two pair', 'three of a kind', 'straight', 'flush', 'full house', 'four of a kind', 'straight flush']
    
    def __init__(self):
        self._hand = []
    
    #Distributes 5 cards from deck
    def deal_hand(self, deck):
        for num in range(self.NUM_OF_CARDS):
            self._hand.append(deck[num])
   
    #returns faces of every card in the hand 
    def get_faces(self):
        faces = []
        for num in range(self.NUM_OF_CARDS):
            faces.append(self._hand[num].face)
        return faces
    
    #returns suits of every card in the hand 
    def get_suits(self):
        suits = []
        for num in range(self.NUM_OF_CARDS):
            suits.append(self._hand[num].suit)
        return suits 
    
    #returns the hand after sorting the cards
    def sort_hand(self):
        return sorted(self._hand, key = lambda hand:hand.face)
    
    #returns true if the cards follows both flush and straight rules
    def is_straight_flush(self):     
        Flush = self.is_flush()
        straight = self.is_straight() 
        return (straight and Flush)
    
    #returns true if the faces of 4 cards are same and 1 is different 
    def is_four_of_a_kind(self):
        unique_faces = np.unique(self.get_faces())  
        count_unique_faces = []
        if(len(unique_faces)<=2):
            count_unique_faces = sorted(list(map(lambda x: self.get_faces().count(x), unique_faces)))
        
        Rule = [1,4]
        if(count_unique_faces):
            return np.array_equal(Rule, count_unique_faces)
        else:
            return False
        
    #returns true if the faces of 3 cards are same and the faces of remaining 2 cards are same
    def is_full_house(self):
        unique_faces = np.unique(self.get_faces())  
        count_unique_faces = []
        if(len(unique_faces)<=2):
            count_unique_faces = sorted(list(map(lambda x: self.get_faces().count(x), unique_faces)))     
        
        Rule = [2,3]
        if(count_unique_faces):
            return np.array_equal(Rule, count_unique_faces)
        else:
            return False
    
    #returns true if the suits of all cards are same
    def is_flush(self):
        unique_suits = np.unique(self.get_suits()) 
        return len(unique_suits)==1
    
    #returns true if the cards are sequential
    def is_straight(self): 
        Faces_dict = dict(enumerate(Card.FACES))
        Faces_sorted_list = list(map(lambda x:x[0],list(filter(lambda x: x[1] in self.get_faces(), Faces_dict.items()))))
        if max(Faces_sorted_list) == 12:
            Faces_dict[13]=Faces_dict[0]
            del Faces_dict[0]
        return all(np.diff(sorted(Faces_sorted_list)) == 1)
    
    #returns true if the faces of 3 cards are same and of other 2 cards are different
    def is_three_of_a_kind(self):
        unique_faces = np.unique(self.get_faces())  
        count_unique_faces = []
        if(len(unique_faces)<=3):
            count_unique_faces = sorted(list(map(lambda x: self.get_faces().count(x), unique_faces)))
        
        Rule = [1,1,3]
        if(count_unique_faces):
            return np.array_equal(Rule, count_unique_faces)
        else:
            return False
        
    #returns true if the faces of 2 cards are same and of other 2 cards are same
    def is_two_pair(self):
        unique_faces = np.unique(self.get_faces())  
        count_unique_faces = []
        if(len(unique_faces)<=3):
            count_unique_faces = sorted(list(map(lambda x: self.get_faces().count(x), unique_faces)))
        
        Rule = [1,2,2]
        if(count_unique_faces):
            return np.array_equal(Rule, count_unique_faces)
        else:
            return False    

    #returns true if the faces of 2 cards are same and of remaining 3 cards are different
    def is_pair(self):
        unique_faces = np.unique(self.get_faces())  
        count_unique_faces = []
        if(len(unique_faces)<=4):
            count_unique_faces = sorted(list(map(lambda x: self.get_faces().count(x), unique_faces)))
            
        Rule = [1,1,1,2]
        if(count_unique_faces):
            return np.array_equal(Rule, count_unique_faces)
        else:
            return False 

    #returns Hand after evaluating with the rules in an order of their priority and returns if the rule satisfies
    def evaluate_hand(self):
        hand_evaluation = {'straight flush':self.is_straight_flush(),
                           'four of a kind':self.is_four_of_a_kind(),
                           'full house':self.is_full_house(),
                           'flush':self.is_flush(),
                           'straight':self.is_straight(),
                           'three of a kind':self.is_three_of_a_kind(),
                           'two pair':self.is_two_pair(),
                           'pair':self.is_pair(),
                           'high card':True}
        for h_eval in hand_evaluation.keys():
            if(hand_evaluation[h_eval]):
                return h_eval
            
    #returns the strings of cards in the hand when requested to print the cards in the hand        
    def __str__(self):
        s = ''
        for num in range(self.NUM_OF_CARDS):
            s += f'{self._hand[num].face} of {self._hand[num].suit}'
            s += '\n'
        return s


# In[4]:


from matplotlib import animation
from IPython.display import HTML
import matplotlib
import matplotlib.pyplot as plt
import random
import seaborn as sns
import sys

matplotlib.rcParams['animation.embed_limit'] = 2**128

def update(deck_number, hands, hand_evaluation, frequencies):
    
    # Makes a deck and shuffle it
    deck = DeckOfCards()
    deck.shuffle()
    
    #For each deck evaluate 10 hands
    for hand in range(hands):
        hand = Hand()                      #Makes a hand
        hand.deal_hand(deck._deck)         #Deals to it
        hand.sort_hand()                   #Sorts it
        BEST_HAND_EVALUATION = hand.evaluate_hand()                         #Evaluates it
        frequencies[hand_evaluation.index(BEST_HAND_EVALUATION)] += 1       #Updates the frequency of hand occurrences
        
    plt.cla()
    axes = sns.barplot(x=hand_evaluation, y=frequencies, palette = 'bright')
    axes.set_xticklabels(axes.get_xticklabels(), rotation=45, ha='center')
    axes.set_title(f'Hand Frequencies for {sum(frequencies)} hands')
    axes.set(xlabel = 'Hand Value', ylabel='Frequency')
    axes.set_ylim(top=max(frequencies) * 1.10)
        
    # display frequency & percentage above each patch (bar)
    for bar, frequency in zip(axes.patches, frequencies):
        text_x = bar.get_x() + bar.get_width() / 2.0  
        text_y = bar.get_height() 
        text = f'{frequency:,}\n{frequency / sum(frequencies):.3%}'
        axes.text(text_x, text_y, text, ha='center', va='bottom')  
    
number_of_decks = 5999
hands_per_deck = 10

sns.set_style('whitegrid')
figure = plt.figure('Hand evaluation for poker game')
Hand_Evaluations = ['high card', 'pair', 'two pair', 'three of a kind', 'straight', 'flush', 'full house', 'four of a kind', 'straight flush']
frequencies = [0]*9

card_animation = animation.FuncAnimation(
    figure, update, repeat=False, frames=number_of_decks , interval=1,
    fargs=(hands_per_deck, Hand_Evaluations, frequencies))

HTML(card_animation.to_jshtml())


# In[5]:


print(f'Total hands: {(number_of_decks+1)*hands_per_deck}')
for hand_evaluation in Hand_Evaluations:
    print(f'{hand_evaluation:<20} : {frequencies[Hand_Evaluations.index(hand_evaluation)]:>10}:   {frequencies[Hand_Evaluations.index(hand_evaluation)]*100/sum(frequencies):.3f}%')


# ### Poker Implementation
# 
# #### Rules
# 
# * One Pair:
#     * Create an array of unique faces of cards using numpy array unique function.
#     * Now, Count the number of occurances of each element from unique faces array in the list of faces and sort it
#     * Initialize the rule = Rule = [1,1,1,2]
#     * Returns true if number of occurances of each element from unique faces array is equal with the Rule(using numpy array equal function) else return false
#   
# 
# * Two Pair:
#     * Create an array of unique faces of cards using numpy array unique function.
#     * Now, Count the number of occurances of each element from unique faces array in the list of faces and sort it
#     * Initialize the rule = Rule = [1,2,2]
#     * Returns true if number of occurances of each element from unique faces array is equal with the Rule(using numpy array equal function) else return false
# 
# 
# * Three of a kind:
#     * Create an array of unique faces of cards using numpy array unique function.
#     * Now, Count the number of occurances of each element from unique faces array in the list of faces and sort it
#     * Initialize the rule = Rule = [1,1,3]
#     * Returns true if number of occurances of each element from unique faces array is equal with the Rule(using numpy array equal function) else return false
#  
# 
# * Straight:
#     * Create a dictionary of Faces of all cards defined in class Card with its index element as key
#     * Get the list of keys for each face in the hand that matches with the dictionary of Faces
#     * If the maximum element of list of keys == 12 Then add the value 'Ace' for key 13 and delete key 0 
#     * Returns true if the difference between the each element is 1 else false 
#  
# 
# * Flush:
#     * Create an array of unique suits of cards using numpy array unique function.
#     * Returns true if length of unique suits = 1 else false
#  
# 
# * Full House:
#     * Create an array of unique faces of cards using numpy array unique function.
#     * Now, Count the number of occurances of each element from unique faces array in the list of faces and sort it
#     * Initialize the rule = Rule = [2,3]
#     * Returns true if number of occurances of each element from unique faces array is equal with the Rule(using numpy array equal function) else return false
#  
# 
# * Four of a kind:
#     * Create an array of unique faces of cards using numpy array unique function.
#     * Now, Count the number of occurances of each element from unique faces array in the list of faces and sort it
#     * Initialize the rule = Rule = [1,4]
#     * Returns true if number of occurances of each element from unique faces array is equal with the Rule(using numpy array equal function) else return false
#  
# 
# * Straight Flush:
#     * Returns true if the cards in hand satisfies both straight rule and flush rule else false
#  
# 
# * Evaluate Hand:
#     * Create a dictionary with key: Rule name and Value: Rule function call
#     * Return the key if Rule function call evaluates to true
#     * By default High Card rule is set to True and is evaluated only if other rules return false
#  
# 
# ### Law of large numbers
# 
# * According to the law, the average of the results obtained from a large number of trials should be close to the expected value and will tend to become closer to the expected value as more trials are performed
# * It guarantees the stable long-term results
# 
# Reference: https://en.wikipedia.org/wiki/Law_of_large_numbers
#  
# 
# ### Poker Implementation Successful at approximating the expected probabilities after a large number of samples (using the law of large numbers)
# 
#            | Hand           |   Expected   |    Obtained |
#            |----------------|--------------|-------------|
#            | High Hand      |   50.1177%   |    50.167%  |
#            | One pair       |   42.2569%   |    42.350%  |
#            | Two pair       |   4.7539%    |    4.067%   |
#            | Three of a kind|   2.1128%    |    1.817%   |
#            | Straight       |   0.3925%    |    1.200%   |
#            | Flush          |   0.1965%    |    0.217%   |
#            | Full house     |   0.1441%    |    0.150%   |
#            | Four of a kind |   0.0240%    |    0.033%   |
#            | Straight flush |   0.00139%   |    0.000%   |
#             
#             Successful = corr(Expected, Obtained) = 99.9%
#             
# Reference: https://en.wikipedia.org/wiki/Poker_probability#Frequency_of_5-card_poker_hands
# 

# In[ ]:





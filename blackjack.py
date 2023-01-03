'''
This is a Blackjack game made with python using OOP
'''
import os
import random

suits = {'Hearts','Spades','Diamonds','Clubs'}
ranks = {'Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Jack','Queen','King','Ace'}
values = {'Two':2,'Three':3,'Four':4,'Five':5,'Six':6,'Seven':7,'Eight':8,'Nine':9,
            'Ten':10,'Jack':10,'Queen':10,'King':10,'Ace':1}

class Card:
    '''
    This class is used to create cards
    '''
    def __init__(self,suit,rank):
        self.naipe = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return f"{self.rank} of {self.naipe}"

class Deck:
    '''
    This class is used to create deck of cards
    '''
    def __init__(self):
        self.all_cards=[]
        for suit in suits:
            for rank in ranks:
                self.all_cards.append(Card(suit,rank))
    def __str__(self):
        return f"A deck with {len(self.all_cards)} cards!"

    def shuffle(self):
        '''
        This method is used to shuffle the deck
        '''
        random.shuffle(self.all_cards)    
    def deal_one(self):
        '''
        This method is used to deal one card of the deck
        '''
        return self.all_cards.pop()

class Player:
    '''
    This class is used to handle player account, bets and current cards
    '''         
    def __init__(self,name,cash):
        self.name = name
        self.cash = cash
        self.initial_cash = cash
        self.cards = []
        self.win_count = 0
        self.busts_count = 0
        self.loses_count = 0
    def __str__(self):
        return f"The player {self.name} has ${self.cash}"

    def bet(self,value):
        '''
        This method is used to bet certain ammount of cash
        '''
        if self.cash < value:
            print(f"Not enought balance!")
            return 0
        else:
            self.cash -= value
            return value
    def win(self,value):
        '''
        This method update the player cash when the player wins
        '''
        self.cash+=value

    def hit(self,card):
        '''
        This method add a card to the player cards
        '''
        self.cards.append(card)
    
    def cards_clear(self):
        '''
        This method remove all the cards of the player hand
        '''
        self.cards.clear()
    
class Dealer:

    def __init__(self):
        self.name = 'Dealer'
        self.cards=[]
    
    def hit(self,card):
        '''
        This method add a card to the dealer cards
        '''
        self.cards.append(card)
    
    def clear(self):
        '''
        This method remove all the cards of the player hand
        '''
        self.cards.clear()

def show(p1,sum):
    '''
    This function show the cards of the current play and it's sum   
    '''
    print(f"{p1.name} hand: ")
    for card in p1.cards:
        print(card)
    print(f"The sum is: {sum}")

def check_win(p1:Player, player_sum:int, dealer_sum:int, bet:int):
    '''
    This function you checks win conditions and returns False if the game reach a win condition
    And True otherwise
    '''
    if player_sum == 21:
        print(f"You hit 21!")
        print(f"You win ${2*bet}")
        player.win(value=2*bet)
        player.win_count += 1
        return False
    if player_sum > 21:
        print("You Busted!")
        print(f"You lose your bet of ${bet}")
        player.busts_count += 1
        return False
    if dealer_sum > 21:
        print("Dealer Busted!")
        print(f"You win ${2*bet}")
        player.win(value=2*bet)
        player.busts_count += 1
        return False
    if dealer_sum > player_sum:
        print(f"The dealer get closer with {dealer_sum} > {player_sum}")
        print(f"You lose your bet of ${bet}")
        player.loses_count += 1
        return False
    if 17 <= dealer_sum < player_sum:
        print(f"You got closer with {player_sum} > {dealer_sum}")
        print(f"You win ${2*bet}")
        player.win(value=2*bet)
        player.win_count += 1
        return False
    return True

def keep_playing(player:Player):
    '''
    This function checks if the player can and want keep playing 
    '''
    if player.cash == 0:
        print(f"You lose all you cash!")
        print(f"GAME OVER!")
        return False
    choice = None
    while True:
        try:
            choice = input("Do you want to keep playing? [y/n]: ")
        except:
            continue
        else:
            if choice == 'y' or choice == 'Y':
                return True
            if choice == 'n' or choice == 'N':
                return False
            print("Please, choose a valid option.")
            
# Setting the game, creating the player

deck = Deck()
deck.shuffle()
player = Player(name='Player 1', cash=1000)
dealer = Dealer()

game_on = True

#Starting the game 

while game_on:
    sum = 0 
    dealer_sum=0
    player.cards_clear()
    dealer.cards.clear()

    print(player)
    bet = player.bet(int(input(f"Insert the value of the bet: ")))
    while bet==0:
        bet = player.bet(int(input(f"Insert the value of the bet: ")))

    print(f"Starting!")
    print(f"Dealing the first card:")

    player.hit(deck.deal_one())

    if player.cards[-1].rank == 'Ace':
        while True:
            print(f"You got an Ace, choose it's value: [1 or 11] ")
            choice_n = int(input())
            if choice_n == 1 or choice_n == 11:
                sum += choice_n
                break
    else:
        sum += player.cards[-1].value
    
    show(player,sum)

    player_action = True
    validating_choice = True
    dealer_action = False
    hit_or_stand = None
    while player_action:    
        while validating_choice:
            try:
                hit_or_stand=int(input(f"Choose your next action. Type 1 for hit and 2 for Stand: "))
            except:
                print("It looks that you didn't enter a integer.")
                continue
            else: 
                if hit_or_stand == 1 or hit_or_stand == 2:
                    break
                else:
                    print(f"Please, insert a valid choice.")
                    #this break the inner loop, that takes the choice 
            
        if hit_or_stand == 1:
            player.hit(deck.deal_one())
            if player.cards[-1].rank == 'Ace':
                ace = True
                while ace:
                    choice_n = int(input(f"You got an Ace, choose it's value: [1 or 11] "))
                    if choice_n == 1 or choice_n == 11:
                        sum += choice_n
                        break
            else:
                sum += player.cards[-1].value
            show(player,sum)
            player_action = check_win(player,sum,dealer_sum, bet)
        else:
            print(f"Now the dealer will take cards until it reachs 17 or bust!")
            dealer_action = True
            break
    
    while dealer_action:
        dealer.hit(deck.deal_one())
        if dealer.cards[-1].rank == 'Ace':
            if 17 <= (dealer_sum + 11) <= 21:
                dealer_sum += 11
        else:
            dealer_sum += dealer.cards[-1].value
        if dealer_sum >= 17:
            show(dealer,dealer_sum)
        dealer_action = check_win(player,sum, dealer_sum, bet)

    game_on = keep_playing(player)

    if not game_on:
        print(player)
        player_balance = player.cash - player.initial_cash
        if(player_balance < 0):
            print(f"\nYou lost ${-player_balance}")
        else:
            print(f"\nYou won ${player_balance}")
        print("\nHere's a resume of the current play: ")
        print(f"Wins: {player.win_count}")
        print(f"Busts: {player.busts_count}")
        print(f"Loses: {player.loses_count}")

      
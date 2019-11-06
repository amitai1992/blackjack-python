import random
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Prince', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10, 'Prince': 10, 'Queen': 10, 'King': 10, 'Ace': (11, 1)}

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    def __str__(self):
        string_card = f'suit: {self.suit}, rank: {self.rank}'
        return string_card

class Deck:
    deck = []  # list of all the cards
    def __init__(self):
        for suit in suits:
            for rank in ranks:
                temp = Card(suit, rank)
                self.deck.append(temp)
    def deck_Shuffle(self):
        random.shuffle(self.deck)

    def __str__(self):
        res = '['
        for card in self.deck:
            res += '('+card.__str__() + '), '
        res += ']'
        return res

    def __len__(self):
        size = 0
        for card in self.deck:
            size += 1
        return size

    def randomcard(self):
        return random.choice(self.deck)

    def removecard(self, other):
        try:
            self.deck.remove(other)
        except:
            print('cant remove card error in line 40')

class Hand:
    def __init__(self):
        self.cards = []  # list of the cards in that hand
        self.sum = 0  # sum of the cards in that hand

    def __add__(self, other):
        try:
            self.cards.append(other)  # we add the card and call ace_handler function to calculate our best sum
            self.ace_handler()
        except:
            print('only cards can be in this function, Line 52')

    def ace_handler(self):
        self.sum = 0
        flag = False
        aces = []
        for card in self.cards: # we sum the cards again to check our options without aces
            if card.rank == 'Ace':  # if we have an ace in our hand we dont sum it we add him to aces list
                aces.append(card)
                flag = True
            else:
                self.sum += values[card.rank]  # if it is not ace we sum it
        if flag:  # if we found ace we enter
            diff = 21 - self.sum  # diff is the difference between 21 and our current sum
            if diff >= 0:  # if diff is smaller then zero then sum is to big and that hand is lost
                if diff > 11:
                    if self.sum + 11 + len(aces) - 1 <= 21:
                        self.sum += 11 + len(aces) - 1
                    else:
                        self.sum += len(aces)
                else:
                    self.sum += len(aces)

    def __str__(self):
        result = 'cards:['
        for card in self.cards:
            result += '('+card.__str__()+'), '
        result += f'], sum = {self.sum}'
        return result

class Chip:
    def __init__(self, total=100, bet=30):
        self.total = total
        self.bet = bet
    def win_bet(self):
        self.total += self.bet
    def loos_bet(self):
        self.total -= self.bet

def take_bet(chip):
    try:
        return chip.bet
    except:
        print('please enter a chip value! line 83')

def hit(deck, hand):
    try:
        card = deck.randomcard()
        hand.__add__(card)
        deck.removecard(card)
    except:
        print('oops somthing went wrong!!! line 90')

def hit_or_not(deck, hand):
    flag = False
    while not flag:
        if hand.sum > 21:
            break
        ans = input('do you want to hit?: ')
        if ans == 'yes':
            hit(deck, hand)
            print('player' + str(hand))
        elif ans == 'no':
            flag = True
        else:
            print("please enter 'yes' or 'no' only!!!")

def show_some(player, dealer):
    try:
        sub_dealer_sum = 0
        temp_dealer = '['
        for i in range(1, len(dealer.cards)):
            temp_dealer += dealer.cards[i].__str__() + ', '
        temp_dealer += ']'
        print('playe'+ str(player))
        print('dealer'+temp_dealer)
    except:
        print('error acords line 108')

def show_all(player, dealer):
    try:
        print('player' + str(player))
        print('dealer'+str(dealer))
    except:
        print('error acords in line 119')

def blackjack_check(player):
    try:
        ace = False
        king = False
        if len(player.cards) == 2:
            for card in player.cards:
                if card.rank == 'King': king = True
                elif card.rank == 'Ace': ace = True
            if ace and king:
                return True
            else:
                return False
        else:
            return False
    except:
        print('somthing went wrong in line 157')

def player_turn_sanerios(player, chip):
    try:
        if player.sum > 21:
            print('player lost')
            chip.loos_bet()
            return False
        elif (player.sum == 21) and (blackjack_check(player)):
            print('player won its blackjack!!!')
            chip.win_bet()
            return False
        else:
            return True
    except:
        print('error in line 150')

def game_sanerios(player, chip, dealer):
    try:

        if dealer.sum > 21:
            print('player won')
            chip.win_bet()
            return False

        elif dealer.sum > player.sum:
            print('dealer won')
            chip.loos_bet()
            return False
        elif dealer.sum == player.sum:
            print('its a tai')
            return False
        elif (dealer.sum == 21) and (blackjack_check(dealer)):
            print('dealer won its black jack!!!')
            chip.loos_bet()
            return False
        else:
            print('player won')
            chip.win_bet()
            return False
    except:
        print('error in line 178')



deck = Deck()
deck.deck_Shuffle()
chips = Chip()
game = True
mingame = True

while game and chips.total > chips.bet:
    deck = Deck()
    deck.deck_Shuffle()
    player_hand = Hand()
    dealer_hand = Hand() 
    while mingame:
        hit(deck, player_hand)
        hit(deck, dealer_hand)
        hit(deck, player_hand)
        hit(deck, dealer_hand)
        show_some(player_hand, dealer_hand)
        hit_or_not(deck, player_hand)
        show_some(player_hand, dealer_hand)
        mingame = player_turn_sanerios(player_hand, chips)
        if mingame:
            while dealer_hand.sum < player_hand.sum and dealer_hand.sum <= 21:
                hit(deck, dealer_hand)
                show_all(player_hand, dealer_hand)
            mingame = game_sanerios(player_hand, chips, dealer_hand)
        print(chips.total)
    while not mingame:
        res = input('do you want to conteniue playing?: ')
        if res == 'yes':
            mingame = True
        elif res == 'no':
            mingame = True
            game = False
        else:
            print("answer with 'yes' or 'no' only, try again")

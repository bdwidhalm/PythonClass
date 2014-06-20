# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
outcome = "New deal?"
score = 0
hand_result = ""

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.card_list = []

    def __str__(self):
        result = "Hand contains "
        for card in self.card_list:
            result += str(card)
            result += " "
        return result

    def add_card(self, card):
        self.card_list.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        hand_value = 0
        ace = False
        for card in self.card_list:
            hand_value += VALUES[card.get_rank()]
            if card.get_rank() == "A":
                ace = True
        if hand_value > 0:
            if not ace:
                return hand_value
            else:
                if hand_value + 10 <= 21:
                    return hand_value + 10
                else:
                    return hand_value
        else:
            return 0
   
    def draw(self, canvas, pos):
        for card in self.card_list:
            card.draw(canvas, pos)
            pos[0] += 75
 
        
# define deck class 
class Deck:
    def __init__(self):
        self.card_list = []
        for suit in SUITS:
            for rank in RANKS:
                add_card = Card(suit, rank)
                self.card_list.append(add_card)
        random.shuffle(self.card_list)

    def shuffle(self):
        self.card_list = []
        for suit in SUITS:
            for rank in RANKS:
                add_card = Card(suit, rank)
                self.card_list.append(add_card)
        random.shuffle(self.card_list)

    def deal_card(self):
        return self.card_list.pop()
    
    def __str__(self):
        result = "Deck contains "
        for card in self.card_list:
            result += str(card)
            result += " "
        return result



#define event handlers for buttons
def deal():
    global outcome, in_play, deck, dealer_hand, player_hand, hand_result, score
    if in_play:
        score -= 1
    
    deck = Deck()
    
    player_hand = Hand()
    dealer_hand = Hand()
    
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    
    outcome = "Hit or Stand?"
    hand_result = ""
    
    
    in_play = True

def hit():
    global in_play, score, outcome, hand_result
    # if the hand is in play, hit the player
    if in_play:
        if player_hand.get_value() <= 21:
            player_hand.add_card(deck.deal_card())
            # if busted, assign a message to outcome, update in_play and score
            if player_hand.get_value() > 21:
                outcome = "New deal?"
                hand_result = "You busted, you lost!"
                score -= 1
                in_play = False
       
def stand():
    global in_play, score, outcome, hand_result
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play:
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck.deal_card())
        if dealer_hand.get_value() > 21:
            score += 1
            in_play = False
            outcome = "New deal?"
            hand_result = "Dealer busted, you win!"
        else:
            in_play = False
            # assign a message to outcome, update in_play and score
            if player_hand.get_value() <= dealer_hand.get_value():
                score -= 1
                outcome = "New deal?"
                hand_result = "You lost!"
            else:
                score += 1
                outcome = "New deal?"
                hand_result = "You won!"
    else:
        pass
    
    
# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    global dealer_hand, player_hand, score
    canvas.draw_text("BlackJack", [200, 50], 48, "Black")
    canvas.draw_text(outcome, [200, 350], 36, "Red")
    canvas.draw_text(hand_result, [150, 300], 36, "Yellow")
    score_text = "Score: " + str(score)
    canvas.draw_text(score_text, [400, 550], 24, "Black")
    if player_hand.get_value() != 0:
        canvas.draw_text(str(player_hand.get_value()), [15, 450], 24, "Black")
    
    player_hand.draw(canvas, [70, 400])
    dealer_hand.draw(canvas, [70, 100])
    
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [70 + CARD_BACK_CENTER[0], 100 + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)
    else:
        if player_hand.get_value() != 0:
            canvas.draw_text(str(dealer_hand.get_value()), [15, 150], 24, "Black")

dealer_hand = Hand()
player_hand = Hand()
# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
frame.start()


# remember to review the gradic rubric
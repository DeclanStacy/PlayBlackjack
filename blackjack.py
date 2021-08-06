#! python3
# Blackjack
'''
Card desgin:

/---------\
| 5     5 |
|         |
|         |
|         |
|         |
|         |
|         |
|         |
| 5     5 |
\---------/

/---------\
|---------|
|---------|
|---------|
|---------|
|---------|
|---------|
|---------|
|---------|
|---------|
\---------/
'''

import random

# Defines variables
integers = [str(i) for i in range(2,11)]
deck = []
playerHand = []
dealerCards = []
money = 500
bet = 0
blackjack = False
cardHeight = 9

# Defines class for cards
# Has the following attributes:
# faceUp - list of strings representing front of card, each string is one line of text
# faceDown - list of strings representing back of card, each string is one line of text
# value - value of the card (1 for ace)
class Card():

    # Initializes based on card name
    def __init__(self, name):
        # Front of card design
        corners = '|%s     %s|' % (name, name) if name == '10' else '|%s       %s|' % (name, name)
        self.faceUp = ['/---------\\', corners]
        for i in range(cardHeight-4):
            self.faceUp.append('|         |')
        self.faceUp.append(corners)
        self.faceUp.append('\\---------/')

        # Back of card design
        self.faceDown = ['/---------\\']
        for i in range(cardHeight-2):
            self.faceDown.append('|---------|')
        self.faceDown.append('\\---------/')
        
        if name in integers:
            self.value = int(name)
        elif name == 'A':
            self.value = 1
        else:
            self.value = 10

# Creates an instance of every card object
cards = [Card(i) for i in 'A23456789JQK']
cards.append(Card('10'))

# Shuffles cards
def shuffleCards(deck, playerHands = [[]], dealerCards = []):
    deck = []
    for card in cards:
        for i in range(4):
            deck.append(card)
    # Prevents duplicate cards from being added into the deck
    for playerHand in playerHands:
        for card in playerHand:
            deck.remove(card)
    for card in dealerCards:
        deck.remove(card)
    random.shuffle(deck)
    return deck

# Gives the player or the dealer a card from the deck
def drawCard(deck, playerHands, dealerCards, i = -1):
    if len(deck) == 0:
        deck = shuffleCards(deck, playerHands, dealerCards)
    # If no index given, that means the dealer is drawing
    if i == -1:
        dealerCards.append(deck[0])
    else:
        playerHands[i].append(deck[0])
    deck = deck[1:]
    return deck, dealerCards if i == -1 else playerHands

# Deals cards (two to player, two to dealer)
def dealCards(deck):
    deck, playerHands = drawCard(deck, [[]], [], 0)
    deck, dealerCards = drawCard(deck, playerHands, [])
    deck, playerHands = drawCard(deck, playerHands, dealerCards, 0)
    deck, dealerCards = drawCard(deck, playerHands, dealerCards)
    return deck, playerHands, dealerCards

# Asks the player to play another hand
def playAgain():
    print('Would you like to play a hand of blackjack? (Y/N)')
    choice = input()
    if choice.lower().startswith('y'):
        return True
    elif choice.lower().startswith('n'):
        return False
    else:
        print('That is not a valid answer. Please enter yes or no.')
        return playAgain()

# Asks the player how much money they want to bet and subtracts that from their bankroll
def getBet(money, bet):
    valid = False
    print('You have $%s.' % money)
    print('How much money do you want to give to the house?')
    print('Umm ... I mean ... bet.')
    while not valid:
        try:
            bet = int(input())
            if bet <= money and bet >= 10:
                valid = True
            elif bet >= 10:
                print('Nice try, but the house doesn\'t give loans to cheaters like you!')
                print('You can only bet up to $%s!' % money)
            elif bet > 0:
                print('Minimum bet is $10! No low rollers in this house!')
            else:
                print('How the heck do you bet $%s?' % bet)
                print('Please enter a positive integer.')
        except ValueError:
            print('Please enter an integer greater than ten and no higher than $%s' % money)
        
    money -= bet
    print('Thank you for your contribution!')
    return money, bet

# Displays the dealer's inital hand (first card face down)
def displayDealerHand(hand):
    for i in range(cardHeight):
        print(hand[0].faceDown[i] + hand[1].faceUp[i])

# Displays the hand of anyone, all face up
def displayHand(hand):
    for i in range(cardHeight):
        for card in hand:
            print(card.faceUp[i], end = '')
        print()

# Displays the hand of the dealer and the player, side by side
def displayBothHands(playerHand, dealerCards, faceUp = False):
    print('Dealer\'s cards:' + ' '*10 + 'Your cards:')
    for i in range(cardHeight):
        toDisplay = dealerCards[0].faceUp[i] if faceUp else dealerCards[0].faceDown[i]
        toDisplay += dealerCards[1].faceUp[i]
        toDisplay += ' ' * 3
        for card in playerHand:
            toDisplay += card.faceUp[i]
        print(toDisplay)

    
# Displays the dealer hand, player hand, the value of the player hand,
# the player's money, and how much they bet
def displayPlayerTurn(playerHands, dealerCards, money, bets, i):
    displayBothHands(playerHands[i], dealerCards)
    cardCount = determineValue(playerHands[i])
    if len(playerHands) > 1:
        print('Hand %s out of %s' % (i+1, len(playerHands)))
    # If the player has an ace, tell them both values their hand can take
    if determineValue(playerHands[i], final = True) != cardCount:
        print('Value of cards in your hand: ' + str(cardCount) + ' or ' + str(cardCount + 10))
    else:
        print('Value of cards in your hand: ' + str(cardCount))
    print('Amount of money you have: $%s' % money)
    print('Amount of money you have bet on this hand: $%s' % bets[i])

# Displays the dealer hand, the value of all non-busted hands,
# the player's money, and how much they bet
def displayDealerTurn(playerHands, dealerCards, money, bets):
    print('Dealer\'s cards:')
    displayHand(dealerCards)
    # Get the values of the non-busted hands the player has and displays them
    values = []
    for i, playerHand in enumerate(playerHands):
        if bets[i]:
            cardCount = determineValue(playerHand, final = True)
            values.append(str(cardCount))
    if len(values) > 1:
        print('You have %s non-busted hands, with values of: %s' % (len(values), ', '.join(values)))
    else:
        print('Value of your hand:', values[0])
    # Get the bets of the non-busted hands the player has and displays them
    validBets = ['$' + str(i) for i in bets if i > 0]
    if len(validBets) > 1:
        print('You have the following bets placed on each hand:', ', '.join(validBets))
    else:
        print('Amount of money you have bet on this hand:', validBets[0])
    # Displays the value of the dealer's hand
    cardCount = determineValue(dealerCards, final = True)
    print('Value of cards in the dealer\'s hand:', cardCount)
    print('Amount of money you have: $%s' % money)

# Determines the combined value of every card in the hand
# If final is True, then count aces as 11 if it keeps the sum below 22
def determineValue(hand, final = False):
    cardCount = 0
    aces = False
    for i in range(len(hand)):
        card = hand[i]
        if card.value == 1:
            aces = True
        cardCount += card.value
    if final and aces and cardCount + 10 <= 21:
        cardCount += 10
    return cardCount
    
# Asks the player what they want to do
def getOption(playerHand, money, bet):
    options = ['hit (h)', 'stand (st)']
    # Check if the player can double or split
    if len(playerHand) == 2 and playerHand[0].value == playerHand[1].value and money >= bet:
        options.append('split (sp)')
    if money >= bet:
        options.append('double (d)')

    print('What would you like to do ...')
    for opt in options:
        print(opt.capitalize())
    opt = input()
    if opt.lower().startswith('h'):
        return 'hit'
    elif opt.lower().startswith('d') and 'double (d)' in options:
        return 'double'
    elif opt.lower()[:2] == 'st':
        return 'stand'
    elif opt.lower()[:2] == 'sp' and 'split (sp)' in options:
        return 'split'
    else:
        print('That is not a valid option.')
        return getOption(playerHand, money, bet)

# Determines whether the player has lost
def checkMoney(money):
    if money == 0:
        print('Haha you lost all your money! Thanks for playing!')
        print('(And losing, as expected)')
        return True
    return False
   
# Determines whether the player or the dealer has blackjack
def isBlackjack(playerHand, dealerCards, money, bet):
    playerBlackjack = False
    dealerBlackjack = False
    
    if determineValue(playerHand, final = True) == 21:
        playerBlackjack = True
    if determineValue(dealerCards, final = True) == 21:
        dealerBlackjack = True
        
    if playerBlackjack and dealerBlackjack:
        displayBothHands(playerHand, dealerCards, True)
        print('Wow! The dealer has blackjack! Unfortunately, so do you, so you keep your money. :(')
        money += bet
    elif playerBlackjack:
        displayBothHands(playerHand, dealerCards, True)
        print('You have blackjack. Congratulations.')
        print('You win $%s. Yay.' % (bet * 1.5))
        money += bet * 2.5
    elif dealerBlackjack:
        displayBothHands(playerHand, dealerCards, True)
        print('Yes! The dealer has blackjack! You lose your money! Every single penny of that $%s!' % (bet))
    else:
        return money, False
    return money, True

# Runs a different function based on what the player decides to do
def resolveOption(option, deck, playerHands, dealerCards, money, bets, i):
    if option == 'hit':
        deck, playerHands, money, bets = hit(deck, playerHands, dealerCards, money, bets, i)
    elif option == 'split':
        deck, playerHands, money, bets = split(deck, playerHands, dealerCards, money, bets, i)
    elif option == 'double':
        deck, playerHands, money, bets = double(deck, playerHands, dealerCards, money, bets, i)
    # If the player stood, then nothing happens
    return deck, playerHands, money, bets

# Checks if the hand has a value over 21
def bust(hand):
    cardCount = determineValue(hand)
    if cardCount > 21:
        return True
    return False

# Runs when the player decides to hit
def hit(deck, playerHands, dealerCards, money, bets, i):
    # Hit
    deck, playerHands = drawCard(deck, playerHands, dealerCards, i)
    # Check for bust
    if bust(playerHands[i]):
        displayHand(playerHands[i])
        print('The value of the cards in your hand is over 21! You have busted!')
        print('That means the dealer wins and you lose your $%s bet! Yay!' % bets[i])
        bets[i] = 0
    # Continue the game loop if they didn't bust
    else:
        deck, playerHands, money, bets = doAction(deck, playerHands, dealerCards, money, bets, i)
    return deck, playerHands, money, bets

# Runs when the player decides to double
def double(deck, playerHands, dealerCards, money, bets, i):
    # Double the bet
    money -= bets[i]
    bets[i] *= 2
    print('You have doubled the amount of money you will give to the house. $%s!' % bets[i])
    print('You now have only $%s remaining.' % money)
    # Give player a card
    print('You get one card! Press enter to see what failure awaits your terrible decision!')
    wait = input()
    deck, playerHands = drawCard(deck, playerHands, dealerCards, i)
    # Check for bust
    if bust(playerHands[i]):
        displayHand(playerHands[i])
        print('You have busted! I told you it was a terrible decision!')
        print('That means the dealer wins and you lose your $%s bet! Yay!' % bets[i])
        bets[i] = 0
    # Continue (the player doesn't get to do anything else after they double)
    else:
        displayPlayerTurn(playerHands, dealerCards, money, bets, i)
        print('There\'s your one card. I hope you\'re happy.')
        print('Press enter to continue your walk into oblivion!')
        wait = input()
    return deck, playerHands, money, bets

# Runs when the player decides to split
def split(deck, playerHands, dealerCards, money, bets, i):
    # Do the split
    money -= bets[i]
    bets.append(bets[i])
    playerHands.append(playerHands[i][1:])
    playerHands[i] = playerHands[i][:1]
    deck, playerHands, money, bets = doAction(deck, playerHands, dealerCards, money, bets, i)
    return deck, playerHands, money, bets

# Does the dealer's turn
def dealerTurn(deck, playerHands, dealerCards, money, bets):
    while True:
        displayDealerTurn(playerHands, dealerCards, money, bets)
        # Check for bust
        dealerCardCount = determineValue(dealerCards, final = True)
        if bust(dealerCards):
            winnings = sum(bets)
            print('Unfortunately, the dealer busted, so you won. Here\'s your measely $%s.' % winnings)
            money += winnings * 2
            return deck, money
        # Check if the dealer's turn is over and resolve the bets
        elif dealerCardCount >= 17:
            for i, playerHand in enumerate(playerHands):
                if not bets[i]: continue
                playerCardCount = determineValue(playerHand, final = True)
                if playerCardCount > dealerCardCount:
                    print('Hand %s is a winner. I bet you feel so proud. Here\'s your measely $%s.' % (i+1, bets[i]))
                    money += bets[i] * 2
                elif dealerCardCount > playerCardCount:
                    print('On hand %s, the dealer wins! %s more dollars for the house!' % (i+1, bets[i]))
                else:
                    print('Hand %s is a push! I guess I have to give you your $%s bet back. :(' % (i+1, bets[i]))
                    money += bets[i]
            return deck, money
        # If dealer has less than 17, keep hitting
        else:
            deck, dealerCards = drawCard(deck, playerHands, dealerCards)
            print('Press enter to see the dealer\'s next draw')
            wait = input()

# Displays current state of game, asks player for their next move, and resolves it
def doAction(deck, playerHands, dealerCards, money, bets, i):
    if len(playerHands[i]) == 1:
        deck, playerHands = drawCard(deck, playerHands, dealerCards, i)
    displayPlayerTurn(playerHands, dealerCards, money, bets, i)
    option = getOption(playerHands[i], money, bets[i])
    deck, playerHands, money, bets = resolveOption(option, deck, playerHands, dealerCards, money, bets, i)
    return deck, playerHands, money, bets
    
# Displays rules and shuffles cards
print('I am assuming you know how to play blackjack because I am too lazy to teach you how to play')
print('Hopefully you will lose so the house will make money')
print('Good luck!')
deck = shuffleCards(deck)

# Runs the game loop
while not checkMoney(money) and playAgain():
    blackjack = False
    dealerCards = []
    money, bet = getBet(money, bet)
    deck, playerHands, dealerCards = dealCards(deck)
    money, blackjack = isBlackjack(playerHands[0], dealerCards, money, bet)
    if blackjack: continue
    bets = [bet]
    # Since number of hands a player has can change if they split,
    # uses a while loop instead of a for loop
    i = 0
    while i < len(playerHands):
        deck, playerHands, money, bets = doAction(deck, playerHands, dealerCards, money, bets, i)
        i += 1
    if sum(bets) > 0:
        deck, money = dealerTurn(deck, playerHands, dealerCards, money, bets)
print('You ended with $%s. Congratulations.' % money)
print('Have a nice day!')



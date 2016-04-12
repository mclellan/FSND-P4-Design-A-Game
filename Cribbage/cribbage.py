#Cribbage hand simulator
import random
import sys
import collections
import math 

class game(object):
	""" contains game information """
	hands = []

	def addHistory(self,add_event):
		self.history += [add_event]

	def __init__(self,player1,player2):
		self.player1 = player1
		self.player2 = player2

	def getHistory(self):
		return self.history

class player(object):
	""" contains information about the player """
	def __init__(self,name,isHuman,points = 0):
		self.name = name
		self.isHuman = isHuman
		self.points = points

	def addPoints(self, points):
		self.points += points

class deck(object):
	"""52 cards"""

	played = []

	def __init__(self):
		self.cards = [card('Hearts','Ace',1,1,'AH'),
		card('Hearts','Two',2,2,'2H'),
		card('Hearts','Three',3,3,'3H'),
		card('Hearts','Four',4,4,'4H'),
		card('Hearts','Five',5,5,'5H'),
		card('Hearts','Six',6,6,'6H'),
		card('Hearts','Seven',7,7,'7H'),
		card('Hearts','Eight',8,8,'8H'),
		card('Hearts','Nine',9,9,'9H'),
		card('Hearts','Ten',10,10,'10H'),
		card('Hearts','Jack',11,10,'JH'),
		card('Hearts','Queen',12,10,'QH'),
		card('Hearts','King',13,10,'KH'),
		card('Diamonds','Ace',1,1,'AD'),
		card('Diamonds','Two',2,2,'2D'),
		card('Diamonds','Three',3,3,'3D'),
		card('Diamonds','Four',4,4,'4D'),
		card('Diamonds','Five',5,5,'5D'),
		card('Diamonds','Six',6,6,'6D'),
		card('Diamonds','Seven',7,7,'7D'),
		card('Diamonds','Eight',8,8,'8D'),
		card('Diamonds','Nine',9,9,'9D'),
		card('Diamonds','Ten',10,10,'10D'),
		card('Diamonds','Jack',11,10,'JD'),
		card('Diamonds','Queen',12,10,'QD'),
		card('Diamonds','King',13,10,'KD'),
		card('Clubs','Ace',1,1,'AC'),
		card('Clubs','Two',2,2,'2C'),
		card('Clubs','Three',3,3,'3C'),
		card('Clubs','Four',4,4,'4C'),
		card('Clubs','Five',5,5,'5C'),
		card('Clubs','Six',6,6,'6C'),
		card('Clubs','Seven',7,7,'7C'),
		card('Clubs','Eight',8,8,'8C'),
		card('Clubs','Nine',9,9,'9C'),
		card('Clubs','Ten',10,10,'10C'),
		card('Clubs','Jack',11,10,'JC'),
		card('Clubs','Queen',12,10,'QC'),
		card('Clubs','King',13,10,'KC'),
		card('Spades','Ace',1,1,'AS'),
		card('Spades','Two',2,2,'2S'),
		card('Spades','Three',3,3,'3S'),
		card('Spades','Four',4,4,'4S'),
		card('Spades','Five',5,5,'5S'),
		card('Spades','Six',6,6,'6S'),
		card('Spades','Seven',7,7,'7S'),
		card('Spades','Eight',8,8,'8S'),
		card('Spades','Nine',9,9,'9S'),
		card('Spades','Ten',10,10,'10S'),
		card('Spades','Jack',11,10,'JS'),
		card('Spades','Queen',12,10,'QS'),
		card('Spades','King',13,10,'KS')]

	def __str__(self):
		s = []
		for card in self.cards:
			s.append(card.short_name)
		return ', '.join(s)

	def add_card(self,card):
		self.cards.append(card)

	def remove_card(self,card):
		self.cards.remove(card)

	def order(self):
		self.cards.sort()

	def shuffle(self):
		random.shuffle(self.cards)

	def play_card(self,x=-1):
		return self.cards.pop(x)

	def deal_to_hand(self, hand, x):
		for i in range(x):
			hand.add_card(self.play_card())

	def move_to_crib(self, crib, card):
		self.cards.remove(card)
		crib.add_card(card)

class card(object):
	"""a card with given suit, value, and name"""

	suit = 'suit'
	name = 'name'
	run_value = 0
	count_value = 0
	short_name = 'sn'

	def __init__(self,suit,name,run_value,count_value,short_name):
		self.suit=suit
		self.name=name
		self.run_value=run_value
		self.count_value=count_value
		self.short_name=short_name

class hand(deck):
	"""a hand of cards of any number"""

	def __init__(self,player,isDealer=False):
		self.cards = []
		self.id = id
		self.isDealer = isDealer
		self.player = player

class crib(deck):
	"""the discarded 2 cards from each player"""

	def __init__(self,id=1):
		self.cards = []
		self.id = id

class upcard(deck):
	"""single card drawn from deck after discarding"""

	def __init__(self):
		self.cards = []

class peg(deck):
	"""the cards played by the players"""

	def __init__(self):
		self.cards = []

def score(hand,upcard,isCrib):
	run_values = []
	count_values = []
	for card in hand.cards:
		run_values += [card.run_value]
		count_values += [card.count_value]
	run_values += [upcard.cards[0].run_value]
	count_values += [upcard.cards[0].count_value]

	runs = score_runs(run_values)
	print "runs, ", runs
	pairs = score_pairs(run_values)
	print "pairs, ", pairs
	fifteens = score_fifteens(count_values)
	print "fifteens, ", fifteens
	upjack = score_upjack(hand,upcard)
	print "upjack, ", upjack
	flush = score_flush(hand,upcard,isCrib)
	print "flush, ", flush
	return runs + pairs + fifteens + upjack + flush
		
def score_runs(values):
	""" find runs and also count runs on duplicate values
		so called "double" runs, "triple" runs, and 
		"double double" runs
	"""

	values.sort()
	pair = 1
	pair_value = 0
	last = 0
	x = 1
	score = 0
	for value in values:
		if value == last:
			"""pair found"""
			if value != pair_value and pair_value != 0:
				"""finds 2nd double uniquely"""
				pair += 1
			pair_value = value
			pair += 1
		elif value == last + 1:
			"""run of length x"""
			x += 1
		else:
			x = 1
			pair = 1
			pair_value = 0
		if x > 2:
			if pair > 1:
				score = x * pair
			else:
				score = x
		last = value
	return score

def score_pairs(values):
	"""finds all pairs,trips,quads of cards"""

	points = 0
	y = collections.Counter(values)
	for x in range(2,5):
		found = [i for i in y if y[i]==x]
		for f in found:
			points += math.factorial(x)
	return points

def score_fifteens(values):
	"""
		find all unique combinations that add to 15
		method adapted from stackexchange user thefourtheye
	"""

	def _a(idx,l,r,t):
		if t == sum(l): r.append(l)
		elif t < sum(l): return
		for u in range(idx, len(values)):
			_a(u + 1, l + [values[u]],r,t)
		return r
	return len(_a(0,[],[],15)) * 2

def score_upjack(hand,upcard):
	"""if a jack in the hand matches upcards suit"""
	for card in hand.cards:
		if upcard.cards[0].suit == card.suit and card.name == 'Jack':
			return 1
	return 0

def score_flush(hand,upcard,isCrib):
	suit_count = 1
	suits = []
	for card in hand.cards:
		suits += [card.suit]
	y = collections.Counter(suits)
	if [i for i in y if y[i]==4]:
		points = 4
		if upcard.cards[0].suit == suits[0]:
			return 5
		elif isCrib:
			return 0
		else:
			return 4
	return 0

def score_upcard(player):
	player.points += 2
	game.addHistory('%s scores 2 for jack as upcard' % player.name)

def pegging(peg,hand1,hand2):
	peghand1 = hand1
	peghand2 = hand2
	hands = [peghand1,peghand2]
	
	cards_played = 0
	dealer_priority = False
	goGiven = False

	while cards_played < 8:
		# 8 cards are played in total

		for hand in hands:
			# cycle through players

			if (dealer_priority and hand.isDealer) or (not dealer_priority and not hand.isDealer):
				# check turn to play

				if len(hand.cards) > 0:
					# check if player has cards remaining

					count = getCount(peg)

					if canPlay(count,hand):
						# check if player has a viable move

						if hand.player.isHuman:
							#if player is human

							success = False

							while not success:
								# loop until player picks a card that is playable
								# check first if there are cards that are playable

								if canPlay(count,hand):
									var = raw_input("The count is:%s\r\nCards available (%s)\r\nEnter a valid card to play: " % (count,hand))
									for card in hand.cards:
										if card.short_name == var:
											if card.count_value <= 31-count:
												peg = pegCard(peg,card,hand.player)
												success = True
												cards_played += 1
												hand.remove_card(card)
											else:
												print "That card cannot be played."
						else:
							# pick random card for AI player
							hand.shuffle()
							for card in hand.cards:
								if card.count_value <= 31-count:
									peg = pegCard(peg,card,hand.player)
									cards_played += 1
									hand.remove_card(card)

					else:
						if goGiven:
							peg = pegCard(peg,card('new','new',None,None,'new'),hand.player)
							goGiven = False
						else:
							peg = pegCard(card('go','go',None,None,'go'),hand.player)
							goGiven = True

		if not goGiven:
			dealer_priority = not dealer_priority


def pegCard(peg,card,player):
	""" logic and scoring for pegging play """
	# test, just add one
	peg.add_card(card)
	player.addPoints(1)
	return peg


def getCount(peg):
	x = 0
	for card in peg.cards:
		if card.short_name == 'new':
			x = 0
		else:
			x += card.count_value
	return x

def canPlay(count,hand):
	for card in hand.cards:
		if card.count_value <= 31-count:
			return True
	return False


	


player1 = player('You',True)
player2 = player('AI',False)
game = game(player1,player2)
deck = deck()
deck.shuffle()
hand1 = hand(player1,True)
hand2 = hand(player2,False)
crib = crib(1)
deck.deal_to_hand(hand1,6)
deck.deal_to_hand(hand2,6)
print hand1
var = raw_input("Enter comma delimited cards to send to crib: ")
cards = str.split(var,',')
for card in cards:
	for hand_card in hand1.cards:
		if hand_card.short_name == card:
			hand1.move_to_crib(crib,hand_card)
upcard = upcard()
deck.deal_to_hand(upcard,1)
if upcard.cards[0].name == 'Jack':
	score_upcard
print "The upcard is: ", upcard
peg = peg()
pegging(peg,hand1,hand2)
print hand1
print "hand score is: ", score(hand1,upcard,False)

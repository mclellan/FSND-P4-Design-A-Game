#Cribbage hand simulator
import random, sys, math, collections, copy
from models import User, Game, Score
# from google.appengine.ext import ndb


class cgame(object):
	""" contains game information """
	dealBool = False

	def setDeal(self,dealBool):
		self.dealBool = dealBool

	def addHistory(self,add_event):
		self.history += [add_event]

	def __init__(self,player1,player2):
		self.player1 = player1
		self.player2 = player2
		cgame.game_over = False
		cgame.winner = None

	def declareWinner(self,player):
		self.game_over = True
		self.winner = player

	def getHistory(self):
		return self.history

	def score(self,player,points):
		if player == self.player1:
			if self.player1.addPoints(points):
				cgame.winner = self.player1
				cgame.game_over = True
		else:
			if self.player2.addPoints(points):
				cgame.winner = self.player2
				cgame.game_over = True
		#print game.player1.name, game.player1.points, game.player2.name, game.player2.points

class player(object):
	""" contains information about the player """
	def __init__(self,name,isHuman,points = 0):
		self.name = name
		self.isHuman = isHuman
		self.points = points

	def addPoints(self, points):
		self.points += points
		if self.points >= 121:
			return True
		else:
			return False

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
		"""if card in self.cards:
			self.cards.remove(card)
		else:
			for c in self.cards:
				if card.short_name == c.short_name:
					self.cards.remove(c)"""
		self.cards.remove(card)
		crib.add_card(card)

class card(object):
	"""a card with given suit, value, and name"""

	def __init__(self,suit,name,run_value,count_value,short_name):
		self.suit=suit
		self.name=name
		self.run_value=run_value
		self.count_value=count_value
		self.short_name=short_name

class hand(deck):
	"""a hand of cards of any number"""

	"""
	def __init__(self,player,isDealer=False):
		self.cards = []
		self.id = id
		self.isDealer = isDealer
		self.player = player
	"""

	# method to convert a datastore string to a set of cards
	def __init__(self, s):
		self.cards = []
		goCard = card('go','go',0,0,'go')
		newCard = card('new','new',0,0,'new')
		fullDeck = deck()
		fullDeck.add_card(goCard)
		fullDeck.add_card(newCard)
		cards = str.split(s,',')
		for c in cards:
			for hand_card in fullDeck.cards:
				if hand_card.short_name == c.strip():
					fullDeck.move_to_crib(self,hand_card)

class crib(deck):
	"""the discarded 2 cards from each player"""

	def __init__(self,player):
		self.cards = []
		self.player = player

class upcard(deck):
	"""single card drawn from deck after discarding"""

	def __init__(self):
		self.cards = []

class peg(deck):
	"""the cards played by the players"""

	def __init__(self):
		self.cards = []

def score(game,hand,upcard,isCrib):
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

	total = runs + pairs + fifteens + upjack + flush 
	print hand.player.name, "scores: ", total 
	
	game.score(hand.player,total)
	"""
	if game.player1 == hand.player:
		game.player1.addPoints(total,game)
	else:
		game.player2.addPoints(total,game)"""
		
def score_runs(values):
	""" find runs and also count runs on duplicate values
		so called "double" runs, "triple" runs, and 
		"double double" runs
	"""

	values.sort()
	print values
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
		elif value == last + 1 and last != 0:
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

def score_upcard(game,player):
	game.score(player,2)
	"""
	if game.player1 == player:
		game.player1.points += 2
	else:
		game.player2.points += 2"""
	#game.addHistory('%s scores 2 for jack as upcard' % player.name)

def pegging(game,p,hand1,hand2):
	peghand1 = copy.deepcopy(hand1)
	peghand2 = copy.deepcopy(hand2)
	hands = [peghand1,peghand2]
	hands[0].player = hand1.player
	hands[1].player = hand2.player
	
	cards_played = 0
	dealer_priority = False
	goGiven = False

	goCard = card('go','go',0,0,'go')
	newCard = card('new','new',0,0,'new')

	while cards_played < 8:
		# 8 cards are played in total

		for h in hands:
			# cycle through players

			if (dealer_priority and h.isDealer) or (not dealer_priority and not h.isDealer):
				# check turn to play

				count = getCount(p)

				if canPlay(count,h):
					# check if player has a viable move

					if h.player.isHuman:
						#if player is human

						success = False

						while not success:
							# loop until player picks a card that is playable
							# check first if there are cards that are playable

							if canPlay(count,h):
								var = raw_input("The count is:%s\r\nCards available (%s)\r\nEnter a valid card to play: " % (count,h))
								for c in h.cards:
									if c.short_name == var:
										if c.count_value <= 31-count:
											#peg = pegCard(peg,c,hand.player)
											pegCard(game,p,c,h.player)
											success = True
											cards_played += 1
											h.remove_card(c)
										else:
											print "That card cannot be played."
					else:
						# pick random card for AI player
						h.shuffle()
						for c in h.cards:
							if c.count_value <= 31-count:
								pegCard(game,p,c,h.player)
								cards_played += 1
								h.remove_card(c)
								break

					# check count
					if getCount(p) == 31:
						pegCard(game,p,newCard,h.player)
						goGiven = False

				else:
					if goGiven:
						# Previous player already passed
						# so end this set of cards by playing new
						pegCard(game,p,newCard,h.player)
						goGiven = False
					else:
						# The first player incapable of playing
						# gives a go, passing the play
						pegCard(game,p,goCard,h.player)
						goGiven = True
						dealer_priority = not dealer_priority

		if not goGiven:
			dealer_priority = not dealer_priority

		if game.game_over:
			break

def pegCard(game,peg,card,player):
	""" logic and scoring for pegging play """
	print '%s plays: %s' % (player.name, card.short_name)
	y = getCount(peg)
	peg.add_card(card)
	score_message = []
	x = getCount(peg)

	"""
	# get game player who is scoring
	if game.player1 == player:
		scorer = game.player1
	else:
		scorer = game.player2"""
	
	# Don't score a go/end
	if card.name == 'go':
		return

	# determine number of played cards
	card_count = 0
	for c in peg.cards:
		if c.count_value != 0:
			card_count += 1

	# score 31s as 1 point since the go/lastcard
	# is always counted
	if x == 31:
		#scorer.addPoints(2,game)
		game.score(player,2)
		score_message += ['scores 2 points for playing 31']
	
	elif card.short_name == 'new':
		if y == 31:
			return
		# score go
		#scorer.addPoints(1,game)
		game.score(player,1)
		score_message += ['scores 1 point for a go']
	
	elif card_count == 8 and x != 31:
		# score last card
		#scorer.addPoints(1,game)
		game.score(player,1)
		score_message += ['scores 1 point for playing the last card']

	# score 15s
	if x == 15:
		#scorer.addPoints(2,game)
		game.score(player,2)
		score_message += ['scores 2 points for playing 15']

	y = getCount(peg)
	# score sets of cards 
	setValues = []
	for i in range(1,len(peg.cards)+1):
		if y != 0:
			if [peg.cards[-i].run_value] != 0:
				setValues += [peg.cards[-i].run_value]
				y -= peg.cards[-i].count_value

	if len(setValues) > 1 and setValues[0] == setValues[1]:
		# pair
		if len(setValues) > 2 and setValues[2] == setValues[1]:
			# triple
			if len(setValues) > 3 and setValues[3] == setValues[2]:
				# quadruple
				#scorer.addPoints(12,game)
				game.score(player,12)
				score_message += ['scores 12 points for playing a quadruple']
			else:
				#scorer.addPoints(6,game)
				game.score(player,6)
				score_message += ['scores 6 points for playing a triple']
		else:
			#scorer.addPoints(2,game)
			game.score(player,2)
			score_message += ['scores 2 points for playing a pair']

	# score runs
	values = []
	run_score = 0
	for i in range(1,len(peg.cards)+1):
		if x != 0:
			if [peg.cards[-i].run_value] != 0:
				values += [peg.cards[-i].run_value]
				x -= peg.cards[-i].count_value
			# print values, x
			if len(values) > 2:
				valueSort = copy.copy(values)
				valueSort.sort()
				last = -1
				z = 1
				for v in valueSort:
					if v == last + 1:
						z += 1
					else:
						z = 1
					last = v
					if z == len(valueSort):
						print valueSort, values
						run_score = z
	if run_score > 0:
		#scorer.addPoints(run_score,game)
		game.score(player,run_score)
		score_message += ['scores %s points for playing a run' % run_score]
		#print run_score, 'RUN RUN RUN'

	for s in score_message:
		print '%s %s' % (player.name, s)

def getCount(p):
	x = 0
	for c in p.cards:
		if c.short_name == 'new':
			x = 0
		else:
			x += c.count_value
	return x

def canPlay(count,h):
	for c in h.cards:
		if c.count_value <= 31-count:
			return True
	return False

def testRun(peg,hand):
	a = True
	while a:
		count = getCount(peg)
		var = raw_input("The count is:%s\r\nCards available (%s)\r\nEnter a valid card to play: " % (count,hand))
		for c in hand.cards:
			if c.short_name == var:
				if c.count_value <= 31-count:
					peg = pegCard(peg,c,hand.player)
					success = True
					#cards_played += 1
					hand.remove_card(c)
				else:
					print "That card cannot be played."

def newGame(playerName):
	""" creates a new game from player names 
	and determines the dealer """
	player1 = player(playerName,True)
	player2 = player('AI',False)
	g = cgame(player1,player2)

	# determine dealer
	dealer = random.choice([g.player1,g.player2])
	if dealer == g.player1:
		g.setDeal(True)
		g.message = 'The dealer is: %s' % dealer.name
	return g



def playGame(game):
	""" container for a full game"""

	while not game.game_over:
		# player a hand
		playHand(game, dealBool)

		# change dealer
		dealBool = not dealBool
		print 'Point totals:'
		print game.player1.name, game.player1.points
		print game.player2.name, game.player2.points
		print ''

	print game.winner.name, 'has won the game!'

def playHand(game, dealBool):
	d = deck()
	d.shuffle()
	#cr = crib()

	# Set dealer/play order
	if dealBool:
		hand1 = hand(game.player1,True)
		hand2 = hand(game.player2,False)
		cr = crib(game.player1)
	else: 
		hand1 = hand(game.player2,True)
		hand2 = hand(game.player1,False)
		cr = crib(game.player2)


	d.deal_to_hand(hand1,6)
	d.deal_to_hand(hand2,6)

	hands = [hand1,hand2]
	for h in hands:
		if h.player.isHuman:
			print h
			x = 0
			while x < 2:
				var = raw_input("Enter %s card(s) separated by a comma: " % (2-x))
				cards = str.split(var,',')
				if len(cards) > 2-x:
					print 'too many cards, pick %s cards' % (2-x)
				else :
					for c in cards:
						for hand_card in h.cards:
							if hand_card.short_name == c:
								h.move_to_crib(cr,hand_card)
								x += 1

		else:
			for i in range(2):
				h.move_to_crib(cr,h.cards[i])

	u = upcard()
	d.deal_to_hand(u,1)
	if u.cards[0].name == 'Jack':
		score_upcard(game,hand1.player)
	print "The upcard is: ", u
	p = peg()
	#testRun(peg,hand1)
	pegging(game,p,hand1,hand2)

	#scoring 
	if not game.game_over:
		print hand2, u
		score(game,hand2,u,False)
		if not game.game_over:
			print hand1, u
			score(game,hand1,u,False)
			if not game.game_over:
				print cr, u
				score(game,cr,u,True)



# determine the state of the game and then resume play in the next
# game step
def resumeFromAnywhere(game, request):

	#user_hand, ai_hand, crib, dealer, pegging, upcard
	u = hand(str(game.user_hand))
	a = hand(str(game.ai_hand))
	cr = hand(str(game.crib_hand))
	uc = hand(str(game.upcard))
	goToPegging = True

	# Check that the user and ai's hands are empty
	if len(u.cards) == 0 or u.cards == None:
		# deal the hands and return the game and message
		return dealHands(game,u,a)

	# Check if the crib has been populated by two user cards
	# if not we check the request to see if it contains
	# valid card selections
	cards_to_play = 2 - len(cr.cards)
	if cards_to_play > 0:
		goToPegging = False

		# validate request
		if request is not None:
			# clear the game messaging
			game.message = ''

			# try to play the cards in the request
			game = playToCrib(game,u,a,cr,uc,request,cards_to_play)
			cr = hand(str(game.crib_hand))
			if len(cr.cards) == 4:
				goToPegging = True
				request = None
	
	if goToPegging and not game.game_over:
		# pegging needs to start or continue
		game = pegging2(game,u,a,uc,request)
		
		# determine number of played cards
		card_count = 0
		p = hand(str(game.pegging))
		for c in p.cards:
			if c.count_value != 0:
				card_count += 1

		if card_count == 8:
			# Score the hands and crib
			if game.dealer:
				# if dealer --> ai, user, crib(user)
				game = scoreHand(game,game.ai_hand,False,False) if game.game_over is False else game
				game = scoreHand(game,game.user_hand,True,False) if game.game_over is False else game
			else:
				# if not dealer --> user, ai, crib(ai)
				game = scoreHand(game,game.user_hand,True,False) if game.game_over is False else game
				game = scoreHand(game,game.ai_hand,False,False) if game.game_over is False else game

			game = scoreHand(game,game.crib_hand,game.dealer,True) if game.game_over is False else game
						
			# change dealer and reset hands
			game.dealer = not game.dealer
			game.user_hand = ''
			game.ai_hand = ''
			game.upcard = ''
			game.pegging = ''
			game.crib_hand = ''

			# deal new hands
			game = dealHands(game,hand(''),hand('')) if game.game_over is False else game

	return game


def dealHands(game,u,a):
 	# create a 52 card deck and deal new hands of 6
	d = deck()
	d.shuffle()
	d.deal_to_hand(u,6)	
	d.deal_to_hand(a,6)

	game.addHistory(str(u))
	game.user_hand = str(u)
	game.ai_hand = str(a)

	# determine the dealer's name
	if game.dealer:
		deal = 'your'
	else:
		deal = "the AI's"

	game.message += str('It is %s deal and crib. Select two cards from your hand to put in the crib. Your hand is: %s' % (deal, str(u)))
	return game

def parseRequest(game,u,request,cards_to_play):
	played = []
	cards = str.split(str(request.play),',')
	if len(cards) is not cards_to_play:
		game.message = 'Choose %s card(s). Format for multiple cards: AH,2H' % cards_to_play
		return game
	else :
		for c in cards:
			match = False
			# check player's hand for the cards entered
			# in the request
			for hand_card in u.cards:
				if hand_card.short_name == c.strip():
					played += [hand_card]
					match = True

			if not match:
				# the entered card isn't in the player's hand
				# gracefully handle this and message to the user
				game.message = c + ': is not a valid play (not a card in your hand). '
				game.message += 'Choose %s card(s) to ' % cards_to_play
				if len(u.cards) > 4:
					game.message += 'put in the crib. Format: AH,2H'
				else:
					game.message += 'play.'
				game.message += ' Cards in your hand: ' + str(u)
				return game
		if len(played) == 0:
			game.message = 'Choose %s card(s). Format for multiple cards: AH,2H' % cards_to_play
	return played

def playToCrib(game,u,a,cr,uc,request,cards_to_play):
		temp_game = parseRequest(game,u,request,cards_to_play)
		if type(temp_game) is Game:
			return temp_game
		else:
			for hand_card in temp_game:
				u.move_to_crib(cr,hand_card)

		# add selection to game history
		game.addHistory('You played %s into the crib.'% request.play)

		# select two cards from AI to pass
		for i in range(2):
			a.move_to_crib(cr,a.cards[i])

		# select upcard
		d = deck()
		# remove cards already played
		cards_to_remove = str.split(', '.join([str(u),str(a),str(cr)]),', ')
		for deck_card in d.cards:
			for s in cards_to_remove:
				if deck_card.short_name == s:
					d.remove_card(deck_card)
		d.shuffle()
		d.deal_to_hand(uc,1)
		game.message = 'The upcard is ' + uc.cards[0].short_name + '. '

		#score 2 points if the upcard is a Jack for the dealer
		if uc.cards[0].name == 'Jack':
			if game.dealer:
				game.message += 'You scored 2 points for turning up a Jack for the upcard.'
				game.score(True,2)
			else:
				game.message += 'AI scored 2 points for turning up a Jack for the upcard.'
				game.score(False,2)

		# Update game
		game.crib_hand = str(cr)
		game.ai_hand = str(a)
		game.user_hand = str(u)
		game.upcard = str(uc)

		return game

def handsMinusPegging(h,p):
	# remove from the hands the cards already played
	for c in h.cards:
		for pc in p.cards:
			if c.short_name == pc.short_name:
				h.remove_card(c)
	return h

def pegging2(game,u,a,uc,request):
	# return if previous play ended game
	if game.game_over:
		return game

	# get pegging so far
	p = hand(str(game.pegging))
	count = getCount(p)

	# return if pegging is complete
	card_count = 0
	for c in p.cards:
		if c.count_value != 0:
			card_count += 1
	if card_count == 8:
		return game

	# cards to indicate a go or new set of play
	goCard = card('go','go',0,0,'go')
	newCard = card('new','new',0,0,'new')

	# update playable cards 
	u = handsMinusPegging(u,p)
	a = handsMinusPegging(a,p)

	if len(p.cards) == 0 and request == None:
		# pick random card for AI player if the first play
		# goes to the AI, otherwise prompt user to play first
		if game.dealer:
			c = random.choice(a.cards)
			game = pegCard2(game,p,c,False)
		else: 
			game.message += 'It is your turn to begin pegging. '
	
	elif request == 'AIPLAY' or request == 'AIPLAYGO':
		""" AI play logic"""
		# See if AI has a playable card
		if canPlay(count,a):
			# Select valid playable card
			a.shuffle()
			for c in a.cards:
				if c.count_value <= 31-count:
					game = pegCard2(game,p,c,False)
					break
			request = 'AIPLAYED'
			return pegging2(game,u,a,uc,request)

		elif request == 'AIPLAY':
			# check if count was 31 and play new instead of go
			if count == 31:
				game = pegCard2(game,p,newCard,True)
				return pegging2(game,u,a,uc,request)
			else:	
				# AI can't play so gives go
				game = pegCard2(game,p,goCard,False)
				game.message += 'The AI has no moves and gives you a go.\r\n'
				u = handsMinusPegging(u,hand(game.pegging))

				# Check if user can play on that go
				if not canPlay(count, u):
					# If not the user scores the go
					# and pegging returns to AI for new round
					game = pegCard2(game,p,newCard,True)
					game.message += 'You have no plays, the AI will start a new round of pegging.\r\n'
					request = 'AIPLAY'
					return pegging2(game,u,a,uc,request)

		elif request == 'AIPLAYGO':
			# Can't play but the go was given
			# score end of hand
			game = pegCard2(game,p,newCard,False)
			game.message += 'Your turn to start a new round of pegging. Please play a card.\r\n'
			return game

	elif request == 'AIPLAYED':
		# Check to see the player has a valid response
		if not canPlay(count,u):
			game = pegCard2(game,p,goCard,True)
			request = 'AIPLAYGO'
			return pegging2(game,u,a,uc,request)
		
	else:
		# User has submitted a play
		if request != None:
			temp_game = parseRequest(game,u,request,1)
			if type(temp_game) is not Game:
				# Card selected exists
				game = pegCard2(game,p,temp_game[0],True)

				# Check to see if AI can play
				request = 'AIPLAY'
				game = pegging2(game,u,a,uc,request)

	if not game.game_over:
		# update values to provide better messaging
		p = hand(str(game.pegging))
		count = getCount(p)
		u = handsMinusPegging(u,p)
		a = handsMinusPegging(a,p)

		if len(u.cards) > 0 and 'in your hand' not in game.message:
			game.message += 'Cards remaining in your hand: ' + str(u) + '\r\n'
		if len(u.cards) > 0 and 'The count is' not in game.message:
			game.message += ' The count is: ' + str(getCount(p))
			
	return game

def pegScore(game,points,player,message):
	if not game.game_over:
		game.message += message
		game.addHistory(message)
		game.score(player,points)
	return game

def pegCard2(game,peg,card,player):
	""" logic and scoring for pegging play """

	# See if card attempt can be played (count under 31)
	count = getCount(peg)
	if card.count_value > 31-count:
		game.message = 'Card cannot be played, the count is too high. Current count: ' + str(count)
		return game

	name = game.user.get().name if player == True else 'AI'
	game.addHistory('%s plays: %s. ' % (name, card.short_name))
	game.message += '%s plays: %s. ' % (name, card.short_name)

	y = getCount(peg)
	peg.add_card(card)
	score_message = []
	card_count = 0
	x = getCount(peg)
	
	# Don't score a go/end
	if card.name == 'go':
		game.pegging = str(peg)
		return game

	# determine number of played cards
	for c in peg.cards:
		if c.count_value != 0:
			card_count += 1

	if x == 31:
		game = pegScore(game,2,player,'%s scores 2 points for playing 31' % name)
	
	elif card.short_name == 'new':
		# The last play was 31 so don't score
		if y == 31:
			game.pegging = str(peg)
			return game
		else:
			# score go
			game = pegScore(game,1,player,'%s scores 1 point for a go' % name)
	
	# score last card
	elif card_count == 8:
		
		game = pegScore(game,1,player,'%s scores 1 point for playing the last card' % name)

	# score 15s
	if x == 15:
		game = pegScore(game,2,player,'%s scores 2 points for playing 15' % name)


	y = getCount(peg)
	# score sets of cards 
	setValues = []
	for i in range(1,len(peg.cards)+1):
		if y != 0:
			if [peg.cards[-i].run_value] != 0:
				setValues += [peg.cards[-i].run_value]
				y -= peg.cards[-i].count_value

	if len(setValues) > 1 and setValues[0] == setValues[1]:
		# pair
		if len(setValues) > 2 and setValues[2] == setValues[1]:
			# triple
			if len(setValues) > 3 and setValues[3] == setValues[2]:
				# quadruple
				game = pegScore(game,12,player,'%s scores 12 points for playing a quadruple' % name)
			else:
				game = pegScore(game,6,player,'%s scores 6 points for playing a triple' % name)
		else:
			game = pegScore(game,2,player,'%s scores 2 points for playing a pair' % name)

	# score runs
	values = []
	run_score = 0
	for i in range(1,len(peg.cards)+1):
		# iterate through all the cards pegged
		if x != 0:
			# check that we are on the most recent run
			# by counting down cards to 0 (initial peg value)
			if peg.cards[-i].run_value != 0:
				# ignore plays of 'go'
				# add the card to the set of values
				values += [peg.cards[-i].run_value]
				x -= peg.cards[-i].count_value

			if len(values) > 2:
				# runs are of minimum length 3
				values.sort()
				last = -1
				z = 1
				for v in values:
					if v == last + 1:
						z += 1
					else:
						z = 1
					last = v
					if z == len(values):
						#print valueSort, values
						run_score = z
	if run_score > 0:
		game = pegScore(game,run_score,player,'%s scores %s points for playing a pair' % (name,run_score))

	game.pegging = str(peg)

	return game

def scoreHand(game,h,player,isCrib):
	hs = hand(str(h))
	upcard = hand(str(game.upcard))
	name = game.user.get().name if player == True else 'AI'


	run_values = []
	count_values = []
	for card in hs.cards:
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
	upjack = score_upjack(hs,upcard)
	print "upjack, ", upjack
	flush = score_flush(hs,upcard,isCrib)
	print "flush, ", flush

	total = runs + pairs + fifteens + upjack + flush 
	msg = (name + "scores: " + str(total) + 
			'(runs: ' + str(runs) + 
			',pairs: ' + str(pairs) + 
			',fifteens: ' + str(fifteens) + 
			',upjack: ' + str(upjack) + 
			',flush: ' + str(flush) + ') ')
	if isCrib:
		msg += ' for the crib.'
	game.message += msg
	game.addHistory(msg)
	game.score(player,total)

	return game


#g = newGame('John')
#p = pickle.dumps(g)
#print p
#g2 = pickle.loads(p)
#print g2
#print g2.player1, g2.player2, g2.winner
#playGame(g2)
# test # game.player1.points = 120
#playGame(game)

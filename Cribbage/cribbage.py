#Cribbage hand simulator
import random, sys, math, collections, copy

class game(object):
	""" contains game information """
	hands = []

	def addHistory(self,add_event):
		self.history += [add_event]

	def __init__(self,player1,player2):
		self.player1 = player1
		self.player2 = player2
		game.finished = False
		game.winner = None

	def declareWinner(self,player):
		self.finished = True
		self.winner = player

	def getHistory(self):
		return self.history

	def score(self,player,points):
		if player == self.player1:
			if self.player1.addPoints(points):
				game.winner = self.player1
				game.finished = True
		else:
			if self.player2.addPoints(points):
				game.winner = self.player2
				game.finished = True
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

	def __init__(self,player,isDealer=False):
		self.cards = []
		self.id = id
		self.isDealer = isDealer
		self.player = player

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

		if game.finished:
			break


def pegCard(game,peg,card,player):
	""" logic and scoring for pegging play """
	print '%s plays: %s' % (player.name, card.short_name)
	y = getCount(peg)
	peg.add_card(card)
	score_message = []
	card_count = 0
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

def playGame(game):
	""" container for a full game"""

	# Determine the dealer randomly for first hand
	dealBool = False
	dealer = random.choice([game.player1,game.player2])
	print 'The dealer is:',dealer.name
	if dealer == game.player1:
		dealBool = True

	while not game.finished:
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
	if not game.finished:
		print hand2, u
		score(game,hand2,u,False)
		if not game.finished:
			print hand1, u
			score(game,hand1,u,False)
			if not game.finished:
				print cr, u
				score(game,cr,u,True)

player1 = player('John',True)
player2 = player('AI',False)
game = game(player1,player2)
# test # game.player1.points = 120
playGame(game)

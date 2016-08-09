"""models.py - This file contains the class definitions for the Datastore
entities used by the Game. Because these classes are also regular Python
classes they can include methods (such as 'to_form' and 'new_game')."""

import random
from datetime import date
from protorpc import messages
from google.appengine.ext import ndb


class User(ndb.Model):
    """User profile"""
    name = ndb.StringProperty(required=True)
    email = ndb.StringProperty()


class Game(ndb.Model):
    """Game object"""
    user_points = ndb.IntegerProperty(required=True)
    ai_points = ndb.IntegerProperty(required=True)
    game_over = ndb.BooleanProperty(required=True, default=False)
    user = ndb.KeyProperty(required=True, kind='User')
    history = ndb.StringProperty(required=True)
    dealer = ndb.BooleanProperty(required=True, default=False)
    user_hand = ndb.StringProperty(required=True)
    crib_hand = ndb.StringProperty(required=True)
    ai_hand = ndb.StringProperty(required=True)
    pegging = ndb.StringProperty(required=True)
    upcard = ndb.StringProperty(required=True)
    message = ndb.StringProperty(required=True)

    @classmethod
    def new_game(cls, user):
        """Creates and returns a new game"""

        game = Game(user=user,
                    user_points=0,
                    ai_points=0,
                    game_over=False,
                    history = '',
                    user_hand = '',
                    crib_hand = '',
                    ai_hand = '',
                    pegging = '',
                    dealer = random.choice([True,False]),
                    upcard= '',
                    message='Good luck playing Cribbage!',
                    parent=user)

        game.put()
        return game

    def to_form(self):
        """Returns a GameForm representation of the Game"""
        form = GameForm()
        form.urlsafe_key = self.key.urlsafe()
        form.user_name = self.user.get().name
        form.user_points = self.user_points
        form.ai_points = self.ai_points
        form.game_over = self.game_over
        form.message = self.message
        form.pegging = self.pegging
        form.upcard = self.upcard
        form.user_hand = self.user_hand
        return form

    def end_game(self, won=False):
        """Ends the game - if won is True, the player won. - if won is False,
        the player lost."""
        self.game_over = True
        self.put()
        # Add the game to the score 'board'
        score = Score(user=self.user, date=date.today(), won=won,
                      points=self.user_points)
        score.put()

    def swapDealer(self):
        self.dealer = not self.dealer
        self.put()

    def addHistory(self,add_event):
        self.history += add_event + '\r\n'
        self.put()

    def getHistory(self):
        return self.history

    def score(self,user,points):
        if user == True:
            if self.user_points + points >= 121:
                self.user_points = 121
                self.game_over = True
                self.message += "You have won the game!"
            else:
                self.user_points += points
        else:
            if self.ai_points + points >= 121:
                self.ai_points = 121
                self.game_over = True
                self.message += "The AI wins the game!"
            else:
                self.ai_points += points
        self.put()

        if self.game_over:
            # Add the game to the score 'board'
            score = Score(user=self.user, date=date.today(), won=user,
                          user_points=self.user_points, ai_points=self.ai_points)
            score.put()

    #def game_history(self)
    #    form = GameForm()


class Score(ndb.Model):
    """Score object"""
    user = ndb.KeyProperty(required=True, kind='User')
    date = ndb.DateProperty(required=True)
    won = ndb.BooleanProperty(required=True)
    user_points = ndb.IntegerProperty(required=True)
    ai_points = ndb.IntegerProperty(required=True)

    def to_form(self):
        return ScoreForm(user_name=self.user.get().name, won=self.won,
                         date=str(self.date), user_points=self.user_points,ai_points=self.ai_points)


class GameForm(messages.Message):
    """GameForm for outbound game state information"""
    urlsafe_key = messages.StringField(1, required=True)
    user_points = messages.IntegerField(2, required=True)
    ai_points = messages.IntegerField(3, required=True)
    game_over = messages.BooleanField(4, required=True)
    message = messages.StringField(5, required=True)
    user_name = messages.StringField(6, required=True)
    pegging = messages.StringField(7, required=True)
    upcard = messages.StringField(8, required=True)
    user_hand = messages.StringField(9, required=True)

class GameForms(messages.Message):
    """Return multiple GameForms"""
    items = messages.MessageField(GameForm, 1, repeated=True)


class NewGameForm(messages.Message):
    """Used to create a new game"""
    user_name = messages.StringField(1, required=True)


class MakeMoveForm(messages.Message):
    """Used to make a play in an existing game"""
    play = messages.StringField(1, required=True)


class ScoreForm(messages.Message):
    """ScoreForm for outbound Score information"""
    user_name = messages.StringField(1, required=True)
    date = messages.StringField(2, required=True)
    won = messages.BooleanField(3, required=True)
    user_points = messages.IntegerField(4, required=True)
    ai_points = messages.IntegerField(5, required=True)


class ScoreForms(messages.Message):
    """Return multiple ScoreForms"""
    items = messages.MessageField(ScoreForm, 1, repeated=True)


class StringMessage(messages.Message):
    """StringMessage-- outbound (single) string message"""
    message = messages.StringField(1, required=True)

from distutils.util import strtobool
import random
import datetime
from .constants import ANY_CATEGORY
from django.db import models

from django.db.models import Q, F, FloatField, ExpressionWrapper


class QuestionManager(models.Manager):
    """
    Custom trivia models manager implements 'business logic' for trivia question data.
     Specifically, it provides functions to return randomized QuerySets of of Question Data.
    """

    def get_random_questions(self, qty, difficulty, category=ANY_CATEGORY):
        """Returns a QuerySet of random questions that meet passed criteria"""

        # Generate random indices
        rng_list = self.get_random_indices(qty=qty, difficulty=difficulty, category=category)

        rng_query = Q()

        # Build custom OR query
        for rng in rng_list:
            rng_query.add(Q(pk=rng), Q.OR)

        # Return the Question with randomized id's
        return self.filter(rng_query)

    def get_random_indices(self, qty, difficulty, category):
        """
        Helper function that returns randomized indices of Questions that meet passed criteria
        """

        # Generate random index number of possibilities
        if category == ANY_CATEGORY:
            count = self.filter(difficulty=difficulty).count()
        else:
            count = self.filter(difficulty=difficulty, category=category).count()

        # Special Case - qty exceeds total count of unique questions in db
        safe_qty = qty
        if count < safe_qty:
            safe_qty = count

        # Generate random question pk indices
        rng_list = []
        # for i in range(safe_qty):
        i = 0
        while i < safe_qty:
            # Generate random number
            rng = random.randrange(1, self.last().id)

            # Get next ordered matching question index starting at random index
            try:
                # Any category
                if category == ANY_CATEGORY:
                    # Not unique - already present in list
                    while (rng in rng_list) or (str(self.get(pk=rng).difficulty) != difficulty):
                        # rng = random.randrange(qty)
                        rng = (rng + 1) % (self.last().id + 1)
                        if rng == 0:
                            rng += 1

                # Specific category
                else:
                    # Not unique - does not meet question criteria
                    while (rng in rng_list) or (str(self.get(pk=rng).difficulty) != difficulty) or (
                            str(self.get(pk=rng).category) != category):
                        # Skip index
                        rng = (rng + 1) % (self.last().id + 1)
                        if rng == 0:
                            rng += 1

                # Append valid unique index found
                rng_list.append(rng)
                i += 1

            # Deleted question - does not exist
            except self.model.DoesNotExist:
                # Skip index
                rng = (rng + 1) % (self.last().id + 1)
                if rng == 0:
                    rng += 1

        return rng_list


class TrueFalseManager(models.Manager):
    def get_questions_options(self, question):
        """Returns a shuffled list of answer options"""
        # List of possible answers
        choices = [self.get(question=question).correct_answer,
                   not self.get(question=question).correct_answer]
        random.shuffle(choices)
        # Return shuffled list
        return choices

    def is_correct(self, question, answer):
        """Returns True if passed answer matches correct answer"""
        return self.get(question=question).correct_answer == strtobool(answer.lower())


class MultipleChoiceManager(models.Manager):
    def get_questions_options(self, question):
        """Returns a shuffled list of answer options"""
        # List of possible answers
        choices = [self.get(question=question).correct_answer,
                   self.get(question=question).incorrect_b,
                   self.get(question=question).incorrect_c,
                   self.get(question=question).incorrect_d]
        random.shuffle(choices)
        # Return shuffled list
        return choices

    def is_correct(self, question, answer):
        """Returns True if passed answer matches correct answer"""
        this_mc = self.get(question=question)
        return this_mc.correct_answer == answer


class ScoreManager(models.Manager):
    """Custom manager to access and modify Scores in db"""

    def start(self, user, difficulty):
        """Function records the username, difficulty, and start time for new games"""
        # username = user.get_username()  # parse username from user object

        # Record game start in db
        new_game = self.create(username=user, difficulty=difficulty)
        new_game.save()

        # return pk of game
        return new_game.pk

    def end(self, pk, correct, total):
        """
        Function records the end results of a trivia game based on end datetime,
        number of correct questions, and number of total questions
        """
        game_score = self.get(pk=pk)
        # Record game datetime end and score
        game_score.__setattr__("datetime_end", datetime.datetime.now())
        game_score.__setattr__('questions_correct', correct)
        game_score.__setattr__('total_questions', total)
        game_score.save()
        return game_score

    def get_best_games(self, qty):
        """
        Aggregates the weighted score and orders the results in descending order.
        Returns a QuerySet of the first ordered elements of length(qty). Aggregated
        weighted score attribute can be accessed as 'weighted_score'
        """
        best_games = self.all().exclude(datetime_end=None).annotate(
            weighted_score=ExpressionWrapper(F('questions_correct') * F('difficulty__weight') * 10,
                                             output_field=FloatField())).annotate(
            elapsed=F('datetime_end') - F('datetime_start')
        ).order_by('-weighted_score', 'elapsed')
        return best_games[:qty]

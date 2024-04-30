from django.urls import reverse
from django.test import TestCase
from django.template.loader import render_to_string

class ScoresTests(TestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/scores")
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):  
        response = self.client.get(reverse("Scores"))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):  
        response = self.client.get(reverse("Scores"))
        self.assertTemplateUsed(response, "scores.html")

    def test_template_content(self):
        response = self.client.get(reverse("Scores"))
        self.assertContains(response, render_to_string('scores.html'))

    def test_context_given(self):
        # "expected" context = {
        #     'fixtures': sorted_gamedata,
        #     'isauth': request.user.is_authenticated,
        #     'current_prediction_score': predicted_game.predictionscore if game.matchday < upcoming_matchweek else 0,
        #     'score_accuracy': predicted_game.correct_accuracy if game.matchday < upcoming_matchweek else 0,
        #     'result_accuracy': predicted_game.result_accuracy if game.matchday < upcoming_matchweek else 0,
        #     'is_score_complete': predicted_game.isscorecomplete
        # }
        response = self.client.get('/scores') 
        # Check if the context contains the expected data
        isauth = response.context['isauth']
        self.assertTrue(isinstance(isauth, bool))

        fixtures = response.context['fixtures']
        self.assertTrue(isinstance(fixtures, list))

        current_prediction_score = response.context['current_prediction_score']
        self.assertTrue(isinstance(current_prediction_score, int))

        score_accuracy = response.context['score_accuracy']
        self.assertTrue(isinstance(score_accuracy, int))

        result_accuracy = response.context['result_accuracy']
        self.assertTrue(isinstance(result_accuracy, int))

        is_score_complete = response.context['is_score_complete']
        self.assertTrue(isinstance(is_score_complete, bool))

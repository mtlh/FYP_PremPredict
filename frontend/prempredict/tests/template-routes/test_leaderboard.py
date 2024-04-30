from datetime import date
from django.urls import reverse
from django.test import TestCase
from django.template.loader import render_to_string

class LeaderboardTests(TestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/leaderboard")
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):  
        response = self.client.get(reverse("Leaderboard"))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):  
        response = self.client.get(reverse("Leaderboard"))
        self.assertTemplateUsed(response, "leaderboard.html")

    def test_template_content(self):
        response = self.client.get(reverse("Leaderboard"))
        self.assertContains(response, render_to_string('leaderboard.html'))

    def test_context_given(self):
        # "expected" context = {
        #     'users': userarr,
        #     'isauth': request.user.is_authenticated,
        #     'auth_username': request.user.username,
        #     'ai_record_latestgameweek': ai_latestgameweek,
        #     'ai_record_average_gw_score': ai_record.average_gw_score,
        #     'ai_record_score': ai_record.score,
        #     'ai_record_result_accuracy': ai_record.result_accuracy,
        #     'ai_record_correct_accuracy': ai_record.correct_accuracy,
        #     'ai_record_updated': max(userarr, key=lambda x: x["updated"])["updated"]
        # }
        response = self.client.get('/leaderboard') 

        # Check if the context contains the expected data
        isauth = response.context['isauth']
        self.assertTrue(isinstance(isauth, bool))

        usersarr = response.context['users']
        self.assertTrue(isinstance(usersarr, list))

        username = response.context['auth_username']
        self.assertTrue(isinstance(username, str))

        ai_record_latestgameweek = response.context['ai_record_latestgameweek']
        self.assertTrue(isinstance(ai_record_latestgameweek, int))

        ai_record_average_gw_score = response.context['ai_record_average_gw_score']
        self.assertTrue(isinstance(ai_record_average_gw_score, int))

        ai_record_score = response.context['ai_record_score']
        self.assertTrue(isinstance(ai_record_score, int))

        ai_record_result_accuracy = response.context['ai_record_result_accuracy']
        self.assertTrue(isinstance(ai_record_result_accuracy, int))

        ai_record_correct_accuracy = response.context['ai_record_correct_accuracy']
        self.assertTrue(isinstance(ai_record_correct_accuracy, int))

        ai_record_updated = response.context['ai_record_updated']
        self.assertTrue(isinstance(ai_record_updated, date))

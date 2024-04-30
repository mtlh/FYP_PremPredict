from datetime import date
from django.urls import reverse
from django.test import TestCase
from django.template.loader import render_to_string

class PredictTests(TestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/predict")
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):  
        response = self.client.get(reverse("Predict"))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):  
        response = self.client.get(reverse("Predict"))
        self.assertTemplateUsed(response, "predict.html")

    def test_template_content(self):
        response = self.client.get(reverse("Predict"))
        self.assertContains(response, render_to_string('predict.html'))

    def test_context_given(self):
        # "expected" context = {
        #     'isauth': request.user.is_authenticated,
        #     'matchday': deadlines["matchday"],
        #     'deadline': deadlines["deadline"],
        #     'timetodeadline': deadlines["timetodeadline"],
        #     'current': deadlines["current"],
        #     'baseurl': str(os.environ.get("BASE_URL"))
        # }
        response = self.client.get('/predict') 
        # Check if the context contains the expected data
        isauth = response.context['isauth']
        self.assertTrue(isinstance(isauth, bool))

        matchday = response.context['matchday']
        self.assertTrue(isinstance(matchday, int))

        deadline = response.context['deadline']
        self.assertTrue(isinstance(deadline, date))

        timetodeadline = response.context['timetodeadline']
        self.assertTrue(isinstance(timetodeadline, str))

        current = response.context['current']
        self.assertTrue(isinstance(current, date))

        baseurl = response.context['baseurl']
        self.assertTrue(isinstance(baseurl, str))

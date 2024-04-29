from django.urls import reverse
from django.test import TestCase
from django.template.loader import render_to_string

class HomePageTests(TestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):  
        response = self.client.get(reverse("Home"))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):  
        response = self.client.get(reverse("Home"))
        self.assertTemplateUsed(response, "home.html")

    def test_template_content(self):
        response = self.client.get(reverse("Home"))
        self.assertContains(response, render_to_string('home.html'))

    def test_context_given(self):
        response = self.client.get('/') 
        # Check if the context contains the expected data
        isauth = response.context['isauth']
        self.assertTrue(isinstance(isauth, bool))

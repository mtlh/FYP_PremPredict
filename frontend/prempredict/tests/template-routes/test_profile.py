from django.urls import reverse
from django.test import TestCase
from django.template.loader import render_to_string

class ProfileTests(TestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/profile")
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):  
        response = self.client.get(reverse("Profile"))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):  
        response = self.client.get(reverse("Profile"))
        self.assertTemplateUsed(response, "profile.html")

    def test_template_content(self):
        response = self.client.get(reverse("Profile"))
        self.assertContains(response, render_to_string('profile.html'))

    def test_context_given(self):
        response = self.client.get('/profile') 
        # Check if the context contains the expected data
        isauth = response.context['isauth']
        self.assertTrue(isinstance(isauth, bool))
        predictions_made = response.context['predictions_made']
        self.assertTrue(isinstance(predictions_made, str))
        username = response.context['username']
        self.assertTrue(isinstance(username, str))

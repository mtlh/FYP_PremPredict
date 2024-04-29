from django.urls import reverse
from django.test import TestCase
from django.template.loader import render_to_string

class TablePageTests(TestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/table/")
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):  
        response = self.client.get(reverse("Table"))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):  
        response = self.client.get(reverse("Table"))
        self.assertTemplateUsed(response, "table.html")

    def test_template_content(self):
        response = self.client.get(reverse("Table"))
        self.assertContains(response, render_to_string('table.html'))

    def test_context_given(self):
        response = self.client.get('/table/') 
        # Check if the context contains the expected data
        tablearr = response.context['tabledata']
        self.assertTrue(isinstance(tablearr, list))
        isauth = response.context['isauth']
        self.assertTrue(isinstance(isauth, bool))

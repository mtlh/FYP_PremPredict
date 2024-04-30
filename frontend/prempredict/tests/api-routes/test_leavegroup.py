from django.test import Client, TestCase
from django.contrib.auth.models import User
from django.urls import reverse

class LeaveGroupApiEndpoint(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = Client()
        self.client.get('/load/api')
        self.client.get('/load/table/teams')
        self.client.get('/load/game/1/4/')
        self.client.get('/load/game/5/9/')
        self.client.get('/load/game/10/14/')
        self.client.get('/load/game/15/19/')
        self.client.get('/load/game/20/24/')
        self.client.get('/load/game/25/29/')
        self.client.get('/load/game/30/34/')
        self.client.get('/load/game/35/38/')
        
    def test_url_exists_at_correct_location(self):
        response = self.client.post("/leaderboard/leave")
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):  
        response = self.client.post(reverse("Leave A Custom Leaderboard"))
        self.assertEqual(response.status_code, 200)

    def test_endpoint_sucess_case(self):
        # Existing group
        invitelink = "rfv4jshwy3tbeu1jsxt96ef7v"
        formdata_example = dict()
        formdata_example["invitelink"] = invitelink

        self.client.login(username='testuser', password='testpassword')
        response = self.client.post('/leaderboard/join', formdata_example)
        response = self.client.post('/leaderboard/leave', formdata_example)
        
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.content, bytes)
        self.assertEqual(response.content.decode('utf-8'), 'Left group!')

    def test_endpoint_incorrect_inv(self):
        invitelink = "wronglink"
        formdata_example = dict()
        formdata_example["invitelink"] = invitelink
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post('/leaderboard/leave', formdata_example)
        
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.content, bytes)
        self.assertEqual(response.content.decode('utf-8'), 'You are not part of this group.')

    def test_endpoint_no_auth(self):
        invitelink = "rfv4jshwy3tbeu1jsxt96ef7v"
        formdata_example = dict()
        formdata_example["invitelink"] = invitelink
        response = self.client.post('/leaderboard/leave', formdata_example)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.content, bytes)
        self.assertEqual(response.content.decode('utf-8'), 'User not authenticated.')


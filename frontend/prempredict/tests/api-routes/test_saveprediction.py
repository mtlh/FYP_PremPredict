import random
from django.test import Client, TestCase
from django.contrib.auth.models import User
from prempredict.models import PremGames
from prempredict.views.functions.getGameweekDeadlines import getGameweekDeadline
from django.urls import reverse

class SavePredictApiEndpoint(TestCase):

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
        response = self.client.post("/predict/save")
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):  
        response = self.client.post(reverse("Save User Prediction"))
        self.assertEqual(response.status_code, 200)

    def test_endpoint_sucess_case(self):
        currentMatchday = getGameweekDeadline()["matchday"]
        games = PremGames.objects.filter(matchday=currentMatchday).all()
        formdata_example = dict()
        for game in games:
            formdata_example["homescore"+str(game.matchid)] = random.randint(1, 5)
            formdata_example["awayscore"+str(game.matchid)] = random.randint(1, 5)

        self.client.login(username='testuser', password='testpassword')
        response = self.client.post('/predict/save', formdata_example)
        
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.content, bytes)
        self.assertEqual(response.content.decode('utf-8'), 'Updated your predictions!')

    def test_endpoint_no_auth(self):
        currentMatchday = getGameweekDeadline()["matchday"]
        games = PremGames.objects.filter(matchday=currentMatchday).all()
        formdata_example = dict()
        for game in games:
            formdata_example["homescore"+str(game.matchid)] = random.randint(1, 5)
            formdata_example["awayscore"+str(game.matchid)] = random.randint(1, 5)

        response = self.client.post('/predict/save', formdata_example)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.content, bytes)
        self.assertEqual(response.content.decode('utf-8'), 'User not authenticated')

    def test_endpoint_no_param(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post('/predict/save')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.content, bytes)
        self.assertEqual(response.content.decode('utf-8'), 'Please provide some data')

    def test_endpoint_empty_param(self):
        formdata_example = dict()
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post('/predict/save', formdata_example)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.content, bytes)
        self.assertEqual(response.content.decode('utf-8'), 'Given data is invalid')

    def test_endpoint_invalid_param(self):
        formdata_example = "test"
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post('/predict/save', formdata_example)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.content, bytes)
        self.assertEqual(response.content.decode('utf-8'), 'Given data is invalid')

    def test_endpoint_incomplete_games(self):
        currentMatchday = getGameweekDeadline()["matchday"]
        games = PremGames.objects.filter(matchday=currentMatchday).all()
        formdata_example = dict()
        for game in games:
            formdata_example["homescore"+str(game.matchid)] = random.randint(1, 5)
            formdata_example["awayscore"+str(game.matchid)] = random.randint(1, 5)
        formdata_example["awayscore"+str(game.matchid)] = ""

        self.client.login(username='testuser', password='testpassword')
        response = self.client.post('/predict/save', formdata_example)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.content, bytes)
        self.assertEqual(response.content.decode('utf-8'), 'Please refresh to get the newest games and try again.')


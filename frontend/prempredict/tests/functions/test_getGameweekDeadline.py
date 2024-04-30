from datetime import datetime
from django.utils import timezone
import pytz
from django.test import Client, TestCase
from django.contrib.auth.models import User
from prempredict.models import PremSeasonInfo, PremGameweeks
from prempredict.views.functions.getGameweekDeadlines import getGameweekDeadline


class GameweekDeadlineFunction(TestCase):

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

    # Function returns to test:
    # 'matchday': currentMatchday
    # 'deadline': deadline_datetime
    # 'timetodeadline': f"{int(days)}:{int(hours)}:{int(total_seconds // 60)} dd:hh:mm"
    # 'current': current_datetime

    def test_function_matchday(self):
        currentMatchdayTest = PremSeasonInfo.objects.filter(active=True).get().currentMatchday
        deadline_datetime = datetime.strptime(str(PremGameweeks.objects.filter(number=currentMatchdayTest).get().deadline), '%Y-%m-%d %H:%M:%S%z').astimezone(pytz.timezone('Europe/London'))
        current_datetime = timezone.now().astimezone(pytz.timezone('Europe/London'))
        while current_datetime >= deadline_datetime:
            currentMatchdayTest += 1
            deadline_datetime = datetime.strptime(str(PremGameweeks.objects.filter(number=currentMatchdayTest).get().deadline), '%Y-%m-%d %H:%M:%S%z').astimezone(pytz.timezone('Europe/London'))
        currentMatchday = getGameweekDeadline()["matchday"]
        self.assertEqual(currentMatchdayTest, currentMatchday)

    def test_function_deadline(self):
        # Find deadline that matches the returned gameweek
        currentMatchday = getGameweekDeadline()["matchday"]
        deadline_datetime = datetime.strptime(str(PremGameweeks.objects.filter(number=currentMatchday).get().deadline), '%Y-%m-%d %H:%M:%S%z').astimezone(pytz.timezone('Europe/London'))
        self.assertEqual(getGameweekDeadline()["deadline"], deadline_datetime)

    def test_function_timetodeadline(self):
        current_datetime = timezone.now().astimezone(pytz.timezone('Europe/London'))
        total_seconds = (getGameweekDeadline()["deadline"] - current_datetime).total_seconds()
        days = total_seconds // 86400
        total_seconds %= 86400
        hours = total_seconds // 3600
        total_seconds %= 3600
        self.assertEqual(getGameweekDeadline()["timetodeadline"], f"{int(days)}:{int(hours)}:{int(total_seconds // 60)} dd:hh:mm")

    def test_function_current(self):
        current_datetime = timezone.now().astimezone(pytz.timezone('Europe/London'))
        self.assertEqual(getGameweekDeadline()["current"], current_datetime)


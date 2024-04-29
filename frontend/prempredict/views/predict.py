import os
from django.shortcuts import render
from django.views import View
from prempredict.views.functions.getGameweekDeadlines import getGameweekDeadline
from prempredict.models import PremGames, UserPrediction, AlgorithmPrediction

class PredictHuman(View):
    def get(self, request, *args, **kwargs):
        currentMatchday = getGameweekDeadline()["matchday"]
        games = PremGames.objects.filter(matchday=currentMatchday).exclude(status="POSTPONED")

        if request.user.is_authenticated:
            user_id = request.user.id
            try:
                user_scores = UserPrediction.objects.filter(gameweek=currentMatchday, user_id=user_id).get().scores
            except UserPrediction.DoesNotExist:
                user_scores = {}
        else:
            user_scores = {}

        gamedata = []
        for fixture in games:
            appendarr = {
                "id": fixture.matchid,
                "hometeamname": fixture.hometeam.initals,
                "hometeambadge": fixture.hometeam.badge,
                "hometeamscore": 0,
                "awayteamname": fixture.awayteam.initals,
                "awayteambadge": fixture.awayteam.badge,
                "awayteamscore": 0,
                "date": fixture.date,
                "status": fixture.status
            }
            if str(fixture.matchid) in user_scores:
                appendarr["awayteamscore"] = user_scores.get(str(fixture.matchid)).get("away")
                appendarr["hometeamscore"] = user_scores.get(str(fixture.matchid)).get("home")               
            gamedata.append(appendarr)
            
        context = {
            'fixtures': sorted(gamedata, key=lambda x: x["date"]),
        }
        return render(request, 'predict/humanpredict.html', context)

class PredictAI(View):
    def get(self, request, *args, **kwargs):
        currentMatchday = getGameweekDeadline()["matchday"]
        games = PremGames.objects.filter(matchday=currentMatchday).exclude(status="POSTPONED")

        try:
            ai_scores = AlgorithmPrediction.objects.filter(gameweek=currentMatchday).get().scores
        except AlgorithmPrediction.DoesNotExist:
            ai_scores = {}

        gamedata = []
        for fixture in games:
            appendarr = {
                "id": fixture.matchid,
                "hometeamname": fixture.hometeam.initals,
                "hometeambadge": fixture.hometeam.badge,
                "hometeamscore": 0,
                "awayteamname": fixture.awayteam.initals,
                "awayteambadge": fixture.awayteam.badge,
                "awayteamscore": 0,
                "date": fixture.date,
                "status": fixture.status
            }
            if str(fixture.matchid) in ai_scores:
                appendarr["awayteamscore"] = ai_scores.get(str(fixture.matchid)).get("away")
                appendarr["hometeamscore"] = ai_scores.get(str(fixture.matchid)).get("home")               
            gamedata.append(appendarr)
            
        context = {
            'fixtures': sorted(gamedata, key=lambda x: x["date"]),
        }
        return render(request, 'predict/aipredict.html', context)
    
class PredictMain(View):
    def get(self, request, *args, **kwargs):
        deadlines = getGameweekDeadline()
        context = {
            'isauth': request.user.is_authenticated,
            'matchday': deadlines["matchday"],
            'deadline': deadlines["deadline"],
            'timetodeadline': deadlines["timetodeadline"],
            'current': deadlines["current"],
            'baseurl': str(os.environ.get("BASE_URL"))
        }
        return render(request, 'predict/predict.html', context)


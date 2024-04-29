from uuid import UUID
from django.views.generic import View
from ..models import *
from django.shortcuts import render
from django.db.models import Q

class Home(View):
    def get(self, request, *args, **kwargs):
        context = {
            'isauth': request.user.is_authenticated
        }
        return render(request, 'home.html',  context)
    
class RecentResults(View):
    def get(self, request, *args, **kwargs):

        upcoming_games = PremGames.objects.filter(status="FINISHED").order_by("-date")[:4]
        gamedata = []
        for game in upcoming_games:
            append_items = {
                "hometeamname": game.hometeam.initals,
                "hometeambadge": game.hometeam.badge,
                "hometeamscore": game.score_hometeam,
                "awayteamname": game.awayteam.initals,
                "awayteambadge": game.awayteam.badge,
                "awayteamscore": game.score_awayteam,
                "date": game.date.strftime('%d %b %Y, %H:%M'),
                "status": game.status
            }
            if request.user.is_authenticated:
                try:
                    predicted_game = UserPrediction.objects.get(gameweek=game.matchday, user_id=str(request.user.id))
                    for key, value in predicted_game.scores.items():
                        if UUID(key) == game.matchid:
                            append_items["prediction_home"] = value["home"]
                            append_items["prediction_away"] = value["away"]
                            append_items["prediction_score"] = value["score"]
                except:
                    scores_not_yet_updated = True
            gamedata.append(append_items)
        context = {
            'fixtures': gamedata,
            'isauth': request.user.is_authenticated
        }
        return render(request, './recent_results.html',  context)
    
class UpcomingFixtures(View):
    def get(self, request, *args, **kwargs):

        upcoming_games = PremGames.objects.exclude(Q(status="FINISHED") | Q(status="POSTPONED")).order_by("date")[:4]
        gamedata = []
        for game in upcoming_games:
            append_items = {
                "hometeamname": game.hometeam.initals,
                "hometeambadge": game.hometeam.badge,
                "hometeamscore": game.score_hometeam,
                "awayteamname": game.awayteam.initals,
                "awayteambadge": game.awayteam.badge,
                "awayteamscore": game.score_awayteam,
                "date": game.date.strftime('%d %b %Y, %H:%M'),
                "status": game.status
            }
            if request.user.is_authenticated:
                try:
                    predicted_game = UserPrediction.objects.get(gameweek=game.matchday, user_id=str(request.user.id))
                    for key, value in predicted_game.scores.items():
                        if UUID(key) == game.matchid:
                            append_items["prediction_home"] = value["home"]
                            append_items["prediction_away"] = value["away"]
                except:
                    scores_not_yet_updated = True
            gamedata.append(append_items)
        context = {
            'fixtures': gamedata,
            'isauth': request.user.is_authenticated
        }
        return render(request, './upcoming_fixtures.html',  context)
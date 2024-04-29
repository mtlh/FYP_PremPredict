from uuid import UUID
from django.views.generic import View
import os
from ..models import PremGames, UserPrediction, PremSeasonInfo, AlgorithmPrediction
from django.shortcuts import render
from prempredict.views.functions.getGameweekDeadlines import getGameweekDeadline


class ScoresGameweek(View):
    def get(self, request, *args, **kwargs):
        matchweek = request.GET.get("gameweek")
        usertype = request.GET.get("type")
        try: 
            matchweek = int(matchweek)
        except:
            context = {
                'fixtures': [],
                'isauth': request.user.is_authenticated
            }
            return render(request, './fixtures/fixtureGameweek.html',  context)
        
        class PredictedGame:
            def __init__(self, predictionscore='', correct_accuracy='', result_accuracy='', isscorecomplete=False):
                self.predictionscore = predictionscore
                self.correct_accuracy = correct_accuracy
                self.result_accuracy = result_accuracy
                self.isscorecomplete = isscorecomplete

        matchweek_games = PremGames.objects.filter(matchday=matchweek).exclude(status="POSTPONED")
        upcoming_matchweek = getGameweekDeadline()["matchday"]
        gamedata = []
        for game in matchweek_games:
            if game.status == "FINISHED":
                append_items = {
                    "hometeamname": game.hometeam.initals,
                    "hometeambadge": game.hometeam.badge,
                    "hometeamscore": game.score_hometeam,
                    "awayteamname": game.awayteam.initals,
                    "awayteambadge": game.awayteam.badge,
                    "awayteamscore": game.score_awayteam,
                    "date": game.date,
                    "status": game.status
                }
            else:
                append_items = {
                    "hometeamname": game.hometeam.initals,
                    "hometeambadge": game.hometeam.badge,
                    "hometeamscore": "",
                    "awayteamname": game.awayteam.initals,
                    "awayteambadge": game.awayteam.badge,
                    "awayteamscore": "",
                    "date": game.date,
                    "status": game.status
                }

            if request.user.is_authenticated and usertype == "human":
                try:
                    predicted_game = UserPrediction.objects.get(gameweek=game.matchday, user_id=str(request.user.id))
                    for key, value in predicted_game.scores.items():
                        if UUID(key) == game.matchid:
                            if (game.status == "FINISHED"):
                                try:
                                    append_items["prediction_home"] = value["home"]
                                    append_items["prediction_away"] = value["away"]
                                    append_items["prediction_score"] = value["score"]
                                except:
                                    scores_not_yet_updated = True
                            else:
                                append_items["prediction_home"] = value["home"]
                                append_items["prediction_away"] = value["away"]
                                append_items["hometeamscore"] = ""
                                append_items["awayteamscore"] = ""
                except:
                    predicted_game = PredictedGame()
            
            elif usertype == "algor":
                try:
                    predicted_game = AlgorithmPrediction.objects.get(gameweek=game.matchday)
                    for key, value in predicted_game.scores.items():
                        if UUID(key) == game.matchid:
                            if game.status == "FINISHED":
                                try:
                                    append_items["prediction_home"] = value["home"]
                                    append_items["prediction_away"] = value["away"]
                                    append_items["prediction_score"] = value["score"]
                                except:
                                    scores_not_yet_updated = True
                            else:
                                append_items["prediction_home"] = value["home"]
                                append_items["prediction_away"] = value["away"]
                                append_items["hometeamscore"] = ""
                                append_items["awayteamscore"] = ""
                except:
                    predicted_game = PredictedGame()
            
            else:
                predicted_game = PredictedGame()
                if game.status != "FINISHED":
                    append_items["hometeamscore"] = ""
                    append_items["awayteamscore"] = ""

            gamedata.append(append_items)

        sorted_gamedata = sorted(gamedata, key=lambda x: x["date"])
        context = {
            'fixtures': sorted_gamedata,
            'isauth': request.user.is_authenticated,
            'current_prediction_score': predicted_game.predictionscore if game.matchday < upcoming_matchweek else 0,
            'score_accuracy': predicted_game.correct_accuracy if game.matchday < upcoming_matchweek else 0,
            'result_accuracy': predicted_game.result_accuracy if game.matchday < upcoming_matchweek else 0,
            'is_score_complete': predicted_game.isscorecomplete
        }
        return render(request, './scores/scoresGameweek.html',  context)
    
class ScoresMain(View):
    def get(self, request, *args, **kwargs):
        currentMatchday = PremSeasonInfo.objects.get(active=True).currentMatchday
        context = {
            'currentMatchday': currentMatchday,
            'baseurl': str(os.environ.get("BASE_URL")),
            'isauth': request.user.is_authenticated
        }
        return render(request, './scores/scores.html',  context)
    
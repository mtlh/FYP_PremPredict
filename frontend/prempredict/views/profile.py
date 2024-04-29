import os
from django.shortcuts import render
from django.views import View
from .functions.getGameweekDeadlines import getGameweekDeadline
from ..models import Leaderboard, PremGames, UserPrediction
from dotenv import load_dotenv
from mailjet_rest import Client
from django.db.models import Q

class Profile(View):
    def get(self, request, *args, **kwargs):
        currentMatchweek = getGameweekDeadline()["matchday"]
        if request.user.is_authenticated:
            leaderboard_record = Leaderboard.objects.get(user=request.user)
            user_predictions = UserPrediction.objects.filter(user=request.user).order_by('-predictionscore')
            highestprediction = user_predictions.first()
            latestprediction = user_predictions.order_by("-gameweek").exclude(Q(predictionscore=0) | Q(predictionscore=None)).first()
            context = {
                'isauth': request.user.is_authenticated,
                'username': request.user.username,
                'predictions_made': str(user_predictions.count())+"/"+str(currentMatchweek),
                'predictions_correct': leaderboard_record.correct_accuracy,
                'season_score': leaderboard_record.score,
                'latest_score': latestprediction.predictionscore,
                'latest_gw': latestprediction.gameweek,
                'highest_score': highestprediction.predictionscore,
                'highest_gw': highestprediction.gameweek,
                'overall_position': leaderboard_record.position,
            }
        else:
            context = {
                'isauth': request.user.is_authenticated,
                'username': request.user.username,
                'predictions_made': "0/"+str(currentMatchweek),
            }
        return render(request, 'profile/main.html',  context)
    
    def post(self, request, *args, **kwargs):

        load_dotenv()
        api_key = os.environ['MJ_APIKEY_PUBLIC']
        api_secret = os.environ['MJ_APIKEY_PRIVATE']
        mailjet = Client(auth=(api_key, api_secret), version='v3.1')
        data = {
            'Messages': [
                {
                    "From": {
                        "Email": "matthewtlharvey88@gmail.com",
                        "Name": "PremPredict"
                    },
                    "To": [
                        {
                            "Email": "matthewtlharvey@gmail.com",
                            "Name": "Main"
                        }
                    ],
                    "Subject": "Support ticket - " + str(request.POST.get('email')), 
                    "TextPart": "Name: " + str(request.POST.get('firstname')) + " " + str(request.POST.get('lastname')) + " Message: " + str(request.POST.get('msg')),
                    "HTMLPart": "<h2>Name: " + str(request.POST.get('firstname')) + " " + str(request.POST.get('lastname')) + "</h2><br /><h3> Message: " + str(request.POST.get('msg')) + "</h3>"
                }
            ]
        }
        result = mailjet.send.create(data=data)
        # print(result.json())

        # resend.api_key = str(os.environ['RESEND_KEY'])
        # r = resend.Emails.send({
        # "from": str(request.POST.get('email')),
        # "to": "matthewtlharvey@gmail.com",
        # "subject": "PremPredict Support - " + str(request.POST.get('firstname')) + " " + str(request.POST.get('lastname')),
        # "html": "<p>" + str(request.POST.get('msg')) + "</p>"
        # })

        currentMatchweek = getGameweekDeadline()["matchday"]
        if request.user.is_authenticated:
            leaderboard_record = Leaderboard.objects.get(user=request.user)
            user_predictions = UserPrediction.objects.filter(user=request.user)
            context = {
                'isauth': request.user.is_authenticated,
                'username': request.user.username,
                'predictions_made': str(user_predictions.count())+"/"+str(currentMatchweek),
                'predictions_correct': leaderboard_record.correct_accuracy,
                'season_score': leaderboard_record.score,
                'overall_position': leaderboard_record.position,
                'support_msg': "Message sent. We will get back to you when possible."
            }
        else:
            context = {
                'isauth': request.user.is_authenticated,
                'username': request.user.username,
                'predictions_made': "0/"+str(currentMatchweek),
                'support_msg': "Message sent. We will get back to you when possible."
            }
        return render(request, 'profile/main.html',  context)
    
class ProfileTable(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user_predictions = UserPrediction.objects.filter(user=request.user)
            match_ids = set()
            for prediction in user_predictions:
                match_ids.update(prediction.scores.keys())
            games = PremGames.objects.filter(matchid__in=match_ids)
            team_info = {}
            for game in games:
                away_team_name = game.awayteam.initals
                if away_team_name not in team_info:
                    team_info[away_team_name] = {'pts': 0, 'p': 0, 'w': 0, 'd': 0, 'l': 0, 'gd': 0, 'badge': game.awayteam.badge}
            games_dict = {str(game.matchid): game for game in games}
            for prediction in user_predictions:
                for match_id, score in prediction.scores.items():
                    game = games_dict.get(match_id)
                    if game:
                        if score["home"] > score["away"]:
                            team_info[game.hometeam.initals]["pts"] += 3
                            team_info[game.hometeam.initals]["w"] += 1
                            team_info[game.awayteam.initals]["l"] += 1
                            team_info[game.hometeam.initals]["gd"] += score["home"] - score["away"]; team_info[game.awayteam.initals]["gd"] -= score["home"] - score["away"]
                        elif score["home"] == score["away"]:
                            team_info[game.hometeam.initals]["pts"] += 1
                            team_info[game.awayteam.initals]["pts"] += 1
                            team_info[game.hometeam.initals]["d"] += 1
                            team_info[game.awayteam.initals]["d"] += 1
                        else:
                            team_info[game.awayteam.initals]["pts"] += 3
                            team_info[game.awayteam.initals]["w"] += 1
                            team_info[game.hometeam.initals]["l"] += 1
                            team_info[game.awayteam.initals]["gd"] += score["away"] - score["home"]; team_info[game.hometeam.initals]["gd"] -= score["away"] - score["home"]
                        team_info[game.hometeam.initals]["p"] += 1
                        team_info[game.awayteam.initals]["p"] += 1
            sorted_teams = sorted(team_info.items(), key=lambda item: item[1]['pts'], reverse=True)
            for position, (team_name, info) in enumerate(sorted_teams, start=1):
                info['position'] = position
            context = {
                'isauth': request.user.is_authenticated,
                'username': request.user.username,
                'tabledata': dict(sorted_teams)
            }
        else:
            context = {
                'isauth': request.user.is_authenticated,
                'username': request.user.username,
            }
        return render(request, 'profile/table.html',  context)
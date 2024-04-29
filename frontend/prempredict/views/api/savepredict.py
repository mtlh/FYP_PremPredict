from django.utils import timezone
import html
from django.http import HttpResponse
from django.views.generic import View
from prempredict.views.functions.sanitzeString import cleanString
from prempredict.views.functions.getGameweekDeadlines import getGameweekDeadline
from prempredict.models import UserPrediction, PremGames

class SavePrediction(View):
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user_id = request.user.id
        else:
            return HttpResponse("User not authenticated", status=200)

        cleaned_data = {}
        try:
            for key, value in request.POST.items():
                cleaned_data[cleanString(key)] = int(cleanString(value))
        except:
            return HttpResponse(f"Given data is invalid", status=200)

        if cleaned_data == {}:
            return HttpResponse(f"Please provide some data", status=200)
        
        filtered_data = {key: value for key, value in cleaned_data.items() if key.startswith("awayscore") or key.startswith("homescore")}

        merged_data = {}
        for key, value in filtered_data.items():
            team_identifier = key.split('score')[1]
            if team_identifier not in merged_data:
                merged_data[team_identifier] = {'home': 0, 'away': 0}
            if key.startswith('homescore'):
                merged_data[team_identifier]['home'] += value
            elif key.startswith('awayscore'):
                merged_data[team_identifier]['away'] += value

        currentMatchday = getGameweekDeadline()["matchday"]
        matchdayGames = PremGames.objects.filter(matchday=currentMatchday)
        gameid_arr = []
        for game in matchdayGames:
            gameid_arr.append(str(game.matchid))

        # Check that mergeddata has the correct matchids
        for match in merged_data:
            if match in gameid_arr:
                gameid_arr.remove(match)
                
        if len(gameid_arr) == 0:
            obj, created = UserPrediction.objects.update_or_create(
                user_id=user_id,
                gameweek=currentMatchday,
                defaults={
                    "scores": merged_data
                }
            )
            if not created:
                UserPrediction.objects.filter(
                    user_id=user_id,
                    gameweek=currentMatchday,
                ).update(
                    scores = merged_data,
                    date = timezone.now()
                )

            return HttpResponse(f"Updated your predictions!", status=200)
        else:
            return HttpResponse(f"Please refresh to get the newest games and try again.", status=200)
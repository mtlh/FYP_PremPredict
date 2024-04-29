from django.http import HttpResponse
from django.views.generic import View
from ..functions.getGameweekDeadlines import getGameweekDeadline
from ...models import AdminOnly, PremGames, UserPrediction
import requests
from django.utils import timezone

class UpdateUserScores(View):
    def get(self, request, *args, **kwargs):
        try:
            
            # Get User Predictions (isscorecomplete is false)
            admin_only_instance = AdminOnly.objects.get()
            random_start_index = admin_only_instance.user_score_update
            predictions = UserPrediction.objects.filter(isscorecomplete=False).exclude(gameweek__gte=getGameweekDeadline()["matchday"])[random_start_index:random_start_index+50]
            if len(predictions) == 0:
                random_start_index = 0

            current_index = 0
            while current_index < len(predictions):
                gameweek_score = 0
                prediction_json = {}
                is_all_finished = True
                completed_games = 0
                result_accuracy = 0
                score_accuracy = 0
                
                for key, value in predictions[current_index].scores.items():
                    game = PremGames.objects.get(matchid=key)
                    # Score against prediction
                    local_score = 0
                    if (game.status != "FINISHED" and game.status != "POSTPONED"):
                        is_all_finished = False
                    elif (game.status == "POSTPONED"):
                        skip_game = True
                    else:
                        completed_games+=1
                        # 5 points check
                        if value['home'] == game.score_hometeam and value['away'] == game.score_awayteam:
                            gameweek_score+=5
                            local_score = 5
                            result_accuracy+=1
                            score_accuracy+=1
                        # 2 points checks
                        elif value['home'] > value['away'] and game.score_hometeam > game.score_awayteam:
                            gameweek_score+=2
                            local_score = 2
                            result_accuracy+=1
                        elif value['home'] < value['away'] and game.score_hometeam < game.score_awayteam:
                            gameweek_score+=2
                            local_score = 2
                            result_accuracy+=1
                        elif value['home'] == value['away'] and game.score_hometeam == game.score_awayteam:
                            gameweek_score+=2
                            local_score = 2
                            result_accuracy+=1
                    prediction_json[key] = {'away': value['away'], 'home': value['home'], 'score': local_score}

                predictions[current_index].predictionscore = gameweek_score
                predictions[current_index].scores = prediction_json
                predictions[current_index].result_accuracy = (result_accuracy/completed_games)*100 if completed_games > 0 else 0
                predictions[current_index].correct_accuracy = (score_accuracy/completed_games)*100 if completed_games > 0 else 0
                predictions[current_index].score_check_time = timezone.now()
                if is_all_finished:
                    predictions[current_index].isscorecomplete = True
                predictions[current_index].save()
                current_index+=1

            admin_only_instance.user_score_update = random_start_index+len(predictions)
            admin_only_instance.save()
            # Return current stored information
            return HttpResponse("Updated User scores.", status=200)
        
        except requests.exceptions.RequestException as e:
            # Handle any request-related errors here
            return HttpResponse(str(e), status=400)
      
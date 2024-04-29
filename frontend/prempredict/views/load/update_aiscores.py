from django.http import HttpResponse
from django.views.generic import View
from ...models import AILeaderboard, PremGames, AlgorithmPrediction
import requests
from ..functions.getGameweekDeadlines import getGameweekDeadline
from django.utils import timezone

class UpdateAIScores(View):
    def get(self, request, *args, **kwargs):
        try:
            
            # Get User Predictions (isscorecomplete is false) ... isscorecomplete=False
            predictions = AlgorithmPrediction.objects.filter().exclude(gameweek__gte=getGameweekDeadline()["matchday"]).order_by('score_check_time')

            random_start_index = 0
            while len(predictions) > random_start_index:
                gameweek_score = 0
                prediction_json = {}
                is_all_finished = True
                completed_games = 0
                result_accuracy = 0
                score_accuracy = 0
                for key, value in predictions[random_start_index].scores.items():
                    game = PremGames.objects.get(matchid=key)
                    # Score against prediction
                    local_score = 0

                    if (game.status != "FINISHED"):
                        is_all_finished = False
                    elif (game.status == "POSTPONED"):
                        skip_game = True
                    else:
                        #print([value['home'], value['away'], ' ', game.score_hometeam, game.score_awayteam, value['home'] == game.score_hometeam and value['away'] == game.score_awayteam])
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

                        completed_games+=1
                    prediction_json[key] = {'away': value['away'], 'home': value['home'], 'score': local_score}

                predictions[random_start_index].predictionscore = gameweek_score
                predictions[random_start_index].scores = prediction_json
                predictions[random_start_index].result_accuracy = (result_accuracy/completed_games)*100 if completed_games > 0 else 0
                predictions[random_start_index].correct_accuracy = (score_accuracy/completed_games)*100 if completed_games > 0 else 0
                predictions[random_start_index].score_check_time = timezone.now()
                if is_all_finished:
                    predictions[random_start_index].isscorecomplete = True
                predictions[random_start_index].save()
                random_start_index+=1

            # Return current stored information
            return HttpResponse("Updated AI scores.", status=200)
        
        except requests.exceptions.RequestException as e:
            # Handle any request-related errors here
            return HttpResponse(str(e), status=400)
      
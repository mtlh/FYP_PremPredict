from django.http import HttpResponse
from ..functions.getGameweekDeadlines import getGameweekDeadline
from django.views.generic import View
from ...models import AILeaderboard, AlgorithmPrediction, Leaderboard, UserPrediction, AdminOnly
import requests
from django.utils import timezone

class UpdateLeaderboard(View):
    def get(self, request, *args, **kwargs):
        try:
            
            # USER PREDICTION LEADERBOARD 

            # 1. per user combine all prediction scores.
            currentgameweek = getGameweekDeadline()["matchday"]
            leadboard_records = Leaderboard.objects.all()
            admin_only_instance = AdminOnly.objects.get()
            random_start_index = admin_only_instance.user_leaderboard_update
            if len(leadboard_records) <= random_start_index:
                random_start_index = 0
                admin_only_instance.user_leaderboard_update = 0

            while len(leadboard_records) > random_start_index and random_start_index < admin_only_instance.user_leaderboard_update+25:
                user_predictions = UserPrediction.objects.filter(user=leadboard_records[random_start_index].user).exclude(gameweek__gte=currentgameweek)
                overall_score = 0
                result_accuracy = 0
                score_accuracy = 0
                # 2. Add averages and accuracy % to leaderboard user record.
                for prediction in user_predictions:
                    if prediction.predictionscore:
                        overall_score += prediction.predictionscore
                    if prediction.result_accuracy:
                        result_accuracy += prediction.result_accuracy
                    if prediction.correct_accuracy:
                        score_accuracy += prediction.correct_accuracy
                Leaderboard.objects.filter(user=leadboard_records[random_start_index].user).update(
                    score= overall_score,
                    average_gw_score= overall_score/len(user_predictions) if user_predictions else 0,
                    result_accuracy= result_accuracy/len(user_predictions) if user_predictions else 0,
                    correct_accuracy= score_accuracy/len(user_predictions) if user_predictions else 0,
                    user_recent_update= timezone.now()
                )


                random_start_index+=1

            admin_only_instance.user_leaderboard_update = random_start_index
            admin_only_instance.save()

            # 3. Allocate positions based on overall scores.
            position = admin_only_instance.position_leaderboard_update
            if position >= leadboard_records.count():
                position = 0
            current_leaderboard = leadboard_records.order_by('-score')[position:position+25]
            for leaderboard in current_leaderboard:
                Leaderboard.objects.filter(user=leaderboard.user).update(position=position+1)
                position += 1
            admin_only_instance.position_leaderboard_update = position
            admin_only_instance.save()

            # AI PREDICTION LEADERBOARD
            ai_predictions = AlgorithmPrediction.objects.all().exclude(gameweek__gte=currentgameweek)
            overall_score = 0
            result_accuracy = 0
            score_accuracy = 0
            for prediction in ai_predictions:
                if prediction.predictionscore:
                    overall_score += prediction.predictionscore
                if prediction.result_accuracy:
                    result_accuracy += prediction.result_accuracy
                if prediction.correct_accuracy:
                    score_accuracy += prediction.correct_accuracy
            AILeaderboard.objects.filter(getval=1).update(
                score= overall_score,
                average_gw_score= overall_score/len(ai_predictions) if ai_predictions else 0,
                result_accuracy= result_accuracy/len(ai_predictions) if ai_predictions else 0,
                correct_accuracy= score_accuracy/len(ai_predictions) if ai_predictions else 0
            )

            # Return current stored information
            return HttpResponse("Updated leaderboard positions.", status=200)
        
        except requests.exceptions.RequestException as e:
            # Handle any request-related errors here
            return HttpResponse(str(e), status=400)
      
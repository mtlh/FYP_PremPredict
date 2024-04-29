from django.http import HttpResponse
from django.views.generic import View
from ...models import APIresponses, PremGames, UserProfile, Leaderboard, PremSeasonInfo, PremTeams, PremTable, PremCompetition, PremGameweeks, UserPrediction, AlgorithmPrediction

class ClearDb(View):
    def get(self, request, *args, **kwargs):

        # Clear tables
        # APIresponses.objects.filter().delete()
        # UserProfile.objects.filter().delete()
        # Leaderboard.objects.filter().delete()
        # PremGames.objects.filter().delete()
        # PremSeasonInfo.objects.filter().delete()
        # PremTeams.objects.filter().delete()
        # PremTable.objects.filter().delete()
        # PremCompetition.objects.filter().delete()
        # PremGameweeks.objects.filter().delete()
        # UserPrediction.objects.filter().delete()
        # AlgorithmPrediction.objects.filter().delete()

        # Return current stored information
        return HttpResponse("Cleared all table data.", status=200)
      
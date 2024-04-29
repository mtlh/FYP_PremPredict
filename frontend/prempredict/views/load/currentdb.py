from django.http import HttpResponse
from django.views.generic import View
from ...models import APIresponses, PremSeasonInfo, PremTeams, PremTable, PremCompetition, PremGameweeks

class CurrentDB(View):
    def get(self, request, *args, **kwargs):

        # print(APIresponses.objects.all())
        # print(PremSeasonInfo.objects.all())
        # print(PremTeams.objects.all())
        # print(PremTable.objects.all())
        # print(PremCompetition.objects.all())
        # print(PremGameweeks.objects.all())

        # Return current stored information
        return HttpResponse("Printed all table data.", status=200)
      
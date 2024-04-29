from django.shortcuts import render
from django.views import View
from prempredict.models import PremTable, PremTeams

class Table(View):
    def get(self, request, *args, **kwargs):

        tablearr = []
        maindata = PremTable.objects.all()
        for tablepos in maindata:
            tablearr.append(
                {
                    "position": tablepos.position,
                    "name": tablepos.team.initals,
                    "badge": tablepos.team.badge,
                    "played": tablepos.played,
                    "win": tablepos.win,
                    "loss": tablepos.loss,
                    "draw": tablepos.draw,
                    "goaldifference": int(tablepos.goaldifference),
                    "points": tablepos.points,
                }
            )
        
        context = {
            'tabledata': tablearr,
            'isauth': request.user.is_authenticated
        }
        return render(request, 'table.html',  context)
import re
from django.http import HttpResponse
from django.views.generic import View
from ...models import APIresponses, PremSeasonInfo, PremTable, PremTeams
import requests

class LoadTeamsTable(View):
    def get(self, request, *args, **kwargs):
        try:
            standingdata = APIresponses.objects.get(id=1).fbstanding_api
            for standingposition in standingdata.get("standings", [])[0].get("table", []):
                
                # Fill 'PremTeams' Table
                team_info, created = PremTeams.objects.get_or_create(
                    id=standingposition.get("team").get("id"),
                    defaults={
                        "fullname": standingposition.get("team").get("name"),
                        "shortname": standingposition.get("team").get("shortName"),
                        "initals": standingposition.get("team").get("tla"),
                        "badge": standingposition.get("team").get("crest")
                    }
                )
                if not created:
                    team_info.fullname = standingposition.get("team").get("name")
                    team_info.shortname = standingposition.get("team").get("shortName")
                    team_info.initals = standingposition.get("team").get("tla")
                    team_info.badge = standingposition.get("team").get("crest")
                    team_info.save()

                # Fill 'PremTable' Table
                table_info, created = PremTable.objects.get_or_create(
                    position=standingposition.get("position"),
                    defaults={
                        "team": PremTeams.objects.get(id=standingposition.get("team").get("id")),
                        "season": PremSeasonInfo.objects.get(id=standingdata.get("season").get("id")),
                        "played": standingposition.get("playedGames"),
                        "win": standingposition.get("won"),
                        "draw": standingposition.get("draw"),
                        "loss": standingposition.get("lost"),
                        "goaldifference": standingposition.get("goalDifference"),
                        "points": standingposition.get("points")
                    }
                )
                if not created:
                    table_info.team = PremTeams.objects.get(id=standingposition.get("team").get("id"))
                    table_info.season = PremSeasonInfo.objects.get(id=standingdata.get("season").get("id"))
                    table_info.played = standingposition.get("playedGames")
                    table_info.win =  standingposition.get("won")
                    table_info.draw =  standingposition.get("draw")
                    table_info.loss =  standingposition.get("lost")
                    table_info.goaldifference =  standingposition.get("goalDifference")
                    table_info.points =  standingposition.get("points")
                    table_info.save()

            response = requests.get("https://www.fotmob.com/api/leagues?id=47&ccode3=GBR"); response.raise_for_status()
            fotmobtable = response.json().get("table")[0].get("data").get("table").get("all")
            prem_table_record = PremTable.objects.all()

            for tableteam in fotmobtable:
                for table_record in prem_table_record:
                    premteam = table_record.team
                    if (re.sub(r'\sFC', '', premteam.fullname) == tableteam.get("name")):
                        premteam.badge = "https://images.fotmob.com/image_resources/logo/teamlogo/" + str(tableteam.get("id")) + ".png"
                        premteam.save()

            # Return current stored information
            return HttpResponse("Loaded with fresh data", status=200)
        
        except requests.exceptions.RequestException as e:
            # Handle any request-related errors here
            return HttpResponse(str(e), status=400)
      
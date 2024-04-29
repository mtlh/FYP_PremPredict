from datetime import datetime
from dateutil import parser
from django.http import HttpResponse
from django.views.generic import View
import pytz
from ...models import APIresponses, PremGames, PremGameweeks, PremSeasonInfo, PremTeams, PremCompetition
import requests

class LoadFixtures(View):
    def get(self, request, var1, var2, *args, **kwargs,):
        try:
            matchesdata = APIresponses.objects.get(id=1).fbmatch_api
            all_deadlines = PremGameweeks.objects.all()
            deadline_dates = [datetime.strptime(str(gw.deadline), '%Y-%m-%d %H:%M:%S%z').astimezone(tz=pytz.UTC) for gw in all_deadlines]
            for premgames in matchesdata.get("matches", []):
                if int(premgames.get("matchday")) >= int(var1) and int(premgames.get("matchday")) <= int(var2):
                    new_gw = premgames.get("matchday")
                     # Check if moved date is confirmed (has hrs+min time rather than 00:00, if yes, update it with the correct matchday - otherwise ignore until arranged.
                    premgame_date = datetime.strptime(premgames.get("utcDate"), "%Y-%m-%dT%H:%M:%SZ").astimezone(tz=pytz.UTC)
                    new_gw = sum(1 for deadline in deadline_dates if deadline > premgame_date)
                    new_gw = 38-new_gw
                    # Fill 'PremFixtures' Table
                    result_info, created = PremGames.objects.get_or_create(
                        matchid=premgames.get("id"),
                        defaults={
                            "competition": PremCompetition.objects.get(id=premgames.get("competition").get("id")),
                            "season":  PremSeasonInfo.objects.get(id=premgames.get("season").get("id")),
                            "area_name":  premgames.get("area").get("name"),
                            "area_code":  premgames.get("area").get("code"),
                            "area_flag":  premgames.get("area").get("flag"),
                            "status": premgames.get("status"),
                            "score_winner":  str(premgames.get("score").get("winner")),
                            "score_duration":  premgames.get("score").get("duration"),
                            "score_hometeam":  int(premgames.get("score").get("fullTime").get("home")) if premgames.get("score").get("fullTime").get("home") is not None else 0,
                            "score_awayteam":  int(premgames.get("score").get("fullTime").get("away")) if premgames.get("score").get("fullTime").get("away") is not None else 0,
                            "hometeam":  PremTeams.objects.get(id=premgames.get("homeTeam").get("id")),
                            "awayteam":  PremTeams.objects.get(id=premgames.get("awayTeam").get("id")),
                            "date":  parser.parse(premgames.get("utcDate")).strftime("%Y-%m-%dT%H:%M:%SZ"),
                            "matchday":  new_gw
                        }
                    )
                    if not created:
                        result_info.competition = PremCompetition.objects.get(id=premgames.get("competition").get("id"))
                        result_info.season = PremSeasonInfo.objects.get(id=premgames.get("season").get("id"))
                        result_info.area_name = premgames.get("area").get("name")
                        result_info.area_code = premgames.get("area").get("code")
                        result_info.area_flag = premgames.get("area").get("flag")
                        result_info.status = premgames.get("status")
                        result_info.score_winner = str(premgames.get("score").get("winner"))
                        result_info.score_duration = premgames.get("score").get("duration")
                        result_info.score_hometeam = int(premgames.get("score").get("fullTime").get("home")) if premgames.get("score").get("fullTime").get("home") is not None else 0
                        result_info.score_awayteam = int(premgames.get("score").get("fullTime").get("away")) if premgames.get("score").get("fullTime").get("away") is not None else 0
                        result_info.hometeam = PremTeams.objects.get(id=premgames.get("homeTeam").get("id"))
                        result_info.awayteam = PremTeams.objects.get(id=premgames.get("awayTeam").get("id"))
                        result_info.date = parser.parse(premgames.get("utcDate")).strftime("%Y-%m-%dT%H:%M:%SZ")
                        result_info.matchday = new_gw
                        result_info.save()
                    #print(result_info.date)

            # Return current stored information
            return HttpResponse("Loaded results and fixtures tables with fresh data.", status=200)
        
        except requests.exceptions.RequestException as e:
            # Handle any request-related errors here
            return HttpResponse(str(e), status=400)
      
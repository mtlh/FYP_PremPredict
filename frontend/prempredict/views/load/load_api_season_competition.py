from datetime import datetime, timedelta
import pytz
from django.http import HttpResponse
from django.views.generic import View
from ...models import APIresponses, PremGames, PremSeasonInfo, PremCompetition, PremGameweeks
import requests
import os

class LoadApiFirst(View):
    def get(self, request, *args, **kwargs):

        fbapi_headers = {'X-Auth-Token': os.environ['FBAPI_KEY']}
        fantasy_headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "Priority": "u=0, i",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
            }
        fantasyurl = "https://fantasy.premierleague.com/api/bootstrap-static/"
        standingurl = "https://api.football-data.org/v4/competitions/PL/standings"
        matchesurl = "https://api.football-data.org/v4/competitions/PL/matches"

        try:
            response = requests.get(fantasyurl, headers=fantasy_headers); response.raise_for_status()
            fantasydata = response.json()

            APIresponses.objects.filter(id=1).update(
                fantasty_api=fantasydata
            )

            # Fill 'PremGameweeks' Table
            for gameweekdata in fantasydata.get("events"):
                gameweek_info, created = PremGameweeks.objects.get_or_create(
                    id=gameweekdata.get("id"),
                    defaults={
                        "name": gameweekdata.get("name"),
                        "number": gameweekdata.get("id"),
                        "deadline": gameweekdata.get("deadline_time"),
                        "season": PremSeasonInfo.objects.filter(active=True).get(),
                    }
                )
                if not created:
                    gameweek_info.name = gameweekdata.get("name")
                    gameweek_info.number = gameweekdata.get("id")
                    gameweek_info.deadline = gameweekdata.get("deadline_time")
                    gameweek_info.season = PremSeasonInfo.objects.filter(active=True).get()
                    gameweek_info.save()

                current_deadline = datetime.strptime(str(PremGameweeks.objects.filter(number=gameweekdata.get("id")).get().deadline), '%Y-%m-%d %H:%M:%S%z').astimezone(pytz.timezone('Europe/London'))
                first_gw_game = PremGames.objects.filter(matchday=gameweekdata.get("id")).order_by('date').first().date.astimezone(pytz.timezone('Europe/London')) - timedelta(minutes=90)
                gw = PremGameweeks.objects.get(id=gameweekdata.get("id"))
                gw.deadline = min(first_gw_game, current_deadline)
                gw.save()
                
        except:
            print("Error loading boostrap-static route")

        try:
            response = requests.get(standingurl, headers=fbapi_headers); response.raise_for_status()
            standingdata = response.json()
            response = requests.get(matchesurl, headers=fbapi_headers); response.raise_for_status()
            matchesdata = response.json()

            APIresponses.objects.filter(id=1).update(
                fbmatch_api=matchesdata,
                fbstanding_api=standingdata
            )

            # Fill 'PremCompetition' Table
            competition_info, created = PremCompetition.objects.get_or_create(
                id=standingdata.get("competition").get("id"),
                defaults={
                    "code": standingdata.get("competition").get("code"),
                    "name": standingdata.get("competition").get("name"),
                    "type": str(standingdata.get("competition").get("type")),
                    "emblem": standingdata.get("competition").get("emblem")
                }
            )
            if not created:
                competition_info.code = standingdata.get("competition").get("code")
                competition_info.name = standingdata.get("competition").get("name")
                competition_info.type = str(standingdata.get("competition").get("type"))
                competition_info.emblem = standingdata.get("competition").get("emblem")
                competition_info.save()

            # Fill 'PremSeasonInfo' Table
            season_info, created = PremSeasonInfo.objects.get_or_create(
                id=standingdata.get("season").get("id"),
                defaults={
                    "startDate": standingdata.get("season").get("startDate"),
                    "active": True,
                    "endDate": standingdata.get("season").get("endDate"),
                    "winner": str(standingdata.get("season").get("winner")),
                    "currentMatchday": standingdata.get("season").get("currentMatchday")
                }
            )
            if not created:
                season_info.startDate = standingdata.get("season").get("startDate")
                season_info.active = True
                season_info.endDate = standingdata.get("season").get("endDate")
                season_info.winner = str(standingdata.get("season").get("winner"))
                season_info.currentMatchday = standingdata.get("season").get("currentMatchday")
                season_info.save()

            # Return current stored information
            return HttpResponse("Loaded api responses, season and competition with fresh data.", status=200)
        
        except requests.exceptions.RequestException as e:
            # Handle any request-related errors here
            return HttpResponse(str(e), status=400)
      
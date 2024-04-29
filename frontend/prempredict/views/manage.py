from django.views.generic import View
from ..models import *
from django.shortcuts import render

# TO ACCESS - LOGIN WITH .ENV VARS IN /ADMIN or /LOGIN routes
class ManageAdmin(View):
    def get(self, request, *args, **kwargs):
        endpoints = []
        if request.user.is_superuser:
            endpoints = [
                {
                    "id": "load_api",
                    "targetid": "#load_api",
                    "spinner": "load_api_spinner",
                    "targetspinner": "#load_api_spinner",
                    "url": "/load/api",
                    "method": "GET"
                },
                {
                    "id": "load_userscores",
                    "targetid": "#load_userscores",
                    "spinner": "load_userscores_spinner",
                    "targetspinner": "#load_userscores_spinner",
                    "url": "/load/userscores",
                    "method": "GET"
                },
                {
                    "id": "load_aiscores",
                    "targetid": "#load_aiscores",
                    "spinner": "load_aiscores_spinner",
                    "targetspinner": "#load_aiscores_spinner",
                    "url": "/load/aiscores",
                    "method": "GET"
                },
                {
                    "id": "load_leaderboard",
                    "targetid": "#load_leaderboard",
                    "spinner": "load_leaderboard_spinner",
                    "targetspinner": "#load_leaderboard_spinner",
                    "url": "/load/leaderboard",
                    "method": "GET"
                },
                {
                    "id": "load_table_teams",
                    "targetid": "#load_table_teams",
                    "spinner": "load_table_teams_spinner",
                    "targetspinner": "#load_table_teams_spinner",
                    "url": "/load/table/teams", 
                    "method": "GET"
                },
                {
                    "id": "load_game_1_4",
                    "targetid": "#load_game_1_4",
                    "spinner": "load_game_1_4_spinner",
                    "targetspinner": "#load_game_1_4_spinner",
                    "url": "/load/game/1/4", 
                    "method": "GET"
                },
                {
                    "id": "load_game_5_9",
                    "targetid": "#load_game_5_9",
                    "spinner": "load_game_5_9_spinner",
                    "targetspinner": "#load_game_5_9_spinner",
                    "url": "/load/game/5/9", 
                    "method": "GET"
                },
                {
                    "id": "load_game_10_14",
                    "targetid": "#load_game_10_14",
                    "spinner": "load_game_10_14_spinner",
                    "targetspinner": "#load_game_10_14_spinner",
                    "url": "/load/game/10/14", 
                    "method": "GET"
                },
                {
                    "id": "load_game_15_19",
                    "targetid": "#load_game_15_19",
                    "spinner": "load_game_15_19_spinner",
                    "targetspinner": "#load_game_15_19_spinner",
                    "url": "/load/game/15/19", 
                    "method": "GET"
                },
                {
                    "id": "load_game_20_24",
                    "targetid": "#load_game_20_24",
                    "spinner": "load_game_20_24_spinner",
                    "targetspinner": "#load_game_20_24_spinner",
                    "url": "/load/game/20/24", 
                    "method": "GET"
                },
                {
                    "id": "load_game_25_29",
                    "targetid": "#load_game_25_29",
                    "spinner": "load_game_25_29_spinner",
                    "targetspinner": "#load_game_25_29_spinner",
                    "url": "/load/game/25/29", 
                    "method": "GET"
                },
                {
                    "id": "load_game_30_34",
                    "targetid": "#load_game_30_34",
                    "spinner": "load_game_30_34_spinner",
                    "targetspinner": "#load_game_30_34_spinner",
                    "url": "/load/game/30/34", 
                    "method": "GET"
                },
                {
                    "id": "load_game_35_38",
                    "targetid": "#load_game_35_38",
                    "spinner": "load_game_35_38_spinner",
                    "targetspinner": "#load_game_35_38_spinner",
                    "url": "/load/game/35/38", 
                    "method": "GET"
                },
            ]
        context = {
            'isauth': request.user.is_superuser,
            'endpoints': endpoints
        }
        return render(request, 'manage/adminhome.html',  context)
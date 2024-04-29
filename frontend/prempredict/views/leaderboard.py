from django.shortcuts import render
from django.views import View
from prempredict.models import Leaderboard, UserPrediction, AILeaderboard, AlgorithmPrediction, PublicPrivateLeaderboardEntry, Leaderboard, PublicPrivateLeaderboard
from .functions.getGameweekDeadlines import getGameweekDeadline
from django.db.models import Q

class LeaderboardView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'isauth': request.user.is_authenticated,
        }
        return render(request, 'leaderboard/leaderboard.html',  context)
    

class PublicLeaderboardView(View):
    def get(self, request, *args, **kwargs):
        leaderboards = []
        if request.user.is_authenticated:
            user_public_leaderboards = PublicPrivateLeaderboardEntry.objects.filter(user=request.user, leaderboard__is_public=True)
            leaderboard_entry_details = {}
            for leaderboard_entry in user_public_leaderboards:
                public_private_leaderboard_instance = PublicPrivateLeaderboard.objects.get(invite_url=leaderboard_entry.leaderboard.invite_url)
                leaderboard_entries = PublicPrivateLeaderboardEntry.objects.filter(leaderboard=public_private_leaderboard_instance)
                leaderboard_records = Leaderboard.objects.filter(user__id__in=leaderboard_entries.values('user__id'))
                leaderboard_entry_details = {
                    "name": leaderboard_entry.leaderboard.name,
                    "invcode": leaderboard_entry.leaderboard.invite_url,
                    "user_info": []
                }
                for leaderboard_user_info in leaderboard_records.all():
                    leaderboard_user_details = {
                        "position": int(leaderboard_user_info.position),
                        "score": leaderboard_user_info.score,
                        "result_accuracy": leaderboard_user_info.result_accuracy,
                        "correct_accuracy": leaderboard_user_info.correct_accuracy,
                        "average_gw_score": leaderboard_user_info.average_gw_score,
                        "user_recent_update": leaderboard_user_info.user_recent_update,
                        "user_name": leaderboard_user_info.user.username
                    }
                    leaderboard_entry_details["user_info"].append(leaderboard_user_details)
            if leaderboard_entry_details != {}:
                leaderboard_entry_details["user_info"] = sorted(leaderboard_entry_details["user_info"], key=lambda x: x["position"])
                leaderboards.append(leaderboard_entry_details)
        context = {
            'public_user_leaderboards': leaderboards,
            'isauth': request.user.is_authenticated,
        }
        return render(request, 'leaderboard/public_leaderboard.html',  context)
    
class PrivateLeaderboardView(View):
    def get(self, request, *args, **kwargs):
        leaderboards = []
        if request.user.is_authenticated:
            user_public_leaderboards = PublicPrivateLeaderboardEntry.objects.filter(user=request.user, leaderboard__is_public=False)
            leaderboard_entry_details = {}
            for leaderboard_entry in user_public_leaderboards:
                public_private_leaderboard_instance = PublicPrivateLeaderboard.objects.get(invite_url=leaderboard_entry.leaderboard.invite_url)
                leaderboard_entries = PublicPrivateLeaderboardEntry.objects.filter(leaderboard=public_private_leaderboard_instance)
                leaderboard_records = Leaderboard.objects.filter(user__id__in=leaderboard_entries.values('user__id'))
                leaderboard_entry_details = {
                    "name": leaderboard_entry.leaderboard.name,
                    "invcode": leaderboard_entry.leaderboard.invite_url,
                    "user_info": []
                }
                for leaderboard_user_info in leaderboard_records.all():
                    leaderboard_user_details = {
                        "position": int(leaderboard_user_info.position),
                        "score": leaderboard_user_info.score,
                        "result_accuracy": leaderboard_user_info.result_accuracy,
                        "correct_accuracy": leaderboard_user_info.correct_accuracy,
                        "average_gw_score": leaderboard_user_info.average_gw_score,
                        "user_recent_update": leaderboard_user_info.user_recent_update,
                        "user_name": leaderboard_user_info.user.username
                    }
                    leaderboard_entry_details["user_info"].append(leaderboard_user_details)
            if leaderboard_entry_details != {}:
                leaderboard_entry_details["user_info"] = sorted(leaderboard_entry_details["user_info"], key=lambda x: x["position"])
                leaderboards.append(leaderboard_entry_details)
        context = {
            'private_user_leaderboards': leaderboards,
            'isauth': request.user.is_authenticated,
        }
        return render(request, 'leaderboard/private_leaderboard.html',  context)
    
class ManageLeaderboardView(View):
    def get(self, request, *args, **kwargs):
        leaderboards = []
        if request.user.is_authenticated:
            user_private_leaderboards = PublicPrivateLeaderboardEntry.objects.filter(user=request.user)
            for leaderboard_entry in user_private_leaderboards:
                leaderboard_name_and_invitecode = {"name": leaderboard_entry.leaderboard.name, "invcode": leaderboard_entry.leaderboard.invite_url}
                leaderboards.append(leaderboard_name_and_invitecode)
        context = {
            'user_leaderboards': leaderboards,
            'isauth': request.user.is_authenticated,
        }
        return render(request, 'leaderboard/manage_leaderboard.html',  context)
    
    
class OverallLeaderboardView(View):
    def get(self, request, *args, **kwargs):
        userarr = []
        maindata = Leaderboard.objects.all().order_by('position')[:20]
        currentMatchweek = getGameweekDeadline()["matchday"]
        for user in maindata:
            latestgameweek = UserPrediction.objects.filter(user=user.user, gameweek__in=[currentMatchweek-1, currentMatchweek-2]).exclude(Q(predictionscore=0) | Q(predictionscore=None)).values_list('predictionscore', flat=True).last() or 0
            userarr.append(
                {
                    "position": user.position,
                    "latestgameweek": latestgameweek,
                    "overallscore": user.score,
                    "name": user.user.username,
                    "result_accuracy": user.result_accuracy,
                    "correct_accuracy": user.correct_accuracy,
                    "average_gw_score": user.average_gw_score,
                    "updated": user.user_recent_update,
                }
            )

        ai_record = AILeaderboard.objects.get(getval=1)
        ai_latestgameweek = AlgorithmPrediction.objects.filter(gameweek__in=[currentMatchweek-1, currentMatchweek-2]).exclude(Q(predictionscore=0) | Q(predictionscore=None)).values_list('predictionscore', flat=True).last() or 0

        if request.user.is_authenticated:
            user_record = Leaderboard.objects.get(user=request.user)
            latestgameweek = UserPrediction.objects.filter(user=request.user, gameweek__in=[currentMatchweek-1, currentMatchweek-2]).exclude(Q(predictionscore=0) | Q(predictionscore=None)).values_list('predictionscore', flat=True).last() or 0
            userarr.insert(0,
                {
                    "position": user_record.position,
                    "latestgameweek": latestgameweek,
                    "overallscore": user_record.score,
                    "name": user_record.user.username,
                    "result_accuracy": user_record.result_accuracy,
                    "correct_accuracy": user_record.correct_accuracy,
                    "average_gw_score": user_record.average_gw_score,
                    "updated": user_record.user_recent_update,
                }
            )

        context = {
            'users': userarr,
            'isauth': request.user.is_authenticated,
            'auth_username': request.user.username,
            'ai_record_latestgameweek': ai_latestgameweek,
            'ai_record_average_gw_score': ai_record.average_gw_score,
            'ai_record_score': ai_record.score,
            'ai_record_result_accuracy': ai_record.result_accuracy,
            'ai_record_correct_accuracy': ai_record.correct_accuracy,
            'ai_record_updated': max(userarr, key=lambda x: x["updated"])["updated"]
        }
        return render(request, 'leaderboard/overall_leaderboard.html',  context)
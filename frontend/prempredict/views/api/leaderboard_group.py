import random
import string
from django.http import HttpResponse
from django.views.generic import View
import requests
from ...models import PublicPrivateLeaderboard, PublicPrivateLeaderboardEntry

class CreateGroup(View):
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                ispublic = bool(int(request.POST.get('ispublic', 0)))
            except:
                ispublic = False
            name = str(request.POST.get('name', "MiniLeaderboard"))
            base_url = "https://www.purgomalum.com/service/plain"
            params = {"text": name}
            try:
                response = requests.get(base_url, params=params)
                if response.status_code == 200 and response.text == name:

                    try:
                        PublicPrivateLeaderboard.objects.get(name=name)
                        return HttpResponse("Group name already in use.", status=200)
                    except PublicPrivateLeaderboard.DoesNotExist:
                        invite_link = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(25))
                        new_leaderboard_instance = PublicPrivateLeaderboard()
                        new_leaderboard_instance.invite_url = invite_link
                        new_leaderboard_instance.is_public = ispublic
                        new_leaderboard_instance.name = name
                        new_leaderboard_instance.save()

                        new_leaderboard_instance_entry = PublicPrivateLeaderboardEntry()
                        new_leaderboard_instance_entry.user = request.user
                        new_leaderboard_instance_entry.leaderboard = new_leaderboard_instance
                        new_leaderboard_instance_entry.save()

                else:
                    return HttpResponse("Profanity found in name.", status=200)
                
            except requests.RequestException:
                return HttpResponse(f"Profanity check failure.", status=200)

            return HttpResponse(f"Created a group!", status=200)
        else:
            return HttpResponse("User not authenticated.", status=200)
        
class LeaveGroup(View):
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:

            try:
                invitelink = str(request.POST.get('invitelink', ''))
                entry_to_delete = PublicPrivateLeaderboardEntry.objects.get(leaderboard__invite_url=invitelink, user=request.user)
                entry_to_delete.delete()

                if PublicPrivateLeaderboardEntry.objects.filter(leaderboard__invite_url=invitelink).count() <= 0:
                    instance_to_delete = PublicPrivateLeaderboard.objects.get(invite_url=invitelink)
                    instance_to_delete.delete()

            except PublicPrivateLeaderboardEntry.DoesNotExist:
                return HttpResponse(f"You are not part of this group.", status=200)

            return HttpResponse(f"Left group!", status=200)
        else:
            return HttpResponse("User not authenticated.", status=200)

class JoinGroup(View):
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:

            try:
                invitelink = str(request.POST.get('invitelink', ''))
                existing_leaderboard_instance = PublicPrivateLeaderboard.objects.get(invite_url=invitelink)
                
                try:
                    PublicPrivateLeaderboardEntry.objects.get(leaderboard__invite_url=invitelink, user=request.user)
                    return HttpResponse(f"You are already in this group.", status=200)
                except PublicPrivateLeaderboardEntry.DoesNotExist:
                    new_leaderboard_instance_entry = PublicPrivateLeaderboardEntry()
                    new_leaderboard_instance_entry.user = request.user
                    new_leaderboard_instance_entry.leaderboard = existing_leaderboard_instance
                    new_leaderboard_instance_entry.save()

            except PublicPrivateLeaderboard.DoesNotExist:
                return HttpResponse(f"Group does not exist.", status=200)

            return HttpResponse(f"Joined Group!", status=200)
        else:
            return HttpResponse("User not authenticated.", status=200)
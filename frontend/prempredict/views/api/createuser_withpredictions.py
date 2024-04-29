import random
from django.http import HttpResponse
from django.views.generic import View
from ...models import *
from django.contrib.auth.models import User

class CreatePredictionUser(View):
    def get(self, request, amount, *args, **kwargs):
        
        adjectives = ['happy', 'sunny', 'mysterious', 'colorful', 'brave', 'clever', 'playful', 'radiant', 'graceful', 'vibrant']
        nouns = ['unicorn', 'dragon', 'star', 'moon', 'river', 'garden', 'whisper', 'serenade', 'cascade', 'harmony']

        while amount > 0:
            adjective = random.choice(adjectives)
            noun = random.choice(nouns)
            number = random.randint(1000, 9999)
            username = f"{adjective}_{noun}_{number}"
            email = username + "@gmail.com"
            
            user = User.objects.create_user(username, email, username)
            UserProfile.objects.create(user=user).save()
            Leaderboard.objects.create(user=user).save()

            currentMatchday = 1
            while currentMatchday <= 38:

                # Get all games for that gameweek
                all_gw_games = PremGames.objects.filter(matchday=currentMatchday).all()
                predict_json = {}
                for fixture in all_gw_games:
                    predict_json[str(fixture.matchid)] = {"away":random.randint(0,4), "home":random.randint(0,4)}

                obj, created = UserPrediction.objects.update_or_create(
                    user_id=user.id,
                    gameweek=currentMatchday,
                    defaults={
                        "scores": predict_json
                    }
                )
                if not created:
                    UserPrediction.objects.filter(
                        user_id=user.id,
                        gameweek=currentMatchday,
                    ).update(
                        scores = predict_json,
                        date = timezone.now()
                    )

                currentMatchday+=1
            amount-=1

        return HttpResponse("Created " + str(amount) + " new users (with complete predictions).", status=200)
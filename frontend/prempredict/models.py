from django.db import models
import uuid
from django.utils import timezone
from django.contrib.auth.models import User

# Testing
class TestTable(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    name = models.CharField(max_length=250)

# storing API JSON reponses
class APIresponses(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    updated = models.DateField(default=timezone.now)
    fantasty_api = models.JSONField(default=dict)
    fbmatch_api = models.JSONField(default=dict)
    fbstanding_api = models.JSONField(default=dict)

# Team Table
class PremTeams(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    fullname = models.CharField()
    shortname = models.CharField()
    initals = models.CharField()
    badge = models.URLField()

# League Seasons
class PremSeasonInfo(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    active = models.BooleanField(default=False) 
    currentMatchday = models.PositiveIntegerField(default=1)
    winner = models.CharField(default="null")
    startDate = models.DateField(default=timezone.now)
    endDate = models.DateField(default=timezone.now)

# Season Gameweeks
class PremGameweeks(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    name = models.CharField(default="")
    number = models.PositiveIntegerField(default=1)
    deadline = models.DateTimeField(default=timezone.now)
    season = models.ForeignKey(PremSeasonInfo, on_delete=models.CASCADE)

# Teams Positions in League
class PremTable(models.Model):
    season = models.ForeignKey(PremSeasonInfo, on_delete=models.CASCADE)
    team = models.ForeignKey(PremTeams, on_delete=models.CASCADE)
    position = models.PositiveIntegerField(primary_key=True)
    played = models.PositiveIntegerField(default=0)
    win = models.PositiveIntegerField(default=0)
    draw = models.PositiveIntegerField(default=0)
    loss = models.PositiveIntegerField(default=0)
    goaldifference = models.FloatField(default=0)
    points = models.IntegerField(default=0)

# Competition Info
class PremCompetition(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    code  = models.CharField()
    name = models.CharField()
    type = models.CharField()
    emblem = models.CharField()

# Upcoming Premier League Fixtures
class PremGames(models.Model):
    matchid = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    area_name = models.CharField()
    area_code = models.CharField()
    area_flag = models.CharField()
    status = models.CharField(default="")
    score_winner = models.CharField()
    score_duration = models.CharField()
    score_hometeam = models.PositiveIntegerField()
    score_awayteam = models.PositiveIntegerField()
    hometeam = models.ForeignKey(PremTeams, on_delete=models.CASCADE, related_name='home_fixture')
    awayteam = models.ForeignKey(PremTeams, on_delete=models.CASCADE, related_name='away_fixture')
    season = models.ForeignKey(PremSeasonInfo, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    competition = models.ForeignKey(PremCompetition, on_delete=models.CASCADE)
    matchday = models.PositiveIntegerField()

# Algorithm prediction
class AlgorithmPrediction(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    gameweek = models.PositiveIntegerField(default=1)
    scores = models.JSONField(default=dict)
    date = models.DateField(default=timezone.now)
    score_check_time = models.DateTimeField(default=timezone.now)
    isscorecomplete = models.BooleanField(default=False)
    predictionscore = models.PositiveIntegerField(default=None, blank=True, null=True)
    result_accuracy = models.PositiveIntegerField(default=0)
    correct_accuracy = models.PositiveIntegerField(default=0)

# User prediction
class UserPrediction(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gameweek = models.PositiveIntegerField(default=1)
    scores = models.JSONField(default=dict)
    date = models.DateField(default=timezone.now)
    score_check_time = models.DateTimeField(default=timezone.now)
    isscorecomplete = models.BooleanField(default=False)
    predictionscore = models.PositiveIntegerField(default=None, blank=True, null=True)
    result_accuracy = models.PositiveIntegerField(default=0)
    correct_accuracy = models.PositiveIntegerField(default=0)

# Extended User model for additional fields
class UserProfile(models.Model):
    createnum = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nickname = models.CharField(default="")
    avatar = models.CharField(default="")

# Overall Leaderboard model
class Leaderboard(models.Model):
    createnum = models.BigAutoField(primary_key=True)
    position = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=0)
    result_accuracy = models.PositiveIntegerField(default=0)
    correct_accuracy = models.PositiveIntegerField(default=0)
    average_gw_score = models.PositiveIntegerField(default=0)
    user_recent_update = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["score"]

class PublicPrivateLeaderboard(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    users = models.ManyToManyField(User, through='PublicPrivateLeaderboardEntry')
    is_public = models.BooleanField(default=False)
    invite_url = models.CharField(max_length=255, unique=True)

class PublicPrivateLeaderboardEntry(models.Model):
    leaderboard = models.ForeignKey(PublicPrivateLeaderboard, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

# Overall AI Score
class AILeaderboard(models.Model):
    createnum = models.BigAutoField(primary_key=True)
    score = models.PositiveIntegerField(default=0)
    getval = models.PositiveIntegerField(default=1)
    result_accuracy = models.PositiveIntegerField(default=0)
    correct_accuracy = models.PositiveIntegerField(default=0)
    average_gw_score = models.PositiveIntegerField(default=0)

# Hidden Stats for refreshing APIs or other Admin behaviours
class AdminOnly(models.Model):
    createnum = models.BigAutoField(primary_key=True)
    user_score_update = models.PositiveIntegerField(default=0)
    ai_score_update = models.PositiveIntegerField(default=0)
    user_leaderboard_update = models.PositiveIntegerField(default=0)
    position_leaderboard_update = models.PositiveIntegerField(default=0)
    ai_leaderboard_update = models.PositiveIntegerField(default=0)





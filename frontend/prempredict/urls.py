"""
URL configuration for prempredict project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from prempredict.views.load.update_userscores import UpdateUserScores
from prempredict.views.load.update_aiscores import UpdateAIScores
from prempredict.views.load.update_leaderboard import UpdateLeaderboard

from prempredict.views.leaderboard import LeaderboardView, OverallLeaderboardView, PrivateLeaderboardView, PublicLeaderboardView, ManageLeaderboardView
from prempredict.views.scores import ScoresGameweek, ScoresMain
from prempredict.views.home import Home, RecentResults, UpcomingFixtures
from prempredict.views.login import Login
from prempredict.views.logout import Logout
from .views.table import Table
from prempredict.views.predict import PredictHuman, PredictMain, PredictAI

from prempredict.views.api.savepredict import SavePrediction
from prempredict.views.api.leaderboard_group import CreateGroup, JoinGroup, LeaveGroup
from prempredict.views.api.createuser_withpredictions import CreatePredictionUser

from prempredict.views.profile import Profile, ProfileTable
from prempredict.views.manage import ManageAdmin
from prempredict.views.signup import Signup
from prempredict.views.testing import TestingDelete, TestingGet, TestingInsert, TestingUpdate

from prempredict.views.load.cleardb import ClearDb
from prempredict.views.load.load_api_season_competition import LoadApiFirst
from prempredict.views.load.currentdb import CurrentDB
from prempredict.views.load.load_results_fixtures import LoadFixtures
from prempredict.views.load.load_teams_table import LoadTeamsTable

urlpatterns = [
    path('', Home.as_view(), name="Home"),
    path('recent/', RecentResults.as_view(), name="Recent Results"),
    path('upcoming/', UpcomingFixtures.as_view(), name="Upcoming Fixtures"),

    path('table/', Table.as_view(), name="Table"),

    path('leaderboard/', LeaderboardView.as_view(), name="Leaderboard"),
    path('leaderboard/overall', OverallLeaderboardView.as_view(), name="Overall Leaderboard"),
    path('leaderboard/public', PublicLeaderboardView.as_view(), name="Public Leaderboards"),
    path('leaderboard/private', PrivateLeaderboardView.as_view(), name="Private Leaderboards"),
    path('leaderboard/manage', ManageLeaderboardView.as_view(), name="Manage Leaderboards"),
    path('leaderboard/create', CreateGroup.as_view(), name="Create A Custom Leaderboard"),
    path('leaderboard/leave', LeaveGroup.as_view(), name="Leave A Custom Leaderboard"),
    path('leaderboard/join', JoinGroup.as_view(), name="Join A Custom Leaderboard"),

    path('scores/', ScoresMain.as_view(), name="Scores"),
    path('scoresGameweek/', ScoresGameweek.as_view(), name="Scores by Gameweek"),

    path('predict/', PredictMain.as_view(), name="Predict"),
    path('predict/ai', PredictAI.as_view(), name="Prediction AI Selections"),
    path('predict/human', PredictHuman.as_view(), name="Prediction Human Selections"),
    path('predict/<home>/<homescore>/<away>/<awayscore>', PredictMain.as_view(), name="Prediction Entry"),
    path('predict/save', SavePrediction.as_view(), name='Save User Prediction'),

    path('profile/', Profile.as_view(), name="Profile"),
    path('profile/table', ProfileTable.as_view(), name="Profile Table"),

    path('signup/', Signup.as_view(), name="Signup"),
    path('logout/', Logout.as_view(), name="Logout"),
    path('login/', Login.as_view(), name="Login"),
    path('admin/', admin.site.urls),
    path('manage/', ManageAdmin.as_view(), name="Manage Admin"),

    path('testget/', TestingGet.as_view(), name='testget'),
    path('testinsert/', TestingInsert.as_view(), name='testinsert'),
    path('testupdate/', TestingUpdate.as_view(), name='testupdate'),
    path('testdelete/', TestingDelete.as_view(), name='testdelete'),

    path('load/api', LoadApiFirst.as_view(), name='Loading api responses into db'),
    path('load/current', CurrentDB.as_view(), name='Get all table data'),
    path('load/clear', ClearDb.as_view(), name='Clear all tables'),
    path('load/table/teams', LoadTeamsTable.as_view(), name='Teams Load'),
    path('load/game/<var1>/<var2>/', LoadFixtures.as_view(), name='Game Load'),
    path('load/userscores/', UpdateUserScores.as_view(), name='Score User predictions'),
    path('load/aiscores/', UpdateAIScores.as_view(), name='Score AI predictions'),
    path('load/leaderboard/', UpdateLeaderboard.as_view(), name='Update leaderboard positions'),
    path('load/createuser/<int:amount>/', CreatePredictionUser.as_view(), name='Create Prediction Users'),

]

from django.views.generic import View
import requests
from ..models import *
from prempredict.views.functions.sanitzeString import cleanString
from prempredict.types.forms import SignUpForm
from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.contrib.auth.models import User

    
class Signup(View):
    def get(self, request, *args, **kwargs):
        context = {
            'isauth': request.user.is_authenticated,
            'error': ''
        }
        return render(request, 'signup.html',  context)
    
    def post(self, request, *args, **kwargs):

        form = SignUpForm(request.POST)

        if form.data.get("password") != form.data.get("confpassword"):
            context = {
                'isauth': request.user.is_authenticated,
                'error': 'Passwords dont match'
            }
            return render(request, 'signup.html',  context)
        
        username = cleanString(form.data.get("username"))
        email = cleanString(form.data.get("email"))
        if form.is_valid() and not User.objects.filter(username=username).exists() and form.data.get("password") and username and email:

            base_url = "https://www.purgomalum.com/service/plain"
            params = {"text": username}
            
            try:
                response = requests.get(base_url, params=params)
                if response.status_code == 200 and response.text == username:

                    user = User.objects.create_user(username, email, form.data.get("password"))
                    UserProfile.objects.create(user=user).save()
                    Leaderboard.objects.create(user=user).save()
                    if user is not None:
                        login(request, user)
                        return redirect("/profile")
                    
            except requests.RequestException as e:
                print(f"Profanity filter -> request error: {e}")
            
        context = {
            'isauth': request.user.is_authenticated,
            'error': 'Credentials are invalid'
        }
        return render(request, 'signup.html',  context)
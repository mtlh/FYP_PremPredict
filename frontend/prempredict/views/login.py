from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth import authenticate, login
from prempredict.views.functions.sanitzeString import cleanString
from prempredict.types.forms import LoginForm


class Login(View):
    def get(self, request, *args, **kwargs):
        context = {
            'isauth': request.user.is_authenticated,
            'error': ''
        }
        return render(request, 'login.html',  context)
    
    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=cleanString(form.data.get("username")), password=form.data.get("password"))
            if user is not None:
                login(request, user)
                return redirect("/profile")
        context = {
            'isauth': request.user.is_authenticated,
            'error': 'Credentials are invalid'
        }
        return render(request, 'login.html',  context)
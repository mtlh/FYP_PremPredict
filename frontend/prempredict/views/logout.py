from django.shortcuts import redirect
from django.contrib.auth import logout
from django.views import View

class Logout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("/login")
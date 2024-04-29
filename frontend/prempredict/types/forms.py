from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label="username", max_length=100, min_length=5, required=True)
    password = forms.CharField(label="password", max_length=100, min_length=5, required=True)

class SignUpForm(forms.Form):
    username = forms.CharField(label="username", max_length=100, min_length=5, required=True)
    email = forms.EmailField(label="email", max_length=255, min_length=5, required=True)
    confpassword = forms.CharField(label="confpassword", max_length=100, min_length=5, required=True)
    password = forms.CharField(label="password", max_length=100, min_length=5, required=True)
from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label='Логин', max_length=50)
    password = forms.CharField(widget=forms.PasswordInput(), label='Пароль')


class EmployeeLoginForm(forms.Form):
    username = forms.CharField(label='Логин', max_length=50)
    password = forms.CharField(widget=forms.PasswordInput(), label='Пароль')
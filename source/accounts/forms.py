from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError



class SignUpForm(forms.Form):
    username = forms.CharField(max_length=100, required=True, label='Логин')
    first_name = forms.CharField(max_length=100, required=False, label='Имя')
    last_name = forms.CharField(max_length=100, required=False, label='Фамилия')
    password = forms.CharField(max_length=100, required=True, label='Пароль', widget=forms.PasswordInput)
    password_confirm = forms.CharField(max_length=100, required=True, label='Подтверждение пароля', widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            User.objects.get(username=username)
            raise ValidationError('Username already taken.', code='username_taken')
        except User.DoesNotExist:
            return username

    def clean(self):
        super().clean()
        password_1 = self.cleaned_data.get('password')
        password_2 = self.cleaned_data.get('password_confirm')
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        if password_1 != password_2:
            raise ValidationError('Passwords do not match.', code='password_do_not_match')
        return self.cleaned_data




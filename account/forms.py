from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from account.models import CustomUser


class UserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'last_name', 'first_name', 'middle_name', 'passport',
                  'email', 'born_date', 'phone', 'address']

    def clean_email(self):
        data = self.cleaned_data['email']
        qs = CustomUser.objects.exclude(id=self.instance.id)\
            .filter(email=data)
        if qs.exists():
            raise forms.ValidationError('Указанный адрес электронной почты уже существует.')
        return data


# class ProfileEditForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ['date_of_birth', 'photo']


class LoginForm(forms.Form):
    username = forms.CharField(label='Логин')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')


class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='Введите пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'last_name', 'first_name', 'middle_name',
                  'email', 'born_date', 'phone', 'address']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return cd['password2']

    def clean_email(self):
        data = self.cleaned_data['email']
        if CustomUser.objects.filter(email=data).exists():
            raise forms.ValidationError('Введённый адрес электронной почты уже существует')
        return data

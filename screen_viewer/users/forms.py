from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, UsernameField
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from viewer.models import Location
from .models import Profile

class UserAddForm(UserCreationForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={"class": "form-control"}))

    password1 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={"class": "form-control"})) 
    password2 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={"class": "form-control"}))
    
    locations = forms.ModelMultipleChoiceField(queryset=Location.objects.all(), widget=forms.SelectMultiple(attrs={"class": "form-select", "size": "12"}))

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


    def save(self, commit: bool = ...) -> Any:
        user = super().save(commit)
        
        profile = Profile.objects.get(user=user)
        profile.locations.set(self.cleaned_data['locations'])
        profile.save()
        
        return user
    

class UserEditForm(UserChangeForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={"class": "form-control"}))

    reset_password = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    
    locations = forms.ModelMultipleChoiceField(queryset=Location.objects.all(),
                                               widget=forms.SelectMultiple(attrs={"class": "form-select", "size": "12"}))

    class Meta:
        model = User
        fields = ['username', 'password']


    def save(self, commit: bool = ...) -> Any:
        user = super().save(commit)

        profile = Profile.objects.get(user=user)
        profile.locations.set(self.cleaned_data['locations'])
        profile.save()
        
        return user

class SigninForm(AuthenticationForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput())
    
    password = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'password']


class VerifyForm(forms.Form):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput())
    
    password = forms.CharField(max_length=10,
                                required=True,
                                widget=forms.PasswordInput())
    


class DeleteForm(AuthenticationForm):
    username = UsernameField(widget=forms.HiddenInput())
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(),
    )
    error_messages = {
        "invalid_login": _(
            "Please enter a correct password. Note that field "
            "may be case-sensitive."
        ),
        "inactive": _("This account is inactive."),
    }
    
    class Meta:
        model = User
        fields = ['username', 'password']
    
    
    

    
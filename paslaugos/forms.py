from django.shortcuts import render

from .models import UzsakymasReview, Profilis
from django import forms
from captcha.fields import CaptchaField
from django.contrib.auth.models import User

class UzsakymasReviewForm(forms.ModelForm):
    captcha = CaptchaField()

    class Meta:
        model = UzsakymasReview
        fields = ('content', 'uzsakymas', 'reviewer', 'captcha')
        widgets = {'uzsakymas': forms.HiddenInput(), 'reviewer': forms.HiddenInput()}

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfilisUpdateForm(forms.ModelForm):
    class Meta:
        model = Profilis
        fields = ['nuotrauka']


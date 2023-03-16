from django.shortcuts import render

from .models import UzsakymasReview
from django import forms
from captcha.fields import CaptchaField

class UzsakymasReviewForm(forms.ModelForm):
    captcha = CaptchaField()

    class Meta:
        model = UzsakymasReview
        fields = ('content', 'uzsakymas', 'reviewer', 'captcha')
        widgets = {'uzsakymas': forms.HiddenInput(), 'reviewer': forms.HiddenInput()}

    # def some_view(request):
    #     if request.POST:
    #         form = UzsakymasReviewForm(request.POST)
    #         if form.is_valid():
    #             human = True
    #     else:
    #         form = UzsakymasReviewForm()
    #     return render(request, 'paslaugos/uzsakymas_detail.html', {'form': form})


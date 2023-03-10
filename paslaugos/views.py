from django.shortcuts import render
from .models import *


def index(request):
    num_modelis = AutomobilioModelis.objects.all().count()
    num_automobilis = Automobilis.objects.all().count()
    num_uzsakymas = Uzsakymas.objects.all().count()
    num_paslauga = Paslauga.objects.all().count()
    num_eilute = UzsakymoEilute.objects.all().count()


    context = {
        'num_modelis': num_modelis,
        'num_automobilis': num_automobilis,
        'num_uzsakymas': num_uzsakymas,
        'num_paslauga': num_paslauga,
        'num_eilute': num_eilute
    }
    return render(request, 'paslaugos/index.html', context=context)

def automobiliai(request):
    automobiliai = Automobilis.objects.all()
    context = {
        'automobiliai': automobiliai
    }
    return render(request, 'paslaugos/automobiliai.html', context=context)

def automobilio_modeliai(request):
    automobilio_modeliai = AutomobilioModelis.objects.all()
    context = {
        'automobilio_modeliai': automobilio_modeliai
    }
    return render(request, 'paslaugos/automobiliomodelis.html', context=context)

def uzsakymas(request):
    uzsakymas = Uzsakymas.objects.all()
    context = {
        'uzsakymas': uzsakymas
    }
    return render(request, 'paslaugos/uzsakymas.html', context=context)

def paslauga(request):
    paslauga = Paslauga.objects.all()
    context = {
        'paslauga': paslauga
    }
    return render(request, 'paslaugos/paslauga.html', context=context)




from django.shortcuts import render
from .models import *


def index(request):
    num_modelis = AutomobilioModelis.objects.all().count()
    num_automobilis = Automobilis.objects.all().count()
    num_uzsakymas = Uzsakymas.objects.all().count()
    num_paslauga = Paslauga.objects.all().count()
    num_eilute = UzsakymoEilute.objects.all().count()

    # def authors(request):
    #     authors = Automobiliai.objects.all()
    #     context = {
    #         'authors': automobiliai
    #     }
    #     print(authors)
    #     return render(request, 'automobiliai.html', context=context)

    context = {
        'num_modelis': num_modelis,
        'num_automobilis': num_automobilis,
        'num_uzsakymas': num_uzsakymas,
        'num_paslauga': num_paslauga,
        'num_eilute': num_eilute
    }
    return render(request, 'paslaugos/index.html', context=context)

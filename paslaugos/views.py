from django.contrib.auth.views import LogoutView
from django.shortcuts import render, get_object_or_404
from .models import *
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin


def index(request):
    num_modelis = AutomobilioModelis.objects.all().count()
    num_automobilis = Automobilis.objects.all().count()
    num_uzsakymas = Uzsakymas.objects.all().count()
    num_paslauga = Paslauga.objects.all()
    num_eilute = UzsakymoEilute.objects.all().count()

    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_modelis': num_modelis,
        'num_automobilis': num_automobilis,
        'num_uzsakymas': num_uzsakymas,
        'num_paslauga': num_paslauga,
        'num_eilute': num_eilute,
        'num_visits': num_visits,

    }
    return render(request, 'paslaugos/index.html', context=context)


def automobiliai(request):
    automobiliai = Automobilis.objects.all()
    return render(request, 'paslaugos/automobiliai.html', {'automobiliai': automobiliai})


def automobilio_modeliai(request):
    paginator = Paginator(AutomobilioModelis.objects.all(), 2)
    page_number = request.GET.get('page')
    paged_auto = paginator.get_page(page_number)
    return render(request, 'paslaugos/automobiliomodelis.html', {'automobilio_modeliai': paged_auto})


class UzsakymaiListView(generic.ListView):
    model = Uzsakymas
    paginate_by = 2
    template_name = 'paslaugos/uzsakymas.html'


def paslauga(request):
    paslauga = Paslauga.objects.all()
    return render(request, 'paslaugos/paslauga.html', {'paslauga': paslauga})

# def get_full_text(request):
#     paslauga = Paslauga.objects.all()
#     return render(request, 'paslaugos/paslauga.html', {'aprasymas': paslauga.aprasymas})


def automobilio_duomenys(request, automobilis_id):
    automobilio_modelis = get_object_or_404(Automobilis, pk=automobilis_id)
    return render(request, 'paslaugos/automobilio_duomenys.html', {'automobilio_duomenys': automobilio_modelis})


class SaskaitosListView(generic.ListView):
    model = Uzsakymas
    template_name = 'paslaugos/saskaitos_list.html'


class SaskaitosDetailView(generic.DetailView):
    model = Uzsakymas
    template_name = 'paslaugos/saskaitos_detail.html'

    def get_context_data(self, **kwargs):
        context = super(SaskaitosDetailView, self).get_context_data(**kwargs)
        context['uzsakymo_eilutes'] = UzsakymoEilute.objects.all()
        return context


def search(request):
    query = request.GET.get('query')
    search_results = Automobilis.objects.filter(Q(klientas__icontains=query)
                                                | Q(automobilio_modelis__modelis__icontains=query)
                                                | Q(automobilio_modelis__marke__icontains=query)
                                                | Q(valstybinis_nr__icontains=query)
                                                | Q(vin_kodas__icontains=query))
    return render(request, 'paslaugos/search.html', {'automobilis': search_results, 'query': query})

class CustomLogout(LogoutView):
    template_name = 'registration/logged_out.html'

class AutoByUserListView(LoginRequiredMixin, generic.ListView):
    model = Uzsakymas
    template_name = 'paslaugos/vartotojo_auto.html'
    paginate_by = 10

    def get_queryset(self):
        return Uzsakymas.objects.filter(vartotojas=self.request.user).filter(status__exact='v').order_by('atsiemimo_data')


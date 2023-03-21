from django.contrib.auth.views import LogoutView
from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import *
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.views.generic.edit import FormMixin
from .forms import UzsakymasReviewForm, UserAutomobilisCreateForm
from django.contrib.auth.decorators import login_required
from .forms import UzsakymasReviewForm, UserUpdateForm, ProfilisUpdateForm
from django.contrib.auth.mixins import UserPassesTestMixin
from django.utils.translation import gettext as _


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


class UzsakymasDetailView(FormMixin, generic.DetailView):
    model = Uzsakymas
    template_name = 'paslaugos/uzsakymas_detail.html'
    form_class = UzsakymasReviewForm

    def get_success_url(self):
        return reverse('uzsakymas-detail', kwargs={'pk': self.object.id})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.uzsakymas = self.object
        form.instance.reviewer = self.request.user
        form.save()
        return super(UzsakymasDetailView, self).form_valid(form)


def paslauga(request):
    paslauga = Paslauga.objects.all()
    return render(request, 'paslaugos/paslauga.html', {'paslauga': paslauga})


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
        return Uzsakymas.objects.filter(vartotojas=self.request.user).order_by('atsiemimo_data')


@csrf_protect
def register(request):
    if request.method == "POST":
        # pasiimame reikšmes iš registracijos formos
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        # tikriname, ar sutampa slaptažodžiai
        if password == password2:
            # tikriname, ar neužimtas username
            if User.objects.filter(username=username).exists():
                messages.error(request, _(f'Username {username} already exists'))
                return redirect('register')
            else:
                # tikriname, ar nėra tokio pat email
                if User.objects.filter(email=email).exists():
                    messages.error(request, _(f'Email {email} already exists'))
                    return redirect('register')
                else:
                    # jeigu viskas tvarkoje, sukuriame naują vartotoją
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.info(request, f'Vartotojas {username} užregistruotas!')
                    return redirect('login')
        else:
            messages.error(request, _('Passwords do not match!'))
            return redirect('register')
    return render(request, 'paslaugos/register.html')


@login_required
def profilis(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfilisUpdateForm(request.POST, request.FILES, instance=request.user.profilis)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Profilis atnaujintas")
            return redirect('profilis')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfilisUpdateForm(instance=request.user.profilis)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'paslaugos/profilis.html', context)


class UzsakymasByUserCreateView(LoginRequiredMixin, generic.CreateView):
    model = Uzsakymas
    # fields = ['book', 'due_back']
    success_url = "/paslaugos/manoauto/"
    template_name = 'paslaugos/user_automobilis_form.html'
    form_class = UserAutomobilisCreateForm

    def form_valid(self, form):
        form.instance.reader = self.request.user
        return super().form_valid(form)


class UzsakymasByUserUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Uzsakymas
    fields = ['automobilis', 'grazinimo_data']
    success_url = "/paslaugos/manoauto/"
    template_name = 'paslaugos/user_automobilis_form.html'

    def form_valid(self, form):
        form.instance.vartotojas = self.request.user
        return super().form_valid(form)

    def test_func(self):
        uzsakymas = self.get_object()
        return self.request.user == uzsakymas.vartotojas


class UzsakymasByUserDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Uzsakymas
    success_url = "/paslaugos/manoauto/"
    template_name = 'paslaugos/user_uzsakymas_delete.html'

    def test_func(self):
        uzsakymas = self.get_object()
        return self.request.user == uzsakymas.vartotojas

from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from django.db.models import Count
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from .models import Lokacija, Knjiga, Izposojeno, User
from .forms import LoginForm, RegistrationForm, DodajForm
import operator
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy

def prijava(request):
    context = {}
    context['loginForm'] = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(redirect_to=("/isci/"))
    return render(request, "lib/index.html", context)

def odjava(request):
  logout(request)
  return HttpResponseRedirect(redirect_to=("/prijava/"))


def registracija(request):
    context = {}
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
            )
            return HttpResponseRedirect(redirect_to=("/prijava/"))
    else:
        form = RegistrationForm()
    context['registrationForm'] = form
    return render(request, "lib/registracija.html", context)

@login_required(login_url="/prijava/")
def isci(request):
    context = {}
    knjige = Knjiga.objects.order_by('avtorji')[:10]
    izposojeno = Izposojeno.objects.filter(knjiga__in=knjige)
    context['knjige'] = knjige
    context['izposojeno'] = izposojeno
    return render(request, 'lib/isci.html', context)

@login_required(login_url="/prijava/")
def iskanje(request, niz):
    context = {}
    knjige = Knjiga.objects.filter(naslov__icontains=niz)[:10]
    #knjige.add(Knjiga.objects.filter(avtorji__icontains=niz))
    izposojeno = Izposojeno.objects.filter(knjiga__in=knjige)
    context['knjige'] = knjige
    context['izposojeno'] = izposojeno
    return render(request, 'lib/isci.html', context)

@login_required(login_url="/prijava/")
def izposoja(request, knjiga_id):
    context = {}
    k = Knjiga.objects.get(pk=knjiga_id)
    izposoja1 = Izposojeno(knjiga=k, uporabnik=request.user, izposoja=timezone.now, vracilo=False)
    izposoja1.save()
    knjige = Knjiga.objects.order_by('avtorji')[:10]
    izposojeno = Izposojeno.objects.filter(knjiga__in=knjige)
    context['knjige'] = knjige
    context['izposojeno'].update = izposojeno
    return render(request, "lib/isci.html", context)

@login_required(login_url="/prijava/")
def vrni(request):
    context = {}
    izposojeno = Izposojeno.objects.filter(uporabnik=request.user)
    context['izposojeno'] = izposojeno
    return render(request, "lib/vrni.html", context)

@login_required(login_url="/prijava/")
def vracilo(request, izposoja_id):
    v = Izposojeno.objects.get(pk=izposoja_id)
    v.vracilo = True
    v.save()
    print(v.vracilo)
    return HttpResponseRedirect(redirect_to=("/vrni/"))

@login_required(login_url="/prijava/")
def vrniVse(request):
    izposojeno = Izposojeno.objects.filter(uporabnik=request.user)
    for v in izposojeno:
        v.vracilo = True
        v.save()
        print(v.vracilo)
    return HttpResponseRedirect(redirect_to=("/isci/"))

@method_decorator(login_required(login_url="/prijava/"), name='dispatch')
class KnjigaDodaj(CreateView):
    template_name = 'lib/dodaj.html'
    model = Knjiga
    fields = ['avtorji', 'naslov', 'lokacija']
    success_url = reverse_lazy('isci')

    def form_valid(self, form):
        form.instance.dodajalec = self.request.user
        return super(KnjigaDodaj, self).form_valid(form)

@login_required(login_url="/prijava/")
def statistika(request):
    context = {}
    izposojeno = Izposojeno.objects.order_by('izposoja')
    print(izposojeno)
    n = {}
    for naj in izposojeno:
        if naj.knjiga in n:
            n[naj.knjiga] += 1
        else:
            n[naj.knjiga] = 1
    najpogosteje = []
    for stevec, key in enumerate(sorted(n.items(), key=operator.itemgetter(1), reverse=True)):
        print(key)
        najpogosteje.append(key[0])
        if stevec >= 9:
            break

    print(najpogosteje)

    dodane = Knjiga.objects.annotate(Count('dodajalec_id', distinct=True))
    context['izposojeno'] = izposojeno
    context['najpogosteje'] = najpogosteje
    context['dodane'] = dodane
    return render(request, "lib/statistika.html", context)

@permission_required('Lokacija.can_add', login_url="/prijava/")
def administrator(request):
    return render(request, "lib/administrator.html")

@login_required(login_url="/prijava/")
def profil(request):
    context = {}
    uporabnik = User.objects.order_by('username')
    context['uporabnik'] = uporabnik
    for u in uporabnik:
        print(u)
    return render(request, "lib/profil.html", context)
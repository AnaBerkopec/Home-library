from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Count

from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import ensure_csrf_cookie

from .models import Lokacija, Knjiga, Izposojeno, User
from .forms import LoginForm


@csrf_exempt
def prijava(request):
    context = {}
    knjige = Knjiga.objects.order_by('naslov')[:5]
    #context.update(csrf(request))
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return render(request, "lib/isci.html", context)

    context['knjige'] = knjige
    context['loginForm'] = LoginForm()

    return render(request, "lib/index.html", context)

def registracija(request):
    return render_to_response("lib/registracija.html")

#@login_required(login_url="prijava/")
def isci(request):
    context = {}
    knjige = Knjiga.objects.order_by('naslov')[:5]
    izposojeno = Izposojeno.objects.filter(knjiga__in=knjige)
    context['knjige'] = knjige
    context['izposojeno'] =  izposojeno
    return render_to_response('lib/isci.html', context)

def izposoja(request, knjiga_id): #ne dela se
    context = {}
    print(request)
    return render_to_response(request, "lib/isci.html", context)

def vrni(request):
    context = {}
    izposojeno = Izposojeno.objects.order_by('izposoja') #filter
    context['izposojeno'] = izposojeno
    return render_to_response("lib/vrni.html", context)

def dodaj(request):
    context = {}
    lokacije = Lokacija.objects.order_by('nadstropje')
    context['lokacije'] = lokacije
    return render_to_response("lib/dodaj.html", context)

def statistika(request):
    context = {}
    izposojeno = Izposojeno.objects.order_by('izposoja')
    najpogosteje = Izposojeno.objects.annotate(Count('knjiga'))
    dodane = Knjiga.objects.annotate(Count('dodajalec_id', distinct=True)) #not woring yet
    context['izposojeno'] = izposojeno
    context['najpogosteje'] = najpogosteje
    context['dodane'] = dodane
    for d in dodane:
        print(d.dodajalec)
    return render_to_response("lib/statistika.html", context)

def administrator(request):
    return render_to_response("lib/administrator.html")

def profil(request):
    context = {}
    uporabnik = User.objects.order_by('username')
    context['uporabnik'] = uporabnik
    for u in uporabnik:
        print(u)
    return render_to_response("lib/profil.html", context)
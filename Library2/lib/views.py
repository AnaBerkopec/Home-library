from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from .models import Lokacija, Knjiga, Izposojeno, User
from .forms import LoginForm, RegistrationForm, MenjajUsername, MenjajGeslo
import operator
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.models import Group


def prijava(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(redirect_to=("/isci/"))
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
    if request.user.is_authenticated:
        return HttpResponseRedirect(redirect_to=("/isci/"))
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
            group = Group.objects.get(name='Navadni uporabniki')
            user.groups.add(group)
            return HttpResponseRedirect(redirect_to=("/prijava/"))
    else:
        form = RegistrationForm()
    context['registrationForm'] = form
    return render(request, "lib/registracija.html", context)

@method_decorator(login_required(login_url="/prijava/"), name='dispatch')
class IsciKnjige(ListView):
    model = Knjiga
    template_name = "lib/isci.html"
    context_object_name = "knjige"
    paginate_by = 5

def isciFilter(request, niz):
    print(niz)
    return HttpResponseRedirect(redirect_to=("/vrni/"))

@login_required(login_url="/prijava/")
def iskanje(request, niz):
    context = {}
    knjige = Knjiga.objects.filter(naslov__icontains=niz)[:10]
    #knjige.add(Knjiga.objects.filter(avtorji__icontains=niz))
    izposojeno = Izposojeno.objects.filter(knjiga__in=knjige)
    context['knjige'] = knjige
    context['izposojeno'] = izposojeno
    return render(request, 'lib/vrni.html', context)

@login_required(login_url="/prijava/")
def izposoja(request, knjiga_id):
    k = Knjiga.objects.get(pk=knjiga_id)
    izposoja1 = Izposojeno(knjiga=k, uporabnik=request.user, vracilo=False)
    print(izposoja1.izposoja)
    izposoja1.save()
    return HttpResponseRedirect(redirect_to=("/isci/"))

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
    n = {}
    for naj in izposojeno:
        if naj.knjiga in n:
            n[naj.knjiga] += 1
        else:
            n[naj.knjiga] = 1
    najpogosteje = []
    for stevec, key in enumerate(sorted(n.items(), key=operator.itemgetter(1), reverse=True)):
        najpogosteje.append(key[0])
        if stevec >= 9:
            break

    dodaneKnjige = Knjiga.objects.order_by('dodajalec')
    d = {}
    for dod in dodaneKnjige:
        if dod.dodajalec in d:
            d[dod.dodajalec] += 1
        else:
            d[dod.dodajalec] = 1

    dodane = []
    for stevec, key in enumerate(sorted(d.items(), key=operator.itemgetter(1), reverse=True)):
        dodane.append(key[0].username + ' (' + str(key[1]) + ' knjig)')
        if stevec >= 9:
            break

    context['izposojeno'] = izposojeno
    context['najpogosteje'] = najpogosteje
    context['dodane'] = dodane
    return render(request, "lib/statistika.html", context)

#@method_decorator(login_required(login_url="/isci/"), name='dispatch')
#class LokacijaDodaj(views.LoginRequiredMixin, views.PermissionRequiredMixin,CreateView):
class LokacijaDodaj(CreateView):
    permission_required = "Lokacacija.can_add"
    template_name = 'lib/administrator.html'
    model = Lokacija
    fields =  ['nadstropje', 'omara', 'polica']
    success_url = reverse_lazy('isci')


@login_required(login_url="/prijava/")
def profil(request):
    context = {}
    context['menjajUsername'] = MenjajUsername()
    context['menjajGeslo'] = MenjajGeslo()
    print(request.user)
    context['uporabnik'] = request.user
    return render(request, "lib/profil.html", context)


@login_required(login_url="/prijava/")
def menjajUsername(request):
    context = {}
    context['menjajUsername'] = MenjajUsername()
    context['menjajGeslo'] = MenjajGeslo()
    if request.method == 'POST':
        form = MenjajUsername(request.POST)
        if form.is_valid():
            nov = form.cleaned_data['new_username']
            if not User.objects.filter(username=nov).exists():
                user = User.objects.get(username=request.user.username)
                user.username = nov
                user.save()
                return HttpResponseRedirect(redirect_to=("/isci/"))
    return HttpResponseRedirect(redirect_to=("/profil/"))


@login_required(login_url="/prijava/")
def menjajGeslo(request):
    context = {}
    context['menjajUsername'] = MenjajUsername()
    context['menjajGeslo'] = MenjajGeslo()
    if request.method == 'POST':
        form = MenjajGeslo(request.POST)
        if form.is_valid():
            nov = form.cleaned_data['password1']
            user = User.objects.get(username=request.user.username)
            user.set_password(nov)
            user.save()
            return HttpResponseRedirect(redirect_to=("/isci/"))
    return HttpResponseRedirect(redirect_to=("/profil/"))
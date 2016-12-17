from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response

def prijava(request):
    return render_to_response("lib/index.html")

def registracija(request):
    return render_to_response("lib/registracija.html")

def isci(request):
    return render_to_response('lib/isci.html')

def vrni(request):
    return render_to_response("lib/vrni.html")

def dodaj(request):
    return render_to_response("lib/dodaj.html")

def statistika(request):
    return render_to_response("lib/statistika.html")

def administrator(request):
    return HttpResponse("Hello, world. This is ADMIN.")

def profil(request):
    return render_to_response("lib/profil.html")
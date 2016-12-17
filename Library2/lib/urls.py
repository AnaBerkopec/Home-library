from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.prijava, name='prijava'),
    url(r'^registracija/', views.registracija, name='registracija'),
    url(r'^isci/', views.isci, name='isci'),
    url(r'^vrni/', views.vrni, name='vrni'),
    url(r'^dodaj/', views.dodaj, name='dodaj'),
    url(r'^statistika/', views.statistika, name='statistika'),
    url(r'^administrator', views.administrator, name='administrator'),
    url(r'^profil', views.profil, name='profil'),
]
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.prijava, name='prijava'),
    url(r'prijava/', views.prijava, name='prijava'),
    url(r'^registracija/', views.registracija, name='registracija'),

    #/isci/<gumb_id>
    url(r'^isci/$', views.isci, name='isci'),
    url(r'^isci/(?P<knjiga_id>[0-9]+)$', views.vrni, name='izposoja'), #fake
    url(r'^vrni/', views.vrni, name='vrni'),
    url(r'^dodaj/', views.dodaj, name='dodaj'),
    url(r'^statistika/', views.statistika, name='statistika'),
    url(r'^administrator', views.administrator, name='administrator'),
    url(r'^profil', views.profil, name='profil'),
    url(r'^odjava/', views.prijava, name='odjava'), #maybe not
]
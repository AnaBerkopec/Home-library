from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.prijava, name='prijava'),
    url(r'prijava/', views.prijava, name='prijava'),
    url(r'^registracija/', views.registracija, name='registracija'),
    url(r'^isci/$', views.isci, name='isci'),
    url(r'^isci/(?P<niz>[a-zA-Z]+)$', views.iskanje, name='isci'),
    url(r'^isci/(?P<knjiga_id>[0-9]+)$', views.izposoja, name='izposoja'),
    url(r'^vrni/$', views.vrni, name='vrni'),
    url(r'^vrni/vse$', views.vrniVse, name='vrniVse'),
    url(r'^vrni/(?P<izposoja_id>[0-9]+)$', views.vracilo, name='vracilo'),
    url(r'^dodaj/', views.KnjigaDodaj.as_view(), name='dodaj'),
    url(r'^statistika/', views.statistika, name='statistika'),
    url(r'^administrator', views.administrator, name='administrator'),
    url(r'^profil', views.profil, name='profil'),
    url(r'^odjava/', views.odjava, name='odjava'),
]
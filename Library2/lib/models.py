from __future__ import unicode_literals
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

class Lokacija(models.Model):
    nadstropje = models.IntegerField()
    omara = models.IntegerField()
    polica = models.IntegerField()

    def __str__(self):
        return str(self.nadstropje) + '.' + str(self.omara) + '.' + str(self.polica)


class Knjiga(models.Model):
    avtorji = models.CharField(max_length=200)
    naslov = models.CharField(max_length=200)
    lokacija = models.ForeignKey(Lokacija, on_delete=models.SET_NULL, null=True)
    dodajalec = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.avtorji + ': ' + self.naslov

    def pritlicje(self):
        if self.lokacija.nadstropje == 0:
            return True
        return False

    def podstreha(self):
        if self.lokacija.nadstropje == 3:
            return True
        return False

    def vecAvtorjev(self):
        if len(self.avtorji.split()) > 3:
            return True
        return False

class Izposojeno(models.Model):
    knjiga = models.ForeignKey(Knjiga, on_delete=models.SET_NULL, null=True, related_name='izposoje')
    uporabnik = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    izposoja = models.DateTimeField(default=timezone.now, blank=True)
    vracilo = models.BooleanField(default=False)

    def __str__(self):
        return self.knjiga.naslov + ' (' + self.uporabnik.username + ')'
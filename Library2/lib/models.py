from __future__ import unicode_literals
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

class Lokacija(models.Model):
    """Class representing the location of the book

    This class represents blablabla...
    """
    nadstropje = models.IntegerField()
    omara = models.IntegerField()
    polica = models.IntegerField()

    def __str__(self):
        """String representation of the location. This function...
        """
        return str(self.nadstropje) + '.' + str(self.omara) + '.' + str(self.polica)


class Knjiga(models.Model):
    avtorji = models.CharField(max_length=200)
    naslov = models.CharField(max_length=200)
    lokacija = models.ForeignKey(Lokacija, on_delete=models.SET_NULL, null=True)
    dodajalec = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.avtorji + ': ' + self.naslov

    def niIzposojena(self):
        i = Izposojeno.objects.filter(knjiga=self).order_by('-izposoja')
        if i and i[0].vracilo == False:
            return False
        return True

    def izposojenaKnjiga(self):
        return Izposojeno.objects.filter(knjiga=self).order_by('-izposoja')[0]


    def pritlicje(self):
        if self.lokacija.nadstropje == 0:
            return True
        return False

class Izposojeno(models.Model):
    knjiga = models.ForeignKey(Knjiga, on_delete=models.SET_NULL, null=True, related_name='izposoje')
    uporabnik = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    izposoja = models.DateTimeField(default=timezone.now, blank=True)
    vracilo = models.BooleanField(default=False)

    def __str__(self):
        return self.knjiga.naslov + ' (' + self.uporabnik.username + ')'
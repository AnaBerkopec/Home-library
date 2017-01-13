from django.test import TestCase

# Create your tests here.
# python manage.py test

from .models import Knjiga, Lokacija, Izposojeno

class KnjigaTests(TestCase):
    def test_niIzposojena(self):
        """
        niIzposojena() vrne True, ce knjiga ni izposojena
        """
        knjiga = Knjiga.objects.create(avtorji='avtor', naslov='test')
        Izposojeno.objects.create(knjiga=knjiga, vracilo=False)

        knjiga1 = Knjiga.objects.create(avtorji='avtor1', naslov='test1')
        Izposojeno.objects.create(knjiga=knjiga1, vracilo=True)

        self.assertIs(knjiga.niIzposojena(), False)
        self.assertIs(knjiga1.niIzposojena(), True)

    def test_izposojenaKnjiga(self):
        """
        izposojenaKnjiga() vrne podatke o zadnji izposoji izbrane knjige
        """
        knjiga1 = Knjiga.objects.create(avtorji='avtor1', naslov='test1')
        izposojeno1 = Izposojeno.objects.create(knjiga=knjiga1, vracilo=False)
        self.assertIs(knjiga1.izposojenaKnjiga().pk, izposojeno1.pk)

    def test_pritlicje(self):
        """
        pritlicje() vrne True, ce se knjiga nahaja v pritlicju
        """
        lok1 = Lokacija(nadstropje=0, omara=1, polica=1)
        lok2 = Lokacija(nadstropje=2, omara=1, polica=1)
        k_pritlicje = Knjiga(avtorji="Desa Muck", naslov="Anica", lokacija=lok1)
        k_prvo = Knjiga(avtorji="Desa Muck", naslov="Anica", lokacija=lok2)

        self.assertIs(k_pritlicje.pritlicje(), True)
        self.assertIs(k_prvo.pritlicje(), False)


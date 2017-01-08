from django.test import TestCase

# Create your tests here.
# path && ./manage.py test && echo "hello world"

from .models import Knjiga, Lokacija

class KnjigaTests(TestCase):
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

    def test_podstreha(self):
        """
        podstreha() vrne True, ce se knjiga nahaja na podstresju
        """
        lok1 = Lokacija(nadstropje=3, omara=1, polica=1)
        lok2 = Lokacija(nadstropje=2, omara=1, polica=1)
        k_pritlicje = Knjiga(avtorji="Desa Muck", naslov="Anica", lokacija=lok1)
        k_prvo = Knjiga(avtorji="Desa Muck", naslov="Anica", lokacija=lok2)

        self.assertIs(k_pritlicje.podstreha(), True)
        self.assertIs(k_prvo.podstreha(), False)

    def test_vecAvtorjev(self):
        """
        vecAvtorjev() vrne True, ce je stevilo besed pri avtorjih vecje od 3,
        torej je najverjetneje vec avtorjev
        """
        a_eden = Knjiga(avtorji="Desa Muck", naslov="Anica")
        a_vec = Knjiga(avtorji="Desa Muck, Tone Pavček", naslov="Anica")

        self.assertIs(a_eden.vecAvtorjev(), False)
        self.assertIs(a_vec.vecAvtorjev(), True)


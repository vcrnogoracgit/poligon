from django.db import models

class Poligon(models.Model):
    naziv = models.CharField(max_length=20)
    # -1 start
    # 0 dozvoljeno je da se stranice sijeku
    # 1 nije dozvoljeno da se stranice sijeku
    # 2 zavrsen unos tjemena poligona
    status = models.IntegerField(default=-1)


class Tacka(models.Model):
    x_koordinata = models.FloatField()
    y_koordinata = models.FloatField()
    redni_br = models.IntegerField(default=-1)
    poligon = models.ForeignKey(Poligon, on_delete=models.CASCADE)



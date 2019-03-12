from django.shortcuts import render, redirect
from .models import Tacka, Poligon
from .utility import tacke_u_poligonu

AKCIJA = "start"

def index(request):
    poligon = Poligon.objects.last()
    tjemena, tacke, br_tacaka_u_polinomu = tacke_u_poligonu()
    broj_tjemena = len(tjemena)

    context = {
        "poligon": poligon,
        "tjemena": tjemena,
        "tacke": tacke,
        "broj_tjemena": broj_tjemena,
        "broj_tacaka": len(tacke),
        "broj_tacaka_u_poligonu": br_tacaka_u_polinomu,
        "akcija": AKCIJA,
    }
    return render(request, 'template.html', context)

def kreiraj_piligon(request):
    naziv_poligona = request.POST['naziv_poligona']
    novi_poligon = Poligon.objects.create(naziv=naziv_poligona, status=-1)
    novi_poligon.save()
    global AKCIJA
    AKCIJA = "dodaj_poligon"
    return redirect('index')


def dodaj_tacku(request):
    x = request.POST['x_koordinata']
    y = request.POST['y_koordinata']
    tjeme_tacka = request.POST['tjeme_tacka']
    akcija = "dodaj_tacku"

    poligon = Poligon.objects.last()
    if tjeme_tacka == "ZATVORI_POLIGON":
        poligon.status = 2
        poligon.save()
        redni_br = -1
    else:
        poligon_tjemena = Tacka.objects.filter(poligon=poligon)
        redni_br = len(poligon_tjemena)
        akcija = "dodaj_tjeme"
    nova_tacka = Tacka.objects.create(x_koordinata=x, y_koordinata=y, redni_br=redni_br, poligon=poligon)
    nova_tacka.save()
    global AKCIJA
    AKCIJA = akcija
    return redirect('index')


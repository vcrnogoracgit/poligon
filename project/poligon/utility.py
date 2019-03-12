from math import sqrt, pow
from sys import maxsize
from .models import Tacka, Poligon

SIJECE = 0
NE_SIJECE = 1
NA_STRANICI = 2

def poluprava_sijece_stranicu (tacka, tjeme1, tjeme2):
    x_tacka = tacka.x_koordinata
    y_tacka = tacka.y_koordinata
    x_tjeme_1 = tjeme1.x_koordinata
    y_tjeme_1 = tjeme1.y_koordinata
    x_tjeme_2 = tjeme2.x_koordinata
    y_tjeme_2 = tjeme2.y_koordinata
    if (y_tacka < y_tjeme_1 and y_tacka < y_tjeme_2) or \
       (y_tacka > y_tjeme_1 and y_tacka > y_tjeme_2) or \
       (x_tacka > x_tjeme_1 and x_tacka > x_tjeme_2):
        return NE_SIJECE
    if x_tacka < x_tjeme_1 and x_tacka < x_tjeme_2:
        return SIJECE
    if x_tjeme_2 == x_tjeme_1:
        if x_tjeme_1 == x_tacka:
            return NA_STRANICI
        else:
            return NE_SIJECE
    k = (y_tjeme_2 - y_tjeme_1)/(x_tjeme_2 - x_tjeme_1)
    # jednacina prave kroz dvije tacke  y = k(x - x1) + y1
    y = k*(x_tacka - x_tjeme_1) + y_tjeme_1
    if y == y_tacka:
        return NA_STRANICI
    elif( y > y_tacka and k < 0 ) or (y < y_tacka and k > 0):
        return SIJECE
    else:
        return NE_SIJECE

def get_sort_key(tjeme):
    return tjeme.redni_br

def dodatno_ispitivanje(tjeme1, tjeme2, tjeme3):
    y1 = tjeme1.y_koordinata
    y2 = tjeme2.y_koordinata
    y3 = tjeme3.y_koordinata
    if (y1 >= y2 and y2 >= y3) or ( y1 <= y2 and y2 <= y3):
        return 1
    else:
        return 0

def tacke_u_poligonu():
    poligon = Poligon.objects.last()
    tacke_poligon = Tacka.objects.filter(poligon=poligon)
    tjemena = [tjeme for tjeme in tacke_poligon if tjeme.redni_br is not -1]
    tacke_model = [tacka for tacka in tacke_poligon if tacka.redni_br is -1]
    tjemena_model = sorted(tjemena, key=get_sort_key)
    tacke_view = []
    br_tacaka_u_polinomu = 0
    for tacka in tacke_model:
        tacka_je_na_stranici = False
        brojac_presjeka = 0
        max_daljina = 0
        min_daljina = maxsize
        dict_ = {"x_koordinata": tacka.x_koordinata,
                 "y_koordinata": tacka.y_koordinata,
                 "tacka_je_u_poligonu": 0,
                 }
        for i in range(len(tjemena)):
            tjeme1 = tjemena_model[i-1]
            tjeme2 = tjemena_model[i]
            stranica_poligona = daljina_dvije_tacke(tjeme1, tjeme2)
            stranica1 = daljina_dvije_tacke(tacka, tjeme1)
            stranica2 = daljina_dvije_tacke(tacka, tjeme2)
            max_daljina = max(max_daljina, stranica1, stranica2)
            d = udaljenost_tacka_duzi(stranica_poligona, stranica1, stranica2)
            min_daljina = min(min_daljina, d)
            sijece = poluprava_sijece_stranicu(tacka, tjeme1, tjeme2)
            if sijece == NA_STRANICI:
                tacka_je_na_stranici = True
            elif sijece == SIJECE:
                brojac_presjeka += 1
            if tacka.y_koordinata == tjeme2.y_koordinata and sijece == SIJECE:
                tjeme3 = tjemena[(i+1) % len(tjemena)]
                smanji = dodatno_ispitivanje(tjeme1, tjeme2, tjeme3)
                brojac_presjeka -= smanji
        dict_["max_daljina"] = round(max_daljina, 2)
        dict_["min_daljina"] = round(min_daljina, 2)
        if tacka_je_na_stranici or brojac_presjeka % 2 == 1:
            dict_["tacka_je_u_poligonu"] = 1
            br_tacaka_u_polinomu += 1
        tacke_view.append(dict_)
    return tjemena_model, tacke_view, br_tacaka_u_polinomu

def daljina_dvije_tacke(tacka_1, tacka_2):
    x1 = tacka_1.x_koordinata
    y1 = tacka_1.y_koordinata
    x2 = tacka_2.x_koordinata
    y2 = tacka_2.y_koordinata
    x = pow((x1 - x2), 2)
    y = pow((y1 - y2), 2)
    d = sqrt(x + y)
    return d

def udaljenost_tacka_duzi(stranica_poligona, stranica1, stranica2):
    s = (stranica_poligona + stranica1 + stranica2)/2.0
    P = sqrt(s * (s - stranica_poligona) * (s - stranica1) * (s - stranica2))
    h = 2*P/stranica_poligona
    kraca = stranica1
    duza = stranica2
    if stranica1 > stranica2:
        kraca = stranica2
        duza = stranica1
    if pow(duza, 2) < pow(kraca, 2) + pow(stranica_poligona, 2):
        return h
    else:
        return kraca

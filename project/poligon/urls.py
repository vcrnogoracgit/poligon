from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'dodaj_tacku', views.dodaj_tacku, name='dodaj_tacku'),
    url(r'dodaj_poligon', views.kreiraj_piligon, name='dodaj_poligon'),
]

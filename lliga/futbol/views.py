from django.shortcuts import render
from .models import Lliga, Equip, Partit
import time

def classificacio(request):
    start_time = time.time()
    
    lliga = Lliga.objects.first()
    if not lliga:
        return render(request, "classificacio.html", {"classificacio": [], "temps": 0})

    equips = Equip.objects.all()
    classi = []
    partidos_de_esta_liga = list(Partit.objects.filter(lliga=lliga))

    for equip in equips:
        punts = 0
        for partit in partidos_de_esta_liga:
            if partit.local == equip:
                if partit.gols_local() > partit.gols_visitant():
                    punts += 3
                elif partit.gols_local() == partit.gols_visitant():
                    punts += 1
            
            elif partit.visitant == equip:
                if partit.gols_visitant() > partit.gols_local():
                    punts += 3
                elif partit.gols_visitant() == partit.gols_local():
                    punts += 1
        
        classi.append((punts, equip.nom))

    classi.sort(reverse=True)
    
    end_time = time.time()
    durada = end_time - start_time

    return render(request, "classificacio.html", {
        "classificacio": classi,
        "temps": round(durada, 4),
    })
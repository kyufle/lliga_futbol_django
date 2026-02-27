from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from datetime import datetime, time
from random import randint
from futbol.models import *

faker = Faker(["es_CA","es_ES"])

class Command(BaseCommand):
    help = 'Crea una lliga amb equips i jugadors'

    def add_arguments(self, parser):
        parser.add_argument('titol_lliga', nargs=1, type=str)

    def handle(self, *args, **options):
        titol_lliga = options['titol_lliga'][0]
        if Lliga.objects.filter(nom=titol_lliga).exists():
            print("Aquesta lliga ja està creada.")
            return

        print(f"Creem la nova lliga: {titol_lliga}")
        lliga = Lliga.objects.create(nom=titol_lliga, temporada="2025-2026")

        print("\n--- CREANT EQUIPS I JUGADORS ---")
        prefixos = ["RCD", "Athletic", "", "Deportivo", "Unión Deportiva"]
        
        for i in range(20):
            ciutat = faker.city()
            prefix = prefixos[randint(0, len(prefixos)-1)]
            if prefix:
                prefix += " "
            nom_equip = f"{prefix}{ciutat}".strip()
            equip = Equip.objects.create(ciutat=ciutat, nom=nom_equip, lliga=lliga)
            
            print(f"\nEquip {i+1}: {nom_equip}")
            for j in range(25):
                jugador = Jugador.objects.create(
                    nom=faker.name(),
                    posicio="jugador",
                    edat=25,
                    equip=equip
                )
                print(f"  - Jugador {j+1}: {jugador.nom}")

        print("\n--- CREANT PARTITS I GOLS ---")
        equips = lliga.equips.all()
        comptador_partits = 0
        
        for local in equips:
            for visitant in equips:
                if local != visitant:
                    partit = Partit.objects.create(
                        local=local, 
                        visitant=visitant, 
                        lliga=lliga,
                        data=timezone.make_aware(datetime(2026, randint(1,12), randint(1,28), randint(16,21), 0))
                    )
                    comptador_partits += 1

                    for _ in range(randint(0, 5)):
                        jugadors = local.jugadors.all()
                        m_total = randint(1, 90)
                        Event.objects.create(
                            partit=partit,
                            temps=time(m_total // 60, m_total % 60),
                            tipus=Event.EventType.GOL,
                            jugador=jugadors[randint(0, 24)],
                            equip=local
                        )

                    for _ in range(randint(0, 5)):
                        jugadors = visitant.jugadors.all()
                        m_total = randint(1, 90)
                        Event.objects.create(
                            partit=partit,
                            temps=time(m_total // 60, m_total % 60),
                            tipus=Event.EventType.GOL,
                            jugador=jugadors[randint(0, 24)],
                            equip=visitant
                        )

                    print(f" Partit {comptador_partits}: {local.nom} ({partit.gols_local()}) - {visitant.nom} ({partit.gols_visitant()})")

        print(f"\n Lliga '{titol_lliga}' creada amb èxit!")
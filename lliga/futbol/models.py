from django.db import models

class Lliga(models.Model):
    class Meta:
        verbose_name_plural = "Lligues"
    nom = models.CharField(max_length=100)
    pais = models.CharField(max_length=50, default="Catalunya")
    temporada = models.CharField(max_length=20)

    def __str__(self):
        return self.nom

class Equip(models.Model):
    nom = models.CharField(max_length=100)
    ciutat = models.CharField(max_length=100)
    lliga = models.ForeignKey(Lliga, on_delete=models.CASCADE, related_name='equips')

    def __str__(self):
        return self.nom

class Jugador(models.Model):
    nom = models.CharField(max_length=100)
    cognom = models.CharField(max_length=100, null=True, blank=True) # Permet buit per compatibilitat amb script
    posicio = models.CharField(max_length=50)
    equip = models.ForeignKey(Equip, on_delete=models.CASCADE, related_name='jugadors')
    edat = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        if self.cognom:
            return f"{self.nom} {self.cognom}"
        return self.nom

class Partit(models.Model):
    class Meta:
        unique_together = ["local", "visitant", "lliga"]

    lliga = models.ForeignKey(Lliga, on_delete=models.CASCADE, related_name='partits')
    local = models.ForeignKey(Equip, on_delete=models.CASCADE, related_name="partits_local")
    visitant = models.ForeignKey(Equip, on_delete=models.CASCADE, related_name="partits_visitant")
    data = models.DateTimeField(null=True, blank=True) # Canviat a opcional perquè l'script no el posa
    detalls = models.TextField(null=True, blank=True)

    def __str__(self):
        return "{} - {} ({} - {})".format(
            self.local, 
            self.visitant, 
            self.gols_local(), 
            self.gols_visitant()
        )

    def gols_local(self):
        return self.event_set.filter(
            tipus=Event.EventType.GOL, equip=self.local).count()

    def gols_visitant(self):
        return self.event_set.filter(
            tipus=Event.EventType.GOL, equip=self.visitant).count()

class Event(models.Model):
    class EventType(models.TextChoices):
        GOL = "GOL"
        AUTOGOL = "AUTOGOL"
        FALTA = "FALTA"
        PENALTY = "PENALTY"
        MANS = "MANS"
        CESSIO = "CESSIO"
        FORA_DE_JOC = "FORA_DE_JOC"
        ASSISTENCIA = "ASSISTENCIA"
        TARGETA_GROGA = "TARGETA_GROGA"
        TARGETA_VERMELLA = "TARGETA_VERMELLA"

    partit = models.ForeignKey(Partit, on_delete=models.CASCADE)
    temps = models.TimeField()
    tipus = models.CharField(max_length=30, choices=EventType.choices)
    jugador = models.ForeignKey(Jugador, null=True, on_delete=models.SET_NULL, related_name="events_fets")
    equip = models.ForeignKey(Equip, null=True, on_delete=models.SET_NULL)
    jugador2 = models.ForeignKey(Jugador, null=True, blank=True, on_delete=models.SET_NULL, related_name="events_rebuts")
    detalls = models.TextField(null=True, blank=True)
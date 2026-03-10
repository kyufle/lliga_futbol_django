from django.contrib import admin
from .models import Lliga, Equip, Jugador, Partit, Event

admin.site.register(Lliga)
admin.site.register(Equip)
admin.site.register(Jugador)

class EventInline(admin.TabularInline):
    model = Event
    fields = ["temps","tipus","jugador","equip"]
    ordering = ("temps",)
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # filtrem els jugadors i només deixem els que siguin d'algun dels 2 equips (local o visitant)
        if db_field.name == "jugador":
            partit_id = request.resolver_match.kwargs['object_id']
            partit = Partit.objects.get(id=partit_id)
            # fem un queryset per cada equip
            jugadors_locals = partit.local.jugadors.all()
            jugadors_visitants = partit.visitant.jugadors.all()
            # fusionem els 2 querysets amb l'operador | (= union en BD)
            kwargs["queryset"] = jugadors_locals | jugadors_visitants
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


    

class PartitAdmin(admin.ModelAdmin):
    search_fields = ['local__nom', 'visitant__nom', 'lliga__nom']
    list_display = ('lliga', 'local', 'visitant', 'gols_local', 'gols_visitant')
    inlines = [EventInline]

admin.site.register(Partit, PartitAdmin)
from django.contrib import admin
from .models import Lliga, Equip, Jugador, Partit, Event

admin.site.register(Lliga)
admin.site.register(Equip)
admin.site.register(Jugador)

class EventInline(admin.TabularInline):
    model = Event
    extra = 2

class PartitAdmin(admin.ModelAdmin):
    inlines = [EventInline]
    list_display = ('__str__', 'data', 'lliga')
    list_filter = ('lliga', 'data')

admin.site.register(Partit, PartitAdmin)
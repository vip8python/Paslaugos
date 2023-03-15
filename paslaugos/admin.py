from django.contrib import admin
from .models import *

class UzsakymasAdmin(admin.ModelAdmin):
    list_display = ('automobilis', 'status', 'atsiemimo_data', 'data', 'suma')
    list_editable = ('status', 'atsiemimo_data')
    list_filter = ('status', 'atsiemimo_data')
    list_display_links = ('automobilis',)
    search_fields = ('automobilis__automobilio_modelis', )

    fieldsets = (
        (None, {
            'fields': ('automobilis',)
        }),
        ('Availability', {
            'fields': ('status', 'atsiemimo_data', 'vartotojas')
        }),
    )

class AutomobilisAdmin(admin.ModelAdmin):
    list_display = ('klientas', 'automobilio_modelis',
                    'valstybinis_nr', 'vin_kodas')
    list_display_links = ('klientas',)
    search_fields = ('valstybinis_nr', 'vin_kodas')
    list_filter = ('klientas', 'automobilio_modelis')


class PaslaugaAdmin(admin.ModelAdmin):
    list_display = ('pavadinimas', 'kaina')
    search_fields = ('pavadinimas',)



admin.site.register(AutomobilioModelis)
admin.site.register(Automobilis, AutomobilisAdmin)
admin.site.register(Uzsakymas, UzsakymasAdmin)
admin.site.register(UzsakymoEilute)
admin.site.register(Paslauga, PaslaugaAdmin)

admin.site.site_title = 'autoservisas'
admin.site.site_header = 'Autoserviso admin puslapis'

from django.contrib import admin
from .models import Visita

@admin.register(Visita)
class VisitaAdmin(admin.ModelAdmin):
    list_display = ['pagina', 'fecha']
    list_filter = ['fecha', 'pagina']
    search_fields = ['pagina']
    date_hierarchy = 'fecha'
    readonly_fields = ['pagina', 'fecha']
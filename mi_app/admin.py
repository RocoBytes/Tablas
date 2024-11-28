from django.contrib import admin
from .models import Tablero

@admin.register(Tablero)
class TableroAdmin(admin.ModelAdmin):
    list_display = ('tecnico', 'numero_ot', 'cliente', 'nombre_tablero', 
                   'fecha_entrega', 'dias_restantes', 'estado')
    list_filter = ('estado', 'tecnico')
    search_fields = ('numero_ot', 'cliente', 'nombre_tablero')
    readonly_fields = ('dias_restantes',)
    ordering = ('fecha_entrega',)

    def get_queryset(self, request):
        return super().get_queryset(request)

    def save_model(self, request, obj, form, change):
        obj.save()

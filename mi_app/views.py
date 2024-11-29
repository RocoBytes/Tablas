from django.shortcuts import render
from .models import Tablero

def lista_tableros(request):
    # Filtrar tableros que estén en 'Ejecución' o 'En Pruebas'
    tableros = Tablero.objects.filter(
        estado__in=['EJECUCION', 'EN_PRUEBAS']
    ).order_by('fecha_entrega')
    
    # Actualizar días restantes para cada tablero
    for tablero in tableros:
        tablero.dias_restantes = tablero.calcular_dias_restantes()
        tablero.save()
    
    return render(request, 'mi_app/lista_tableros.html', {'tableros': tableros})

from django.shortcuts import render
from .models import Tablero

def lista_tableros(request):
    # Obtener todos los tableros en ejecución
    tableros = Tablero.objects.filter(estado='EJECUCION').order_by('fecha_entrega')
    
    # Actualizar días restantes
    for tablero in tableros:
        tablero.dias_restantes = tablero.calcular_dias_restantes()
        tablero.save()
    
    return render(request, 'mi_app/lista_tableros.html', {'tableros': list(tableros)})

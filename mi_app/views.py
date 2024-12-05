from django.shortcuts import render
from .models import Tablero
from django.db.models import Q

def lista_tableros(request):
    # Incluir también los tableros pausados
    tableros = Tablero.objects.filter(
        Q(estado='EJECUCION') | 
        Q(estado='EN_PRUEBAS') |
        Q(estado='PAUSADO')
    ).order_by('fecha_entrega')
    
    return render(request, 'mi_app/lista_tableros.html', {
        'tableros': tableros
    })

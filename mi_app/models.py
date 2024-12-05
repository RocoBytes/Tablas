from django.db import models
from django.utils import timezone
from datetime import date

class Tablero(models.Model):
    ESTADOS = [
        ('EJECUCION', 'En Ejecución'),
        ('EN_PRUEBAS', 'En Pruebas'),
        ('TERMINADO', 'Terminado'),
        ('DESPACHADO', 'Despachado'),
        ('PAUSADO', 'Pausado'),
    ]

    tecnico = models.CharField(max_length=100, verbose_name='Técnico a cargo')
    numero_ot = models.CharField(max_length=20, verbose_name='N° OT')
    cliente = models.CharField(max_length=100)
    nombre_tablero = models.CharField(max_length=200, verbose_name='Nombre del Tablero')
    fecha_entrega = models.DateField(verbose_name='Fecha de Entrega')
    estado = models.CharField(max_length=20, choices=ESTADOS, default='EJECUCION')

    @property
    def dias_restantes(self):
        if self.estado == 'PAUSADO':
            return '-'
        
        if self.fecha_entrega:
            dias = (self.fecha_entrega - date.today()).days
            return dias
        return '-'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.numero_ot} - {self.nombre_tablero}"

    class Meta:
        verbose_name = 'Tablero'
        verbose_name_plural = 'Tableros'

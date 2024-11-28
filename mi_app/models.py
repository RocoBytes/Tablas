from django.db import models
from django.utils import timezone
from datetime import date

class Tablero(models.Model):
    ESTADO_CHOICES = [
        ('EJECUCION', 'Ejecución'),
        ('TERMINADO', 'Terminado'),
        ('DESPACHADO', 'Despachado'),
    ]

    tecnico = models.CharField(max_length=100, verbose_name='Técnico a cargo')
    numero_ot = models.CharField(max_length=20, verbose_name='N° OT')
    cliente = models.CharField(max_length=100)
    nombre_tablero = models.CharField(max_length=200, verbose_name='Nombre del Tablero')
    fecha_entrega = models.DateField(verbose_name='Fecha de Entrega')
    dias_restantes = models.IntegerField(verbose_name='Días restantes', editable=False)
    estado = models.CharField(
        max_length=20, 
        choices=ESTADO_CHOICES, 
        default='EJECUCION',
        verbose_name='Estado'
    )

    def calcular_dias_restantes(self):
        hoy = date.today()
        delta = self.fecha_entrega - hoy
        return delta.days

    def save(self, *args, **kwargs):
        self.dias_restantes = self.calcular_dias_restantes()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.numero_ot} - {self.nombre_tablero}"

    class Meta:
        verbose_name = 'Tablero'
        verbose_name_plural = 'Tableros'

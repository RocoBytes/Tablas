from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib import messages
import pandas as pd
from datetime import datetime
from .models import Tablero
from .forms import ExcelImportForm

@admin.register(Tablero)
class TableroAdmin(admin.ModelAdmin):
    list_display = ('tecnico', 'numero_ot', 'cliente', 'nombre_tablero', 
                   'fecha_entrega', 'dias_restantes', 'estado')
    list_filter = ('estado', 'tecnico')
    search_fields = ('numero_ot', 'cliente', 'nombre_tablero')
    readonly_fields = ('dias_restantes',)
    
    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path('import-excel/', self.import_excel, name='import_excel'),
        ]
        return new_urls + urls

    def import_excel(self, request):
        if request.method == 'POST':
            form = ExcelImportForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    excel_file = request.FILES['excel_file']
                    df = pd.read_excel(excel_file)
                    
                    # Verificar columnas requeridas
                    required_columns = ['Técnico', 'N° OT', 'Cliente', 
                                     'Nombre del Tablero', 'Fecha de Entrega', 'Estado']
                    if not all(col in df.columns for col in required_columns):
                        messages.error(request, 'El archivo no tiene todas las columnas requeridas')
                        return redirect('admin:mi_app_tablero_changelist')

                    # Procesar cada fila
                    for _, row in df.iterrows():
                        # Validar el estado
                        estado = row['Estado'].upper()
                        if estado not in ['EJECUCION', 'EN_PRUEBAS', 'TERMINADO', 'DESPACHADO']:
                            estado = 'EJECUCION'  # Estado por defecto

                        # Convertir fecha si es necesario
                        fecha_entrega = row['Fecha de Entrega']
                        if isinstance(fecha_entrega, str):
                            try:
                                fecha_entrega = datetime.strptime(fecha_entrega, '%d/%m/%Y').date()
                            except ValueError:
                                fecha_entrega = datetime.strptime(fecha_entrega, '%Y-%m-%d').date()

                        # Crear o actualizar registro
                        Tablero.objects.update_or_create(
                            numero_ot=row['N° OT'],  # Usar N° OT como identificador único
                            defaults={
                                'tecnico': row['Técnico'],
                                'cliente': row['Cliente'],
                                'nombre_tablero': row['Nombre del Tablero'],
                                'fecha_entrega': fecha_entrega,
                                'estado': estado,
                            }
                        )

                    messages.success(request, 'Datos importados exitosamente')
                except Exception as e:
                    messages.error(request, f'Error al importar datos: {str(e)}')
                
                return redirect('admin:mi_app_tablero_changelist')
        
        form = ExcelImportForm()
        return render(request, 'admin/excel_import.html', {'form': form})

    def get_queryset(self, request):
        return super().get_queryset(request)

    def save_model(self, request, obj, form, change):
        obj.save()

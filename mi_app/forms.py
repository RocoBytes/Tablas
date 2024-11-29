from django import forms

class ExcelImportForm(forms.Form):
    excel_file = forms.FileField(
        label='Seleccionar archivo Excel',
        help_text='El archivo debe tener las columnas: Técnico, N° OT, Cliente, Nombre del Tablero, Fecha de Entrega, Estado'
    )

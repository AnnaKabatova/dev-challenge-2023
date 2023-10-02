from django.contrib import admin
from .models import Spreadsheet, Cell


@admin.register(Spreadsheet)
class SpreadsheetAdmin(admin.ModelAdmin):
    list_display = ('id',)


@admin.register(Cell)
class CellAdmin(admin.ModelAdmin):
    list_display = ('cell_id', 'value', 'result', 'spreadsheet')
    list_filter = ('spreadsheet',)

from rest_framework import serializers
from .models import Cell, Sheet


class CellSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cell
        fields = ['cell_id', 'sheet', 'value', 'result']

class SheetSerializer(serializers.ModelSerializer):
    cells = CellSerializer(many=True, read_only=True)

    class Meta:
        model = Sheet
        fields = ['sheet_id', 'cells']

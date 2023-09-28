from rest_framework import serializers
from .models import Cell, Sheet


class CellCreateSerializer(serializers.Serializer):
    value = serializers.CharField()


class CellSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cell
        fields = '__all__'

class SheetSerializer(serializers.ModelSerializer):
    cells = CellSerializer(many=True, read_only=True)

    class Meta:
        model = Sheet
        fields = ['sheet_id', 'cells']

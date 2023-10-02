from rest_framework import serializers
from .models import Spreadsheet, Cell


class SpreadsheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spreadsheet
        fields = '__all__'


class CellSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cell
        fields = ['value', 'result']
        extra_kwargs = {
            'result': {'required': False}
        }

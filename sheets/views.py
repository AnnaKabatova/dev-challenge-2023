from rest_framework import generics, status
from rest_framework.response import Response
from .models import Cell, Sheet
from .serializers import CellSerializer, SheetSerializer


class CellCreateRetrieveView(generics.GenericAPIView):
    serializer_class = CellSerializer
    
    def get(self, sheet_id, cell_id):
        try:
            cell = Cell.objects.get(sheet__sheet_id__iexact=sheet_id, cell_id__iexact=cell_id)
            serializer = self.serializer_class(cell)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Cell.DoesNotExist:
            return Response({'detail': 'Cell not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request, sheet_id, cell_id):
        data = request.data
        data['sheet'] = sheet_id
        data['cell_id'] = cell_id  # Ensure cell_id is set for create/update
        serializer = self.serializer_class(data=data)
        
        if serializer.is_valid():
            cell, created = Cell.objects.get_or_create(
                sheet__sheet_id__iexact=sheet_id,
                cell_id__iexact=cell_id,
                defaults={'value': data['value']}
            )
            
            if not created:
                cell.value = data['value']
                cell.save()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


I


class SheetRetrieveView(generics.RetrieveAPIView):
    serializer_class = SheetSerializer
    queryset = Sheet.objects.all()
    
    def retrieve(self, request, *args, **kwargs):
        sheet_id = self.kwargs.get('sheet_id', '').lower()

        try:
            sheet = Sheet.objects.get(sheet_id__iexact=sheet_id)
        except Sheet.DoesNotExist:
            return Response({'detail': 'Sheet not found'}, status=status.HTTP_404_NOT_FOUND)

        cells = Cell.objects.filter(sheet=sheet)
        serialized_cells = CellSerializer(cells, many=True).data

        response_data = {cell.cell_id: cell for cell in serialized_cells}

        return Response(response_data, status=status.HTTP_200_OK)

import sympy
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Cell, Sheet
from .serializers import CellCreateSerializer, CellSerializer, SheetSerializer


class CellCreateRetrieveView(generics.GenericAPIView):
    serializer_class = CellSerializer
    
    def calculate_cell_result(self, value):
        if not isinstance(value, (str, int, float)):
            return 'ERROR: Invalid data type'

        if value.startswith('='):
            try:
                expr = sympy.sympify(value[1:])
                if expr.has(sympy.zoo):
                    return 'ERROR: Division by zero'
                return str(expr.evalf())
            except (sympy.SympifyError, ValueError):
                return 'ERROR: Invalid mathematical expression'
        else:
            return value

    def get(self, request, sheet_id, cell_id):
        try:
            cell = Cell.objects.get(sheet__sheet_id__iexact=sheet_id, cell_id__iexact=cell_id)
            serializer = self.serializer_class(cell)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Cell.DoesNotExist:
            return Response({'detail': 'Cell not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request, sheet_id, cell_id):
        data = {"value": request.data.get("value")}
        data["sheet"] = sheet_id
        data["cell_id"] = cell_id
        serializer = CellCreateSerializer(data=data)
        
        if serializer.is_valid():
            if self.detect_circular_dependency(sheet_id, cell_id, data['value']):
                return Response({'error': 'Circular dependency detected'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

            cell, created = Cell.objects.get_or_create(
                sheet__sheet_id__iexact=sheet_id,
                cell_id__iexact=cell_id,
                defaults={'value': data['value']}
            )

            if not created:
                cell.value = data['value']

            cell.result = self.calculate_cell_result(data['value'])

            cell.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def detect_circular_dependency(self, sheet_id, cell_id, value):
        visited_cells = set()
        stack = [(sheet_id, cell_id)]

        while stack:
            current_sheet, current_cell = stack.pop()
            visited_cells.add((current_sheet, current_cell))

            try:
                cell = Cell.objects.get(sheet__sheet_id__iexact=current_sheet, cell_id__iexact=current_cell)
                cell_value = cell.value
            except Cell.DoesNotExist:
                continue

            if cell_value.startswith('='):
                cell_references = sympy.symbols(cell_value[1:])
                for ref in cell_references:
                    ref_sheet, ref_cell = ref.split('_')
                    if (ref_sheet.lower(), ref_cell.lower()) == (sheet_id.lower(), cell_id.lower()):
                        return True

                    if (ref_sheet.lower(), ref_cell.lower()) not in visited_cells:
                        stack.append((ref_sheet.lower(), ref_cell.lower()))
        return False


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

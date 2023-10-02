import re

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Spreadsheet, Cell
from .serializers import CellSerializer


def calculate_formula(formula, spreadsheet):
    try:
        variable_names = re.findall(r'[a-zA-Z]+\d+', formula)

        variable_values = []
        variable_not_found = []

        for var_name in variable_names:
            try:
                cell = Cell.get_by_cell_id(cell_id=var_name, spreadsheet=spreadsheet)
                variable_values.append(cell.value)
            except Cell.DoesNotExist:
                variable_not_found.append(var_name)

        if variable_not_found:
            return f'ERROR: Variables not found: {", ".join(variable_not_found)}'

        for var_name, value in zip(variable_names, variable_values):
            formula = formula.replace(var_name, str(value))

        result = str(eval(formula))

        return result
    except (SyntaxError, NameError, ValueError) as e:
        return 'ERROR'


@api_view(['GET', 'POST'])
def cell_create_retrieve(request, sheet_id, cell_id):
    try:
        spreadsheet, created = Spreadsheet.objects.get_or_create(id=sheet_id)
    except Exception as e:
        return Response(str(e), status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    try:
        cell = Cell.get_by_cell_id(spreadsheet=spreadsheet, cell_id=cell_id)
    except Cell.DoesNotExist:
        cell = Cell(spreadsheet=spreadsheet, cell_id=cell_id)

    if request.method == 'POST':
        data = {'value': request.data.get('value')}

        if data['value'].startswith('='):
            try:
                result = calculate_formula(data['value'][1:], spreadsheet)
                data['result'] = result
            except Exception as e:
                data['result'] = 'ERROR'
        else:
            data['result'] = data['value']

        serializer = CellSerializer(data=data)

        if serializer.is_valid():
            serializer.save(spreadsheet=spreadsheet, cell_id=cell_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    elif request.method == 'GET':
        serializer = CellSerializer(cell)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Unsupported HTTP method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
def sheet_data(request, sheet_id):
    try:
        spreadsheet = Spreadsheet.get_by_id(id=sheet_id)
    except Spreadsheet.DoesNotExist:
        return Response('Spreadsheet not found', status=status.HTTP_404_NOT_FOUND)

    cells = Cell.objects.filter(spreadsheet=spreadsheet).order_by('cell_id')
    data = {}

    for cell in cells:
        data[cell.cell_id] = {
            'value': cell.value,
            'result': cell.result
        }

    return Response(data, status=status.HTTP_200_OK)

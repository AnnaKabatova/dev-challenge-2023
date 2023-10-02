from django.urls import path

from .views import cell_create_retrieve, sheet_data

urlpatterns = [
    path('<sheet_id>/<cell_id>/', cell_create_retrieve, name='cell-create-retrieve'),
    path('<sheet_id>/', sheet_data, name='sheet-data'),
]

app_name = 'sheets'

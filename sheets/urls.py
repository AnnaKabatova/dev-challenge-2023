from django.urls import path

from .views import cell_create_retrieve, sheet_data

urlpatterns = [
    path('<sheet_id>/<cell_id>/', cell_create_retrieve),
    path('<sheet_id>/', sheet_data),
]

app_name = 'sheets'

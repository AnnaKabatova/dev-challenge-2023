from django.urls import path
from . import views

urlpatterns = [
    path('<str:sheet_id>/<str:cell_id>/', views.CellCreateRetrieveView.as_view()),
    path('<str:sheet_id>/', views.SheetRetrieveView.as_view()),
]

app_name = 'sheets'
